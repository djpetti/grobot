#!/bin/bash

# Builds and runs tests inside a container for CI.

docker build -t grobot-testing -f containers/testing/Dockerfile .
docker run -v `pwd`:/grobot -w /grobot grobot-testing ./deploy.py -tc
