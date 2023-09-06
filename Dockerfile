FROM tiangolo/uwsgi-nginx-flask:latest
VOLUME ["/app/pytaranislogo/static", "/app/config", "/app/resources"]
ENV STATIC_URL /static
ENV STATIC_PATH /app/pytaranislogo/static
ENV TARANISLOGO_CFG /app/config/pytaranislogo.cfg
COPY ./requirements.txt /var/www/requirements.txt
# RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev freetype-dev
RUN apt install -y python3-dev libjpeg-dev zlib1g-dev libfreetype-dev
ENV LIBRARY_PATH=/lib:/usr/lib
RUN pip install --no-cache-dir -r /var/www/requirements.txt
COPY main.py /app/main.py
COPY pytaranislogo/ /app/pytaranislogo/
COPY config/settings.yml.example /app/config/settings.yml
COPY dist/pytaranislogo.cfg.example /app/config/pytaranislogo.cfg
