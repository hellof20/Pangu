FROM python:3.7-alpine
ADD static /app/static
ADD templates /app/templates
ADD requirements.txt /app/
ADD apply.sh destroy.sh upgrade.sh /app/
ADD main.py sql.py /app/
WORKDIR /app
RUN pip install -r requirements.txt
RUN apk add terraform
RUN apk add mysql-client
RUN apk add mariadb-connector-c-dev
RUN apk add jq curl git
RUN apk add --no-cache --upgrade bash
RUN curl -sSL https://sdk.cloud.google.com | bash
ENV PATH $PATH:/root/google-cloud-sdk/bin
CMD ["python", "main.py"]