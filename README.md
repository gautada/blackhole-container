# Pixel 

A simple python based service that serves single blank pixels or empty responses via an internal  HTTP server to be used with DNS base AdBlockers

## Distribution

Alpine Linux 3.8

## Dependency

Reversed Proxy Through Apache httpd

## Reference

https://daanlenaerts.com/blog/2015/06/03/create-a-simple-http-server-with-python-3/


cd ../pixel ; docker build --tag=pixel:build . ; docker run --detach=true --dns=172.22.0.05 --hostname=pixel.gautier.local --ip=172.22.0.99 --name=pixel.gautier.docker --network=gautier.docker --restart=always pixel:build ; cd ../httpd
