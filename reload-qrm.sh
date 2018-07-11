#!/bin/bash

git pull
docker stop qrmbot
docker rm qrmbot
docker build -t qrmbot .
docker run -d --rm --name qrmbot qrmbot
