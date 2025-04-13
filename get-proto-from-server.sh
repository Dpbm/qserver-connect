#!/bin/bash

if [ ! $(which curl) &>/dev/null ]; then
    echo "Installing curl...."
    sudo apt install curl
fi

echo "Getting proto file ..."
curl -L https://raw.githubusercontent.com/Dpbm/qserver/refs/heads/main/server/jobsServer/proto/jobs.proto -o ./qserver_connect/jobs.proto

echo "Generating proto files ..."
cd ./qserver_connect
python -m grpc_tools.protoc -I./ --python_out=. --pyi_out=. --grpc_python_out=. jobs.proto