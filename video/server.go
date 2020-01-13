package main

import (
	"bytes"
	"context"
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

type dbVideo struct {
	musicSvcAddr string
}

type dbStruct struct {
	videos []*pb.Video
}

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
	svc.musicSvcAddr = "localhost:8082"
	pb.RegisterVideoServiceServer(srv, svc)
	healthpb.RegisterHealthServer(srv, svc)
	go srv.Serve(l)
	return l.Addr().String()
}

func loadDB(videos *pb.ListVideosResponse) error {
	videoMutex.Lock()
	defer videoMutex.Unlock()
	videoJSON, err := ioutil.ReadFile("videos.json")
	if err != nil {
		log.Fatalf("failed to open video json file: %v", err)
		return err
	}
	if err := jsonpb.Unmarshal(bytes.NewReader(videoJSON), videos); err != nil {
		log.Warnf("failed to parse the video JSON: %v", err)
		return err
	}
	log.Info("successfully parsed product video json")
	return nil
}

func parseVideo() []*pb.Video {
	if reloadVideo || len(cat.Videos) == 0 {
		err := loadDB(&cat)
		if err != nil {
			return []*pb.Video{}
		}
	}
	reloadVideo = false
	return cat.Videos
}

func (p *dbVideo) Check(ctx context.Context, req *healthpb.HealthCheckRequest) (*healthpb.HealthCheckResponse, error) {
	return &healthpb.HealthCheckResponse{Status: healthpb.HealthCheckResponse_SERVING}, nil
}

func (p *dbVideo) Watch(req *healthpb.HealthCheckRequest, ws healthpb.Health_WatchServer) error {
	return status.Errorf(codes.Unimplemented, "health check via Watch not implemented")
}

func (p *dbVideo) ListVideos(context.Context, *pb.Empty) (*pb.ListVideosResponse, error) {
	return &pb.ListVideosResponse{Videos: parseVideo()}, nil
}

func (p *dbVideo) getArtist(ctx context.Context, artistID string) (*pb.Artist, codes.Code, error) {
	conn, err := grpc.DialContext(ctx, p.musicSvcAddr, grpc.WithInsecure())
	if err != nil {
		return nil, codes.Internal, fmt.Errorf("could not connect Music service: %+v", err)
	}
	defer conn.Close()
	artist, err := pb.NewSongServiceClient(conn).GetArtist(ctx, &pb.GetArtistRequest{ArtistId: artistID})
	if err != nil {
		return nil, codes.NotFound, fmt.Errorf("failed to Check Artist Info: %+v", err)
	}
	return artist, codes.OK, nil
}

func (p *dbVideo) GetVideo(ctx context.Context, req *pb.GetVideoRequest) (*pb.Video, error) {
	var found *pb.Video
	for i := 0; i < len(parseVideo()); i++ {
		if req.VideoId == parseVideo()[i].Id {
			found = parseVideo()[i]
			break
		}
	}
	artist, statusCode, err := p.getArtist(ctx, found.Artist.Id)
	if err != nil {
		return nil, status.Errorf(statusCode, "no video with ID %s", req.VideoId)
	}
	found.Artist = artist
	if found == nil {
		return nil, status.Errorf(codes.NotFound, "no video with ID %s", req.VideoId)
	}
	return found, nil
}

func (p *dbVideo) SearchVideos(ctx context.Context, req *pb.SearchVideosRequest) (*pb.SearchVideosResponse, error) {
	// Intepret query as a substring match in name or description.
	var ps []*pb.Video
	for _, video := range parseVideo() {
		if strings.Contains(strings.ToLower(video.Title), strings.ToLower(req.Query)) {
			artist, statusCode, err := p.getArtist(ctx, video.Artist.Id)
			if err != nil {
				return nil, status.Errorf(statusCode, "%v", err)
			}
			video.Artist = artist
			ps = append(ps, video)
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
	_, statusCode, err := p.getArtist(ctx, req.ArtistId)
	if err != nil {
		return nil, status.Errorf(statusCode, "could not connect Music service: %+v", err)
	}
	req.Video.Id = videoID.String()
	req.Video.Artist = &pb.Artist{Id: req.ArtistId}
	data = append(data, req.Video)

	jsonData, err := new(jsonpb.Marshaler).MarshalToString(&pb.ListVideosResponse{Videos: data})
	if err != nil {
		log.Fatalf("marshaling error: %v", err)
	}

	err = ioutil.WriteFile("videos.json", []byte(jsonData), 0644)
	if err != nil {
		return nil, status.Errorf(codes.Internal, "Error saving JSON Data")
	}
	reloadVideo = true
	return &pb.AddVideoResponse{VideoId: req.Video.Id}, nil
}
