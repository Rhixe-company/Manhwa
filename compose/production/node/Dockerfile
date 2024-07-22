FROM docker.io/node:22.5-bookworm-slim

RUN useradd --user-group --create-home --shell /bin/false bot &&\
    npm install --global npm@latest

ENV HOME=/home/bot

USER bot

COPY --chown=bot:bot ./package.json $HOME/app/

RUN chown -R bot:bot $HOME/*



WORKDIR $HOME/app



RUN npm install && npm cache clean --force

ENV PATH ./node_modules/.bin/:$PATH

