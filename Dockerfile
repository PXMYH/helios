FROM python:2.7-alpine3.8
LABEL maintainer Michael Hu

RUN apk --update --no-cache add gcc g++ linux-headers libxslt-dev libxml2-dev libffi-dev openssl-dev
RUN pip install --upgrade pip scrapy

WORKDIR /
COPY craigslist /
COPY src /

CMD [ "python", "main.py" ]
