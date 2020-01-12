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
    if os.path.isfile(DATA_PATH.format(path)):
        with open(DATA_PATH.format(path), 'r') as f:
            return json.load(f)
    SongService.save({}, path)
    return {}


def get_artist(artist_id, data=None):
    if not data:
        data = load_song_data("artists")
    return data[artist_id]


class SongService(app_pb2_grpc.SongServiceServicer):
    ARTISTS_DB = "artists"
    ALBUM_DB = "albums"
    SONG_DB = "songs"

    def __init__(self):
        # A simple json database to contain music data:)
        self.artist_db = load_song_data(self.ARTISTS_DB)
        self.album_db = load_song_data(self.ALBUM_DB)
        self.song_db = load_song_data(self.SONG_DB)

    @staticmethod
    def save(data, path):
        with open(DATA_PATH.format(path), 'w') as f:
            json.dump(data, f)

    def AddArtist(self, request, context):
        artist_id = str(uuid.uuid1())
        self.artist_db[artist_id] = protobuf_to_dict(request)
        SongService.save(self.artist_db, self.ARTISTS_DB)
        response = app_pb2.AddArtistResponse(artist_id=artist_id)
        return response

    def GetArtists(self, request, context):
        for artist_id, artist in self.artist_db.items():
            response = {
                "artist_id": artist_id,
                "name": artist["name"],
                "stage_name": artist["stage_name"],
                "age": artist["age"],
            }

            yield app_pb2.GetArtistResponse(**response)

    def AddAlbum(self, request, context):
        album_id = str(uuid.uuid1())
        if request.artist_id not in self.artist_db:
            context.set_details(f"Artist with id `{request.artist_id}` does not exist")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return app_pb2.GetSongResponse()

        self.album_db[album_id] = protobuf_to_dict(request)
        SongService.save(self.album_db, self.ALBUM_DB)
        response = app_pb2.AddAlbumResponse(album_id=album_id)
        return response

    def GetAlbums(self, request, context):
        for album_id, album in self.album_db.items():
            response = {
                "album_id": album_id,
                "title": album["title"],
                "artist_id": album["artist_id"],
                "date": album["date"],
            }

            yield app_pb2.GetAlbumResponse(**response)

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

    def GetSongs(self, request, context):
        for song_id, song in self.song_db.items():
            response = {
                "featured_artists": [],
                "title": song["title"],
                "album": None,
                "artist": None,
                "track_number": None,
            }
            if "artist_id" in song.keys():
                artist = self.artist_db[song["artist_id"]]
                response["artist"]= app_pb2.Artist(**artist)

            if "album_id" in song.keys():
                album = self.album_db[song["album_id"]]
                response["album"]= app_pb2.Album(
                        artist=app_pb2.Artist(**self.artist_db[album["artist_id"]]),
                        title=album["title"], date=album["date"])
                response["track_number"] = song["track_number"]

            if "featured_artists_ids" in song.keys():
                for feat_artist_id in song["featured_artists_ids"]:
                    response["featured_artists"].append(
                            app_pb2.Artist(**self.artist_db[feat_artist_id]))

            yield app_pb2.GetSongResponse(
                    **{k:response[k] for i, k in enumerate(response.keys()) if response[k] is not None})

    def AddSong(self, request, context):
        song_id = str(uuid.uuid1())
        if request.album_id:
            if request.album_id not in self.album_db.keys():
                context.set_details(f"Album {request.album_id} does not exist")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return app_pb2.AddSongResponse()
            if not request.track_number:
                context.set_details("Song must have a track number if Album parameter is set")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return app_pb2.AddSongResponse()

        if not request.album_id and not request.artist_id:
            context.set_details("artist_id or album_id parameter must be specified")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return app_pb2.GetSongResponse()

        if request.artist_id and request.artist_id not in self.artist_db:
            context.set_details(f"Artist {request.artist_id} does not exist")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return app_pb2.GetSongResponse()

        for artist_id in request.featured_artists_ids:
            if artist_id not in self.artist_db:
                context.set_details(f"Featured Artist {artist_id} does not exist")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return app_pb2.GetSongResponse()

        self.song_db[song_id] = protobuf_to_dict(request)
        SongService.save(self.song_db, self.SONG_DB)
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
