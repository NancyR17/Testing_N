#!/bin/sh

# Variables for Image Name and Tag
IMAGE_NAME="acrbtsaasdev.azurecr.io/capacity-iq/capacity-iq-ui"
TAG="${bamboo.buildNumber}"
CONTEXT_PATH="capacity-iq-ui"

# --- EDITED BUILD COMMAND (with Dockerfile Content) ---
# The Multi-Stage Dockerfile content is passed via pipe (|) to 'docker build -f -'.
echo '
FROM node:22-alpine AS node
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
FROM nginx:1.25.1-alpine
COPY --from=node /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
' | docker build -t "${IMAGE_NAME}:${TAG}" -f - "${CONTEXT_PATH}"

# --- ORIGINAL PUSH COMMAND ---
docker push "${IMAGE_NAME}:${TAG}"
