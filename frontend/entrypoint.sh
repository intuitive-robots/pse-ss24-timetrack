#!/bin/bash

# Replace environment variables in nginx.conf.template and save to nginx.conf
envsubst '${BACKEND_URL}' /etc/nginx/nginx.conf /etc/nginx/nginx.conf

# Start Nginx
exec nginx -g 'daemon off;'