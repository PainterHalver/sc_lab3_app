# Build static React app
FROM node:18.20.2-alpine as build
WORKDIR /app
COPY ./client/package.json ./client/package-lock.json ./
RUN npm install
COPY ./client ./
RUN npm run build

FROM python:3.9.18-alpine
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
COPY --from=build /app/build ./client/build
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:create_app()"]