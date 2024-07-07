#!/bin/bash

docker compose -f docker-compose.local.yml down --remove-orphans -t 0 -v
# make clean

# sudo rm -r static volumes
# sudo chown -R $USER:$USER .
docker compose -f docker-compose.local.yml build --pull

docker compose -f docker-compose.local.yml up -d -V

docker compose -f docker-compose.local.yml logs -f
