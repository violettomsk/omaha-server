FROM alpine:edge

ENV omaha /srv/omaha

RUN apk --update add bash ca-certificates && \
    apk --update add nginx python supervisor uwsgi uwsgi-python py-pip && \
    apk --update add --virtual dev-deps python-dev build-base && \
    apk --update add py-lxml py-psycopg2 py-pillow && \
    apk --update add fuse-dev libxml2-dev libcurl curl-dev libstdc++ && \
    apk --update add --virtual fuse-deps autoconf automake libtool pkgconfig openssl-dev wget tar && \

    # Setup s3fs
    mkdir /usr/src && \
    wget --no-check-certificate https://github.com/s3fs-fuse/s3fs-fuse/archive/v1.78.tar.gz -O /usr/src/v1.78.tar.gz && \
    tar xvz -C /usr/src -f /usr/src/v1.78.tar.gz && \
    cd /usr/src/s3fs-fuse-1.78 && \
    ./autogen.sh && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    mkdir -p /srv/omaha_s3 && \
    rm /usr/src/v1.78.tar.gz && \

    # cleanup
    rm -rf /var/cache/apk/* && \
    apk del fuse-deps dev-deps && \

    # prepare
    mkdir -p $omaha/requirements


# RUN mkdir -p $omaha/requirements
WORKDIR ${omaha}

ADD ./requirements/base.txt $omaha/requirements/base.txt

RUN \
  pip install paver && \
  pip install --upgrade six && \
  pip install -r requirements/base.txt && \
  rm -rf /root/.cache/pip/


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
