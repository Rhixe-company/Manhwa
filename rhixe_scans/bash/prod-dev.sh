#!/bin/bash

until docker-compose down --remove-orphans -t 0 -v; do
    echo "Stopping Containers"

done
# make clean
# clear

# # sudo rm -r volumes
sudo rm -r volumes
# # sudo chown -R $USER:$USER app
# sudo chown -R $USER:$USER .
# until docker-compose build --pull; do
#     echo "Building Images"
# done
# docker system prune --volumes -f
until docker-compose up -d -V; do
    echo "Starting Containers"
done
# clear
# make user-dev
clear
make log
