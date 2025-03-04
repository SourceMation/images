FROM sourcemation/nodejs:latest

LABEL name="angular" \
      vendor="LinuxPolska" \
      url="https://linuxpolska.com/en/"\
      licenses="GPLv2" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="NodeJS and Angular CLI on EL9 Container" \
      description="Provides NodeJS and Angular on Rocky Linux 9 Container" \
      version="19.2.0" \
      io.k8s.display-name="NodeJS and Angular CLI on EL9 Container" \
      io.k8s.description="Provides NodeJS and Angular on Rocky Linux 9 Container" \
      io.openshift.tags="nodejs angular rockylinux"

RUN npm install -g @angular/cli

RUN version=$(ng --version) && echo "angular: $version" >> /var/tmp/sourcemation.yml
CMD [ "/bin/bash" ]
