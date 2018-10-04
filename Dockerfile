FROM python:3.7.0-alpine3.7
MAINTAINER Martin Dulin <martin@dulin.me.uk>

RUN apk add --no-cache libpq
RUN apk add --no-cache -t .build-deps postgresql-dev gcc libc-dev

EXPOSE 8080
RUN mkdir /tmp/build
WORKDIR /tmp/build
COPY . .
RUN pip install --no-cache-dir .

RUN apk del .build-deps
RUN rm -fr /tmp/build
ENTRYPOINT ["playground"]