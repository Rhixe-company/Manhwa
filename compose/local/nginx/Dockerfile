FROM docker.io/nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/local/nginx/default.conf /etc/nginx/conf.d/default.conf

RUN useradd --user-group --create-home --shell /bin/bash bot

ENV HOME=/home/bot

RUN mkdir -p $HOME/app/staticfiles
RUN mkdir -p $HOME/app/media

RUN chown -R bot:bot $HOME/app/staticfiles
RUN chown -R bot:bot $HOME/app/media


CMD ["nginx", "-g", "daemon off;"]
