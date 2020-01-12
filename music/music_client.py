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
  artist = {"name":"Handanovic Sooks", "stage_name":"shan", "age":23} 
  album = {"title":"Funny Album", "date":"14-14-2019"}
  song = {"title":"Geekdom", "track_number":3, "featured_artists_ids":["89979b90-34e2-11ea-83a6-b1766580429c"]}

  # Test Add Artist
#   request = app_pb2.AddArtistRequest(**artist)
#   # make call to server
#   response = stub.AddArtist(request)
#   logger.info(response)

#   # Test GetSong
#   request = app_pb2.GetSongRequest(song_id="01fdbf04-34c2-11ea-83a6-b1766580429c")
#   response = stub.GetSong(request)
#   logger.info(response)

#   # Test Add Song
#   artist = app_pb2.Artist(**artist)
#   album = app_pb2.Album(artist=artist, **album)
#   request = app_pb2.AddSongRequest(**song, artist_id="fd41b124-34d4-11ea-83a6-b1766580429c")
#   # make call to server
#   response = stub.AddSong(request)
#   logger.info(response)

  # Test Get Songs
  request = app_pb2.Empty()
  response = stub.GetSongs(request)
  for song in response:
      logger.info(song)
