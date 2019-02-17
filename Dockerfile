FROM python:3.5

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
        libatlas-base-dev gfortran nginx supervisor

RUN pip3 install uwsgi

COPY ./requirements.txt /project/requirements.txt
COPY /models /project/models

RUN pip3 install -r /project/requirements.txt

RUN useradd --no-create-home nginx

RUN rm /etc/nginx/sites-enabled/default
RUN rm -r /root/.cache

COPY nginx.conf /etc/nginx/
COPY flask-site-nginx.conf /etc/nginx/conf.d/

COPY uwsgi.ini /etc/uwsgi/
COPY supervisord.conf /etc/

COPY /src /project

WORKDIR /project

CMD ["/usr/bin/supervisord"]
