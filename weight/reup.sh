#! /bin/bash

docker-compose -f docker-compose-mockups.yml build --no-cache weight_be
docker-compose -f docker-compose-mockups.yml up