FROM nginx:1.27-alpine

COPY nginx.active-active.conf /etc/nginx/templates/nginx.active-active.conf
COPY nginx.active-passive.conf /etc/nginx/templates/nginx.active-passive.conf
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]