#!/usr/bin/env bash
docker build -t bsmali4/hunter-consumer:2.0 ./hunter-consumer/ -f ./hunter-consumer/Dockerfile
docker build -t bsmali4/hunter-admin-api:2.0 ./hunter-admin-api/ -f ./hunter-admin-api/Dockerfile
docker build -t bsmali4/hunter-admin-gui:2.0 ./hunter-admin-gui/ -f ./hunter-admin-gui/Dockerfile
docker build -t bsmali4/hunter-sense:2.0 ./hunter-sense/ -f ./hunter-sense/Dockerfile
docker build -t bsmali4/hunter-redis:2.0 ./redis/ -f ./redis/Dockerfile
docker build -t bsmali4/hunter-mysql:2.0 ./mysql/ -f ./mysql/Dockerfile
docker build -t bsmali4/hunter-rabbitmq:2.0 ./rabbitmq/ -f ./rabbitmq/Dockerfile