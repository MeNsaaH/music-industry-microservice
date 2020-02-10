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
	addr = "localhost:5050"
	conn, err := grpc.Dial(addr, grpc.WithInsecure())
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	client := pb.NewVideoServiceClient(conn)

	// Test Add New Video Service
	res, err := client.AddVideo(ctx, &pb.AddVideoRequest{ArtistId: "fd41b124-34d4-11ea-83a6-b1766580429c", Video: &pb.Video{Title: "Rumble in the Bronx", Date: "12-12-2010"}})
	if err != nil {
		log.Error(err)
	}
	log.Info(res)

	// Test Search Videoes
	res2, err := client.SearchVideos(ctx, &pb.SearchVideosRequest{Query: "hitch"})
	if err != nil {
		log.Error(err)
	}
	log.Info(res2)

	//  // Test Get Videos
	//  res1, err := client.GetVideo(ctx, &pb.GetVideoRequest{VideoId: "16997b72-361f-11ea-9f35-3c5282eed773"})
	//  if err != nil {
	//    log.Error(err)
	//  }
	//  log.Info(res1)

	//  // Test List Videos
	//  res, err := client.ListVideos(ctx, &pb.Empty{})
	//  if err != nil {
	//    log.Error(err)
	//  }
	//  log.Info(res)
}
