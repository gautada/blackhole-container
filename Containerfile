ARG ALPINE_VERSION={OS_VERSION}

# ╭――――――――――――――――-------------------------------------------------------――╮
# │                                                                         │
# │ STAGE: container                                                      │
# │                                                                         │
# ╰―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――╯
FROM gautada/alpine:$ALPINE_VERSION

# ╭――――――――――――――――――――╮
# │ METADATA           │
# ╰――――――――――――――――――――╯
LABEL source="https://github.com/gautada/blackhole-container.git"
LABEL maintainer="Adam Gautier <adam@gautier.org>"
LABEL description="A benign endpoint for default blocking of advertising/blacklisted domains"

# ╭――――――――――――――――――――╮
# │ STANDARD CONFIG    │
# ╰――――――――――――――――――――╯

# USER:
ARG USER=blackhole

ARG UID=1001
ARG GID=1001
RUN /usr/sbin/addgroup -g $GID $USER \
 && /usr/sbin/adduser -D -G $USER -s /bin/ash -u $UID $USER \
 && /usr/sbin/usermod -aG wheel $USER \
 && /bin/echo "$USER:$USER" | chpasswd

# PRIVILEGE:
# COPY wheel  /etc/container/wheel

# BACKUP:
# COPY backup /etc/container/backup

# ENTRYPOINT:
RUN rm -v /etc/container/entrypoint
COPY entrypoint /etc/container/entrypoint

# FOLDERS
RUN /bin/chown -R $USER:$USER /mnt/volumes/container \
 && /bin/chown -R $USER:$USER /mnt/volumes/backup \
 && /bin/chown -R $USER:$USER /var/backup \
 && /bin/chown -R $USER:$USER /tmp/backup

# ╭――――――――――――――――――――╮
# │ APPLICATION        │
# ╰――――――――――――――――――――╯
# RUN apk add --no-cache --update python3
RUN apk add --no-cache py3-pip py3-requests py3-yaml
# RUN pip install fastapi
# RUN pip install "uvicorn[standard]"

RUN /bin/ln -fsv /mnt/volumes/container/block.list /etc/container/block.list \
 && /bin/ln -fsv /mnt/volumes/container/white.list /etc/container/white.list \
 && /bin/ln -fsv /mnt/volumes/container/black.list /etc/container/black.list \
 && /bin/ln -fsv /mnt/volumes/container/hosts.yml /mnt/volumes/configmaps/hosts.yml \
 && /bin/ln -fsv /mnt/volumes/configmaps/hosts.yml /etc/container/hosts.yml

COPY blackhole.py /home/blackhole/blackhole.py
RUN chown -R $USER:$USER /home/blackhole

# ╭――――――――――――――――――――╮
# │ CONTAINER          │
# ╰――――――――――――――――――――╯
USER $USER
VOLUME /mnt/volumes/backup
VOLUME /mnt/volumes/configmaps
VOLUME /mnt/volumes/container
EXPOSE 8080/tcp
WORKDIR /home/$USER

