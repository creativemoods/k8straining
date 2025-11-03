# Builder Dockerfile
FROM node:18.17-alpine AS studentx_frontend_builder

WORKDIR /app

COPY --chown=node ["package.json", "package-lock.json*", "./"]
# https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3#nodealpine
RUN apk add --no-cache libc6-compat && \
  npm ci --production

COPY --chown=node src ./src/
COPY --chown=node public ./public/

RUN mkdir ./.next && \
  chown node: ./.next && \
  chown -R node: .

USER node

ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=$REACT_APP_API_URL
RUN npm run build

# Runner Dockerfile
FROM node:18.17-alpine AS studentx_frontend_runner

RUN npm install -g serve

WORKDIR /app
USER node

COPY --from=studentx_frontend_builder --chown=node /app/build ./build

EXPOSE 3000
CMD ["serve", "-s", "build", "-l", "3000"]
