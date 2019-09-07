#FROM python:3-slim
FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
RUN apk --update add bash nano
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt
COPY pytaranislogo/ /var/www/pytaranislogo/
COPY config/settings.yml.example /var/www/pytaranislogo/config/settings.yml
COPY dist/pytaranislogo.cfg.example /var/www/pytaranislogo/config/pytaranislogo.cfg


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