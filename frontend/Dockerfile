FROM node:16.16-slim

RUN apt-get update \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src
COPY /src .

RUN npm ci
CMD ./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
