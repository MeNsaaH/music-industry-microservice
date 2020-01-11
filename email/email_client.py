#!/usr/bin/env python

import grpc
import sys

import app_pb2
import app_pb2_grpc

import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger('emailservice-client')
logger.setLevel(logging.INFO)

formatter = jsonlogger.JsonFormatter()
logHandler = logging.StreamHandler(sys.stdout)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


def send_confirmation_email(email, message):
  channel = grpc.insecure_channel('0.0.0.0:8081')
  stub = app_pb2_grpc.EmailServiceStub(channel)
  try:
    response = stub.SendConfirmation(app_pb2.SendConfirmationRequest(
      email = email,
      message = message 
    ))
    logger.info('Request sent.')
  except grpc.RpcError as err:
    logger.error(err.details())
    logger.error('{}, {}'.format(err.code().name, err.code().value))

if __name__ == '__main__':
  logger.info('Client for email service.')
  send_confirmation_email("mmadumanasseh@gmail.com", "This is a confirmation")
