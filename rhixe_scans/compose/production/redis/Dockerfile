FROM docker.io/redis:latest
RUN mkdir -p /usr/src/app/redis
COPY ./compose/production/redis/redis.conf /usr/src/app/redis/redis.conf
COPY ./compose/production/redis/redis-slave.conf /usr/src/app/redis/redis-slave.conf
