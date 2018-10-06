FROM nginx:1.14-alpine
MAINTAINER Martin Dulin <martin@dulin.me.uk>

RUN apk add --no-cache --update openssl
RUN mkdir /cert

COPY ./entrypoint.sh ./openssl.cnf /
COPY nginx.conf.template /

RUN rm -f /etc/nginx/nginx.conf

ENTRYPOINT ["/entrypoint.sh"]

CMD ["nginx", "-g", "daemon off;"]
