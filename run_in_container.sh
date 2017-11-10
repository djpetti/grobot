#!/bin/bash

# Runs the dev server inside a container.

docker build -t grobot-testing -f containers/testing/Dockerfile .
docker run -v `pwd`:/grobot -v /dev/shm:/dev/shm --net=host -w /grobot grobot-testing ./deploy.py $@
