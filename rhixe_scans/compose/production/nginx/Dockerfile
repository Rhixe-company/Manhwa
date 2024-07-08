FROM docker.io/nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/production/nginx/default.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /app/static
RUN mkdir -p /app/media
