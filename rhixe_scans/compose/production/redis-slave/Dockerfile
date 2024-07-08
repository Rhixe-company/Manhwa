FROM docker.io/redis:latest

ENV REDIS_MASTER_SERVICE_HOST redis
ENV REDIS_MASTER_SERVICE_PORT 6379

RUN mkdir -p /usr/src/app/redis-slave

COPY ./compose/production/redis-slave/redis.conf /usr/src/app/redis-slave/redis.conf
COPY ./compose/production/redis-slave/start.sh /start.sh

RUN chmod a+x /start.sh

CMD [ "/start.sh"]
