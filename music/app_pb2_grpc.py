# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import app_pb2 as app__pb2


class SongServiceStub(object):
  """-----------------Song service-----------------

  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.AddArtist = channel.unary_unary(
        '/media.SongService/AddArtist',
        request_serializer=app__pb2.AddArtistRequest.SerializeToString,
        response_deserializer=app__pb2.AddArtistResponse.FromString,
        )
    self.GetArtist = channel.unary_unary(
        '/media.SongService/GetArtist',
        request_serializer=app__pb2.GetArtistRequest.SerializeToString,
        response_deserializer=app__pb2.Artist.FromString,
        )
    self.AddAlbum = channel.unary_unary(
        '/media.SongService/AddAlbum',
        request_serializer=app__pb2.AddAlbumRequest.SerializeToString,
        response_deserializer=app__pb2.AddAlbumResponse.FromString,
        )
    self.AddSong = channel.unary_unary(
        '/media.SongService/AddSong',
        request_serializer=app__pb2.AddSongRequest.SerializeToString,
        response_deserializer=app__pb2.AddSongResponse.FromString,
        )
    self.GetSong = channel.unary_unary(
        '/media.SongService/GetSong',
        request_serializer=app__pb2.GetSongRequest.SerializeToString,
        response_deserializer=app__pb2.Song.FromString,
        )
    self.GetSongs = channel.unary_stream(
        '/media.SongService/GetSongs',
        request_serializer=app__pb2.Empty.SerializeToString,
        response_deserializer=app__pb2.Song.FromString,
        )
    self.GetAlbums = channel.unary_stream(
        '/media.SongService/GetAlbums',
        request_serializer=app__pb2.Empty.SerializeToString,
        response_deserializer=app__pb2.Album.FromString,
        )
    self.GetArtists = channel.unary_stream(
        '/media.SongService/GetArtists',
        request_serializer=app__pb2.Empty.SerializeToString,
        response_deserializer=app__pb2.Artist.FromString,
        )
    self.RemoveSong = channel.unary_unary(
        '/media.SongService/RemoveSong',
        request_serializer=app__pb2.RemoveSongRequest.SerializeToString,
        response_deserializer=app__pb2.Empty.FromString,
        )


class SongServiceServicer(object):
  """-----------------Song service-----------------

  """

  def AddArtist(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetArtist(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AddAlbum(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AddSong(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetSong(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetSongs(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetAlbums(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetArtists(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RemoveSong(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_SongServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'AddArtist': grpc.unary_unary_rpc_method_handler(
          servicer.AddArtist,
          request_deserializer=app__pb2.AddArtistRequest.FromString,
          response_serializer=app__pb2.AddArtistResponse.SerializeToString,
      ),
      'GetArtist': grpc.unary_unary_rpc_method_handler(
          servicer.GetArtist,
          request_deserializer=app__pb2.GetArtistRequest.FromString,
          response_serializer=app__pb2.Artist.SerializeToString,
      ),
      'AddAlbum': grpc.unary_unary_rpc_method_handler(
          servicer.AddAlbum,
          request_deserializer=app__pb2.AddAlbumRequest.FromString,
          response_serializer=app__pb2.AddAlbumResponse.SerializeToString,
      ),
      'AddSong': grpc.unary_unary_rpc_method_handler(
          servicer.AddSong,
          request_deserializer=app__pb2.AddSongRequest.FromString,
          response_serializer=app__pb2.AddSongResponse.SerializeToString,
      ),
      'GetSong': grpc.unary_unary_rpc_method_handler(
          servicer.GetSong,
          request_deserializer=app__pb2.GetSongRequest.FromString,
          response_serializer=app__pb2.Song.SerializeToString,
      ),
      'GetSongs': grpc.unary_stream_rpc_method_handler(
          servicer.GetSongs,
          request_deserializer=app__pb2.Empty.FromString,
          response_serializer=app__pb2.Song.SerializeToString,
      ),
      'GetAlbums': grpc.unary_stream_rpc_method_handler(
          servicer.GetAlbums,
          request_deserializer=app__pb2.Empty.FromString,
          response_serializer=app__pb2.Album.SerializeToString,
      ),
      'GetArtists': grpc.unary_stream_rpc_method_handler(
          servicer.GetArtists,
          request_deserializer=app__pb2.Empty.FromString,
          response_serializer=app__pb2.Artist.SerializeToString,
      ),
      'RemoveSong': grpc.unary_unary_rpc_method_handler(
          servicer.RemoveSong,
          request_deserializer=app__pb2.RemoveSongRequest.FromString,
          response_serializer=app__pb2.Empty.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'media.SongService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class VideoServiceStub(object):
  """---------------Video service----------

  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.ListVideos = channel.unary_unary(
        '/media.VideoService/ListVideos',
        request_serializer=app__pb2.Empty.SerializeToString,
        response_deserializer=app__pb2.ListVideosResponse.FromString,
        )
    self.GetVideo = channel.unary_unary(
        '/media.VideoService/GetVideo',
        request_serializer=app__pb2.GetVideoRequest.SerializeToString,
        response_deserializer=app__pb2.Video.FromString,
        )
    self.AddVideo = channel.unary_unary(
        '/media.VideoService/AddVideo',
        request_serializer=app__pb2.AddVideoRequest.SerializeToString,
        response_deserializer=app__pb2.AddVideoResponse.FromString,
        )
    self.SearchVideos = channel.unary_unary(
        '/media.VideoService/SearchVideos',
        request_serializer=app__pb2.SearchVideosRequest.SerializeToString,
        response_deserializer=app__pb2.SearchVideosResponse.FromString,
        )


class VideoServiceServicer(object):
  """---------------Video service----------

  """

  def ListVideos(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetVideo(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AddVideo(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SearchVideos(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_VideoServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'ListVideos': grpc.unary_unary_rpc_method_handler(
          servicer.ListVideos,
          request_deserializer=app__pb2.Empty.FromString,
          response_serializer=app__pb2.ListVideosResponse.SerializeToString,
      ),
      'GetVideo': grpc.unary_unary_rpc_method_handler(
          servicer.GetVideo,
          request_deserializer=app__pb2.GetVideoRequest.FromString,
          response_serializer=app__pb2.Video.SerializeToString,
      ),
      'AddVideo': grpc.unary_unary_rpc_method_handler(
          servicer.AddVideo,
          request_deserializer=app__pb2.AddVideoRequest.FromString,
          response_serializer=app__pb2.AddVideoResponse.SerializeToString,
      ),
      'SearchVideos': grpc.unary_unary_rpc_method_handler(
          servicer.SearchVideos,
          request_deserializer=app__pb2.SearchVideosRequest.FromString,
          response_serializer=app__pb2.SearchVideosResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'media.VideoService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class EmailServiceStub(object):
  """-------------Email service-----------------

  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.SendConfirmation = channel.unary_unary(
        '/media.EmailService/SendConfirmation',
        request_serializer=app__pb2.SendConfirmationRequest.SerializeToString,
        response_deserializer=app__pb2.Empty.FromString,
        )


class EmailServiceServicer(object):
  """-------------Email service-----------------

  """

  def SendConfirmation(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_EmailServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'SendConfirmation': grpc.unary_unary_rpc_method_handler(
          servicer.SendConfirmation,
          request_deserializer=app__pb2.SendConfirmationRequest.FromString,
          response_serializer=app__pb2.Empty.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'media.EmailService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
