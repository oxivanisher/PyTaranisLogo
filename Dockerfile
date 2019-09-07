FROM python:3-slim
ENV FLASK_APP pytaranislogo.py
MAINTAINER Marc Urben "aegnor@mittelerde.ch"
RUN apt update -y
RUN apt install -y python3-pip python3-dev build-essential
VOLUME ["/app/pytaranislogo/static", "/app/config", "/app/resources"]
ENV TARANISLOGO_CFG="/app/config/pytaranislogo.cfg"
COPY pytaranislogo/ /app/pytaranislogo/
COPY config/settings.yml.example /app/config/settings.yml
COPY dist/pytaranislogo.cfg.example /app/config/pytaranislogo.cfg
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
WORKDIR /app/pytaranislogo
#ENTRYPOINT ["python"]
EXPOSE 80/tcp
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "80"]
#EXPOSE 5000/tcp
#CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]