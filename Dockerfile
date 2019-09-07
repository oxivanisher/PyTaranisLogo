#FROM python:3-slim
FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
RUN apk --update add bash nano
VOLUME ["/app/pytaranislogo/static", "/app/config", "/app/resources"]
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static
ENV TARANISLOGO_CFG /app/config/pytaranislogo.cfg
COPY ./requirements.txt /var/www/requirements.txt
RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev
ENV LIBRARY_PATH=/lib:/usr/lib
RUN pip install -r /var/www/requirements.txt
COPY main.py /app/main.py
COPY pytaranislogo/ /app/pytaranislogo/
COPY config/settings.yml.example /app/config/settings.yml
COPY dist/pytaranislogo.cfg.example /app/config/pytaranislogo.cfg


# ENV FLASK_APP pytaranislogo.py
# MAINTAINER Marc Urben "aegnor@mittelerde.ch"
# RUN apt update -y
# RUN apt install -y python3-pip python3-dev build-essential
# VOLUME ["/app/pytaranislogo/static", "/app/config", "/app/resources"]
# ENV TARANISLOGO_CFG="/app/config/pytaranislogo.cfg"
# COPY pytaranislogo/ /app/pytaranislogo/
# COPY config/settings.yml.example /app/config/settings.yml
# COPY dist/pytaranislogo.cfg.example /app/config/pytaranislogo.cfg
# COPY requirements.txt /app/
# RUN pip install -r /app/requirements.txt
# WORKDIR /app/pytaranislogo
# #ENTRYPOINT ["python"]
# EXPOSE 80/tcp
# CMD ["flask", "run", "--host", "0.0.0.0", "--port", "80"]
# #EXPOSE 5000/tcp
# #CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]