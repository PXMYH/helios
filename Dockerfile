FROM python:2.7-alpine3.8
LABEL maintainer <Michael Hu>

ARG APP_DIR="/app/"
WORKDIR ${APP_DIR}
RUN mkdir -p "${APP_DIR}"
COPY requirements.txt .

# RUN apk update && apk add --update --no-cache g++ linux-headers libxslt-dev libxml2-dev libffi-dev postgresql-libs\
#   && apk add --virtual gcc python-dev musl-dev openssl-dev postgresql-devel\
#   && pip install --upgrade pip \
#   && pip install -r requirements.txt

RUN \
  apk add --no-cache postgresql-libs g++ linux-headers libxslt-dev libxml2-dev libffi-dev\
  && apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev \
  && pip install --upgrade pip \
  && pip install -r requirements.txt

COPY app.py ${APP_DIR}
COPY configs/ services/ swagger/ ${APP_DIR}

ENV POSTGRES_DB_URI "postgres://postgres@localhost:5432/helios"
CMD [ "python", "${APP_DIR}/app.py" ]

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "curl http://127.0.0.1:5000 || exit 1" ]
