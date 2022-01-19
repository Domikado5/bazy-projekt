FROM node:lts-alpine

WORKDIR /vue_app

COPY ./vue_app .

ENV PATH /vue_app/node_modules/.bin:$PATH

RUN npm install
RUN npm install @vue/cli -g

CMD ["npm", "run", "serve"]