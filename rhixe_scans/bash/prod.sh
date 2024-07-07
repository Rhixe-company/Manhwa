#!/bin/bash

docker compose -f docker-compose.production.yml down --remove-orphans -t 0 -v
# make clean

# sudo rm -r static volumes
# sudo chown -R $USER:$USER .
docker compose -f docker-compose.production.yml build --pull

docker compose -f docker-compose.production.yml up -d -V

docker compose -f docker-compose.production.yml logs -f
