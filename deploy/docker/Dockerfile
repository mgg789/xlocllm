FROM node:24-alpine AS build
WORKDIR /app
COPY package.json pnpm-workspace.yaml ./
COPY pnpm-lock.yaml ./
COPY apps/web/package.json apps/web/package.json
RUN corepack enable && pnpm install --filter @xlocllm/web --prod=false --frozen-lockfile=false
COPY apps apps
COPY packages packages
RUN pnpm --filter @xlocllm/web build

FROM nginx:1.27-alpine
COPY deploy/docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/apps/web/dist /usr/share/nginx/html
EXPOSE 8080
