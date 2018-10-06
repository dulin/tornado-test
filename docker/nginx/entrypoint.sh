#!/bin/sh

CRT_YEARS=4
CRT="/cert/ssl.crt"
KEY="/cert/ssl.key"

export NETWORK=$(ip route | tail -1 | cut -d' ' -f1) || true

if [ -e ${CRT} ] && [ -e ${KEY} ]; then
    echo "Using existing cert"
else
    echo "Generate cert"
    export SAN="IP:${CERT_IP},DNS:${CERT_IP}"
    openssl req -nodes -x509 -newkey rsa:4096 -subj "/CN=${CERT_IP}" -keyout "/cert/ssl.key" -out ${CRT}  -days "`expr ${CRT_YEARS} \* 365`" -batch -config "/openssl.cnf"
fi

if [ ! -e "/etc/nginx/nginx.conf" ]; then
    envsubst '${NETWORK}' < "/nginx.conf.template" > "/etc/nginx/nginx.conf"
fi

exec "$@"