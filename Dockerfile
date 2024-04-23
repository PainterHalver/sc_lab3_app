# Build static React app
FROM node:18.20.2-alpine AS build
WORKDIR /app
COPY ./client/package.json ./client/package-lock.json ./
RUN npm install
COPY ./client ./
RUN npm run build

FROM python:3.9.18-alpine
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN apk add --no-cache curl && \
    pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
COPY --from=build /app/build ./client/build
RUN chmod +x start.sh
CMD ["./start.sh"]