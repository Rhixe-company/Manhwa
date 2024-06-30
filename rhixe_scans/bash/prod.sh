#!/bin/bash

until docker-compose -f docker-compose-prod.yaml down --remove-orphans -t 0 -v; do
    echo "Stopping Containers"

done

make clean

sudo rm -r static volumes
sudo chown -R $USER:$USER .
until docker-compose -f docker-compose-prod.yaml build --pull; do
    echo "Building Images"
done

until docker-compose -f docker-compose-prod.yaml up -d -V; do
    echo "Starting Containers"
done
clear
make user
clear
make debug
