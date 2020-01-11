#!/usr/bin/env python

from concurrent import futures
import os
import json
import sys
import time
import uuid
import logging
import grpc
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc
from protobuf_to_dict import protobuf_to_dict, dict_to_protobuf

import app_pb2
import app_pb2_grpc

logger = logging.getLogger("songservice-client")
logger.setLevel(logging.DEBUG)
logHandler = logging.StreamHandler(sys.stdout)
logger.addHandler(logHandler)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data/{}.json")


def load_song_data(path):
    """ Load Sample JSON Data from `data` directory """
    with open(DATA_PATH.format(path), 'r')  as f:
        return json.load(f)

def get_artist(artist_id, data=None):
    if not data:
        data = load_song_data("artists")
    return data[artist_id]


class SongService(app_pb2_grpc.SongServiceServicer):
    ARTISTS_DB = "artists"
    ALBUM_DB = "albums"
    SONG_DB = "songs"

    def __init__(self):
        # A simple json database to contain song :)
        self.artist_db = load_song_data(self.ARTISTS_DB)
        self.album_db = load_song_data(self.ALBUM_DB)
        self.song_db = load_song_data(self.SONG_DB)

    def save(self, data, path):
        with open(DATA_PATH.format(path), 'w') as f:
            json.dump(data, f)

    def AddArtist(self, request, context):
        artist_id = str(uuid.uuid1())
        self.artist_db[artist_id] = protobuf_to_dict(request)
        self.save(self.artist_db, self.ARTISTS_DB)
        response = app_pb2.AddArtistResponse(artist_id=artist_id)
        return response

    def GetSong(self, request, context):
        # get song with id `request.song_id`
        try:
            song = self.song_db[request.song_id]
            artist = self.artist_db[song["artist_id"]]
            album = self.album_db[song["album_id"]]
            response_featured_artist = []

            for entry in song["featured_artists"]:
                response_featured_artist.append(self.artist_db[entry["artist_id"]])

            response_artist = app_pb2.Artist(**artist)
            response_album = app_pb2.Album(artist=response_artist, title=album["title"], date=album["date"])
            response = app_pb2.GetSongResponse(
                    title=song["title"],
                    track_number=song["track_number"], 
                    featured_artists=response_featured_artist, 
                    album=response_album) 
            return response
        except KeyError:
            context.set_details(f"Song with id {request.song_id} does not exist")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return app_pb2.GetSongResponse()

    def AddSong(self, request, context):
        song_id = str(uuid.uuid1())
        response = app_pb2.AddSongResponse(song_id=song_id)
        return response

    def Check(self, request, context):
        return health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.SERVING)

    def Watch(self, request, context):
        yield health_pb2.HealthCheckResponse(
            status=health_pb2.HealthCheckResponse.SERVING)

if __name__ == "__main__":
    logger.info("initializing SongService")
    port = os.environ.get("PORT", "8082")
    channel = grpc.insecure_channel("localhost:"+port)

    # create gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # add class to gRPC server
    service = SongService()
    app_pb2_grpc.add_SongServiceServicer_to_server(service, server)
    health_pb2_grpc.add_HealthServicer_to_server(service, server)

    # start server
    logger.info("listening on port: " + port)
    server.add_insecure_port("[::]:"+port)
    server.start()

    # keep alive
    try:
         while True:
            time.sleep(10000)
    except KeyboardInterrupt:
            server.stop(0)
