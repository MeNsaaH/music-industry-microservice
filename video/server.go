package main

import (
	"bytes"
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"net"
	"os"
	"os/signal"
	"strings"
	"sync"
	"syscall"
	"time"

	pb "github.com/mensaah/music-industry-microservice/genproto"
	healthpb "google.golang.org/grpc/health/grpc_health_v1"

	"github.com/golang/protobuf/jsonpb"
	"github.com/google/uuid"
	"github.com/sirupsen/logrus"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

var (
	cat          pb.ListVideosResponse
	videoMutex   *sync.Mutex
	log          *logrus.Logger
	extraLatency time.Duration

	port = "8003"

	reloadVideo bool
)

func init() {
	log = logrus.New()
	log.Formatter = &logrus.JSONFormatter{
		FieldMap: logrus.FieldMap{
			logrus.FieldKeyTime:  "timestamp",
			logrus.FieldKeyLevel: "severity",
			logrus.FieldKeyMsg:   "message",
		},
		TimestampFormat: time.RFC3339Nano,
	}
	log.Out = os.Stdout
	videoMutex = &sync.Mutex{}
	err := loadDB(&cat)
	if err != nil {
		log.Warnf("could not parse product video")
	}
}

func main() {
	flag.Parse()

	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGUSR1, syscall.SIGUSR2)
	go func() {
		for {
			sig := <-sigs
			log.Printf("Received signal: %s", sig)
			if sig == syscall.SIGUSR1 {
				reloadVideo = true
				log.Infof("Enable video reloading")
			} else {
				reloadVideo = false
				log.Infof("Disable video reloading")
			}
		}
	}()

	if os.Getenv("PORT") != "" {
		port = os.Getenv("PORT")
	}
	log.Infof("starting grpc server at :%s", port)
	run(port)
	select {}
}

func run(port string) string {
	l, err := net.Listen("tcp", fmt.Sprintf(":%s", port))
	if err != nil {
		log.Fatal(err)
	}
	srv := grpc.NewServer()
	svc := &dbVideo{}
	pb.RegisterVideoServiceServer(srv, svc)
	healthpb.RegisterHealthServer(srv, svc)
	go srv.Serve(l)
	return l.Addr().String()
}

type dbVideo struct{}

func loadDB(video *pb.ListVideosResponse) error {
	videoMutex.Lock()
	defer videoMutex.Unlock()
	videoJSON, err := ioutil.ReadFile("videos.json")
	if err != nil {
		log.Fatalf("failed to open video json file: %v", err)
		return err
	}
	if err := jsonpb.Unmarshal(bytes.NewReader(videoJSON), video); err != nil {
		log.Warnf("failed to parse the video JSON: %v", err)
		return err
	}
	log.Info("successfully parsed product video json")
	return nil
}

func parseVideo() []*pb.Video {
	if reloadVideo || len(cat.Video) == 0 {
		err := loadDB(&cat)
		if err != nil {
			return []*pb.Video{}
		}
	}
	return cat.Video
}

func (p *dbVideo) Check(ctx context.Context, req *healthpb.HealthCheckRequest) (*healthpb.HealthCheckResponse, error) {
	return &healthpb.HealthCheckResponse{Status: healthpb.HealthCheckResponse_SERVING}, nil
}

func (p *dbVideo) Watch(req *healthpb.HealthCheckRequest, ws healthpb.Health_WatchServer) error {
	return status.Errorf(codes.Unimplemented, "health check via Watch not implemented")
}

func (p *dbVideo) ListVideos(context.Context, *pb.Empty) (*pb.ListVideosResponse, error) {
	return &pb.ListVideosResponse{Video: parseVideo()}, nil
}

func (p *dbVideo) GetVideo(ctx context.Context, req *pb.GetVideoRequest) (*pb.Video, error) {
	var found *pb.Video
	for i := 0; i < len(parseVideo()); i++ {
		if req.VideoId == parseVideo()[i].Id {
			found = parseVideo()[i]
			break
		}
	}
	if found == nil {
		return nil, status.Errorf(codes.NotFound, "no video with ID %s", req.VideoId)
	}
	return found, nil
}

func (p *dbVideo) SearchVideos(ctx context.Context, req *pb.SearchVideosRequest) (*pb.SearchVideosResponse, error) {
	// Intepret query as a substring match in name or description.
	var ps []*pb.Video
	for _, p := range parseVideo() {
		if strings.Contains(strings.ToLower(p.Title), strings.ToLower(req.Query)) ||
			strings.Contains(strings.ToLower(p.Artist.Name), strings.ToLower(req.Query)) {
			ps = append(ps, p)
		}
	}
	return &pb.SearchVideosResponse{Results: ps}, nil
}

func (p *dbVideo) AddVideo(ctx context.Context, req *pb.AddVideoRequest) (*pb.AddVideoResponse, error) {
	data := parseVideo()
	videoID, err := uuid.NewUUID()
	if err != nil {
		return nil, status.Errorf(codes.Internal, "failed to generate order uuid")
	}
	req.Video.Id = videoID.String()
	data = append(data, req.Video)
	j, err := json.Marshal(data)
	if err != nil {
		return nil, status.Errorf(codes.Internal, "Error creating JSON Data")
	}
	err = ioutil.WriteFile("videos.json", j, 0644)
	if err != nil {
		return nil, status.Errorf(codes.Internal, "Error saving JSON Data")
	}
	return &pb.AddVideoResponse{VideoId: req.Video.Id}, nil
}
