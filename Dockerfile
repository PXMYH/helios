FROM python:2.7-alpine3.8
LABEL maintainer Michael Hu

RUN apk --update --no-cache add gcc g++ linux-headers libxslt-dev libxml2-dev libffi-dev openssl-dev
RUN pip install --upgrade pip scrapy

WORKDIR /opt
COPY craigslist /opt
COPY src /opt

# TODO: add health check to container

CMD [ "python", "/opt/src/main.py" ]
