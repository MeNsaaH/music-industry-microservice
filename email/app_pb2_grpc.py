# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import app_pb2 as app__pb2


class MusicServiceStub(object):
  """-----------------Music service-----------------

  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.AddArtist = channel.unary_unary(
        '/media.MusicService/AddArtist',
        request_serializer=app__pb2.AddArtistRequest.SerializeToString,
        response_deserializer=app__pb2.AddArtistResponse.FromString,
        )
    self.AddMusic = channel.unary_unary(
        '/media.MusicService/AddMusic',
        request_serializer=app__pb2.AddMusicRequest.SerializeToString,
        response_deserializer=app__pb2.AddMusicResponse.FromString,
        )
    self.GetMusic = channel.unary_unary(
        '/media.MusicService/GetMusic',
        request_serializer=app__pb2.GetMusicRequest.SerializeToString,
        response_deserializer=app__pb2.GetMusicResponse.FromString,
        )
    self.RemoveMusic = channel.unary_unary(
        '/media.MusicService/RemoveMusic',
        request_serializer=app__pb2.RemoveMusicRequest.SerializeToString,
        response_deserializer=app__pb2.Empty.FromString,
        )


class MusicServiceServicer(object):
  """-----------------Music service-----------------

  """

  def AddArtist(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def AddMusic(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetMusic(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RemoveMusic(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_MusicServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'AddArtist': grpc.unary_unary_rpc_method_handler(
          servicer.AddArtist,
          request_deserializer=app__pb2.AddArtistRequest.FromString,
          response_serializer=app__pb2.AddArtistResponse.SerializeToString,
      ),
      'AddMusic': grpc.unary_unary_rpc_method_handler(
          servicer.AddMusic,
          request_deserializer=app__pb2.AddMusicRequest.FromString,
          response_serializer=app__pb2.AddMusicResponse.SerializeToString,
      ),
      'GetMusic': grpc.unary_unary_rpc_method_handler(
          servicer.GetMusic,
          request_deserializer=app__pb2.GetMusicRequest.FromString,
          response_serializer=app__pb2.GetMusicResponse.SerializeToString,
      ),
      'RemoveMusic': grpc.unary_unary_rpc_method_handler(
          servicer.RemoveMusic,
          request_deserializer=app__pb2.RemoveMusicRequest.FromString,
          response_serializer=app__pb2.Empty.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'media.MusicService', rpc_method_handlers)
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
