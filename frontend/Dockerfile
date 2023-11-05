FROM node:16.16-slim

WORKDIR /src
COPY /src .

RUN npm ci
CMD ./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
