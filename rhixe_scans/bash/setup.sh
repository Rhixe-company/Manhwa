#!/bin/bash

sudo apt update
# sudo apt install curl python3-pip python3-venv cron pass gnupg2 micro htop postgresql-client-common -y &&
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list >/dev/null

sudo apt update
sudo apt-get install -y postgresql postgresql-contrib curl cron docker-ce docker-compose pass gnupg2 micro htop python3-pip python3-venv python3-dev
# sudo apt-get install -y docker-ce docker-compose
sudo apt install python3-pip python3-dev libffi-dev libssl-dev -y
sudo apt-get install libmagic1 -y
pip3 install docker-compose

sudo usermod -aG docker $USER
sudo su - $USER
