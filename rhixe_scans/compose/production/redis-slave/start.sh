#!/bin/bash

redis-server /usr/src/app/redis-slave/redis.conf --slaveof ${REDIS_MASTER_SERVICE_HOST} ${REDIS_MASTER_SERVICE_PORT}
