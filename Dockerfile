FROM registry.gautier.local:5000/alpine:3.8

COPY server.py /opt/pixel/server.py

RUN apk update ; apk add python3

CMD ["python3", "/opt/pixel/server.py"]
