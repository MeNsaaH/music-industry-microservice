#!/usr/bin/env python

import grpc
import sys

import app_pb2
import app_pb2_grpc

import logging

logger = logging.getLogger("songService-client")
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler(sys.stdout)
logger.addHandler(logHandler)


if __name__ == "__main__":
  logger.info("Client for Song service.")
  # set up server stub
  channel = grpc.insecure_channel("localhost:8082")
  stub = app_pb2_grpc.SongServiceStub(channel)
  artist = {"name":"Ernesto Valverede", "stage_name":"ernesto", "age":23} 
  album = {"title":"Funny Album", "date":"14-14-2019"}
  song = {"title":"Something Awful", "track_number":3}

#   # Test Add Artist
#   request = app_pb2.AddArtistRequest(**artist)
#   # make call to server
#   response = stub.AddArtist(request)
#   logger.info(response)

#   # Test GetSong
#   request = app_pb2.GetSongRequest(song_id="01fdbf04-34c2-11ea-83a6-b1766580429c")
#   response = stub.GetSong(request)
#   logger.info(response)

  # Test Add Song
  artist = app_pb2.Artist(**artist)
  album = app_pb2.Album(artist=artist, **album)
  request = app_pb2.AddSongRequest(**song, album_id="2846d408-34c1-11ea-83a6-b1766580429c")
  # make call to server
  response = stub.AddSong(request)
  logger.info(response)
