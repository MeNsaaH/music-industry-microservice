package main

import (
	"context"
	"os"
	"time"

	pb "github.com/mensaah/music-industry-microservice/genproto"

	"github.com/sirupsen/logrus"
	"google.golang.org/grpc"
)

var (
	cat  pb.ListVideosResponse
	log  *logrus.Logger
	addr string
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
}

func main() {
	ctx := context.Background()
	addr = "localhost:8003"
	conn, err := grpc.Dial(addr, grpc.WithInsecure())
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	client := pb.NewVideoServiceClient(conn)
	res, err := client.AddVideo(ctx, &pb.AddVideoRequest{ArtistId: "somethings", Video: &pb.Video{Title: "Things Fall Apart", Date: "12-12-2010"}})
	if err != nil {
		log.Fatal(err)
	}
	log.Info(res)
}
