FROM crystalnix/omaha-server-base:alpine

ADD . $omaha

# setup all the configfiles
RUN \
    mkdir /etc/nginx/sites-enabled/ && \
    mkdir /var/log/supervisor/ && \
    rm /etc/nginx/nginx.conf && \
    ln -s /srv/omaha/conf/nginx.conf /etc/nginx/ && \
    ln -s /srv/omaha/conf/nginx-app.conf /etc/nginx/sites-enabled/ && \
    ln -sfn /srv/omaha/conf/supervisord.conf /etc/

EXPOSE 80
CMD ["paver", "docker_run"]
