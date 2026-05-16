#!/bin/sh
set -eu

MODE="${LB_MODE:-active-active}"

case "$MODE" in
  active-active)
    cp /etc/nginx/templates/nginx.active-active.conf /etc/nginx/nginx.conf
    ;;
  active-passive)
    cp /etc/nginx/templates/nginx.active-passive.conf /etc/nginx/nginx.conf
    ;;
  *)
    echo "Unknown LB_MODE=$MODE"
    exit 1
    ;;
esac

exec nginx -g 'daemon off;'