# Clisonix Industrial Frontend Docker Image
FROM node:18-alpine AS base

WORKDIR /app

COPY package*.json ./

RUN npm ci --omit=dev --legacy-peer-deps

FROM base AS development
RUN npm ci
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]

FROM base AS build
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine AS production
RUN addgroup -g 1001 -S nodejs
RUN adduser -S Clisonix -u 1001
WORKDIR /app
COPY --from=build --chown=Clisonix:nodejs /app/.next ./.next
COPY --from=build --chown=Clisonix:nodejs /app/node_modules ./node_modules
COPY --from=build --chown=Clisonix:nodejs /app/package*.json ./
USER Clisonix
EXPOSE 3000
ENV NODE_ENV=production
ENV PORT=3000
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:3000 || exit 1
CMD ["npm", "start"]
