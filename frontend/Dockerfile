# Build the React app, then serve the static files with nginx.
FROM node:20-alpine AS build
WORKDIR /app

COPY package.json pnpm-lock.yaml ./
# Install the exact pnpm version pinned in package.json's "packageManager"
# (an unpinned pnpm ignores our build-script settings and fails the install).
RUN npm install -g "$(node -p "require('./package.json').packageManager")" \
    && pnpm install --frozen-lockfile

COPY . .
# Baked in at build time (Vite inlines env vars into the bundle)
ARG VITE_API_URL=http://localhost:8000/api/v1
ENV VITE_API_URL=$VITE_API_URL
RUN pnpm build

FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
