FROM python:3-alpine
MAINTAINER Marc Urben "aegnor@mittelerde.ch"
EXPOSE 80/tcp
RUN apt update -y
RUN apt install -y python-pip python-dev build-essential
VOLUME ["/app/pytaranislogo/static", "/app/config", "/app/log", "/app/resources"]
ENV TARANISLOGO_CFG="/app/config/pytaranislogo.cfg"
COPY pytaranislogo.py /app
COPY pytaranislogo /app
COPY config/settings.yml.example /app/config
COPY dist/pytaranislogo.cfg.example /app/config
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["flask"]
CMD ["run","--host","0.0.0.0","--port","80"]