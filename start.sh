#!/bin/bash

docker-compose down

sudo rm -rf volume

docker-compose up --build