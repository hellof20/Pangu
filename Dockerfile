FROM python:3.7-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN apk add terraform
RUN apk add mysql-client
RUN apk add git
RUN apk add jq
RUN apk add mariadb-connector-c-dev
CMD ["python", "main.py"]