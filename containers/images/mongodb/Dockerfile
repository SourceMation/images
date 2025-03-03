FROM rockylinux/rockylinux:9

ARG TARGETARCH

LABEL name="mongodb" \
      vendor="LinuxPolska" \
      url="https://linuxpolska.com/en/"\
      licenses="GPLv2" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="MongoDB on EL9 Container" \
      description="Provides MongoDB on Rocky Linux 9 Container" \
      version="8.0.5" \
      io.k8s.display-name="MongoDB on EL9 Container" \
      io.k8s.description="Provides MongoDB on Rocky Linux 9 Container" \
      io.openshift.tags="mongodb rockylinux"

ENV HOME="/"

COPY additions/mongodb-org-8.0.repo /etc/yum.repos.d/

RUN groupadd -g 999 mongodb 
RUN useradd -g 999 -u 999 mongodb

# Install sudo to have root permission as a mongodb user
RUN dnf update -y
RUN dnf install -y mongodb-org

# WARNING: vm.max_map_count is too low
# AND
# WARNING: /sys/kernel/mm/transparent_hugepage/enabled is 'always'. We suggest setting it to 'never'
# Do it on the host before starting the container!!!!
# echo "vm.max_map_count=9999999" | sudo tee -a /etc/sysctl.conf
# Above needs a reboot
# echo never | sudo tee /sys/kernel/mm/transparent_hugepage/enabled > /dev/null

# WARNING: Access control is not enabled for the database. Read and write access to data and configuration is unrestricted
COPY additions/one_time_script.sh /opt/
COPY additions/start.sh /home/mongodb/start.sh
RUN chmod +x /home/mongodb/start.sh
RUN chmod +x /opt/one_time_script.sh

ENV APP_VERSION="8.0.5" \
    APP_NAME="mongodb"

EXPOSE 27017

RUN cp /etc/mongod.conf /home/mongodb/mongod.conf
RUN sed -iE "s|/var/lib/mongo|/home/mongodb/database/|g" /home/mongodb/mongod.conf
RUN sed -iE "s|/var/log/mongodb/mongod.log|/dev/stdout|g" /home/mongodb/mongod.conf

RUN chown -R mongodb:mongodb /opt /home/mongodb/
USER 999
ENV HOME="/home/mongodb"
WORKDIR /home/mongodb
RUN mkdir /home/mongodb/database
RUN mkdir /home/mongodb/logs
RUN touch /home/mongodb/logs/mongod.log

ENTRYPOINT ["/home/mongodb/start.sh"]
