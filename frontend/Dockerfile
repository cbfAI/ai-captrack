FROM node:20-alpine

WORKDIR /app

COPY frontend/package*.json ./
RUN npm ci --legacy-peer-deps

COPY frontend/ .

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--host"]
