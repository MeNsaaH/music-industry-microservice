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
    self.AddSong = channel.unary_unary(
        '/media.SongService/AddSong',
        request_serializer=app__pb2.AddSongRequest.SerializeToString,
        response_deserializer=app__pb2.AddSongResponse.FromString,
        )
    self.GetSong = channel.unary_unary(
        '/media.SongService/GetSong',
        request_serializer=app__pb2.GetSongRequest.SerializeToString,
        response_deserializer=app__pb2.GetSongResponse.FromString,
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
      'AddSong': grpc.unary_unary_rpc_method_handler(
          servicer.AddSong,
          request_deserializer=app__pb2.AddSongRequest.FromString,
          response_serializer=app__pb2.AddSongResponse.SerializeToString,
      ),
      'GetSong': grpc.unary_unary_rpc_method_handler(
          servicer.GetSong,
          request_deserializer=app__pb2.GetSongRequest.FromString,
          response_serializer=app__pb2.GetSongResponse.SerializeToString,
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
        response_deserializer=app__pb2.ListVideoResponse.FromString,
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


def add_VideoServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'ListVideos': grpc.unary_unary_rpc_method_handler(
          servicer.ListVideos,
          request_deserializer=app__pb2.Empty.FromString,
          response_serializer=app__pb2.ListVideoResponse.SerializeToString,
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
