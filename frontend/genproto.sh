#!/bin/bash -e

python -m grpc_tools.protoc -I../pb --python_out=./app/ --grpc_python_out=./app/ ../pb/app.proto
