# frontend/Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY . .

RUN npm install
RUN npm run build --prod

# ---- NGINX STAGE ----
FROM nginx:alpine
COPY --from=builder /app/dist/stock-frontend/browser /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
