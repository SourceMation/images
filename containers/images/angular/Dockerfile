FROM quay.io/sourcemation/nodejs-24:latest

ARG BUILD_DATE
ARG TARGETARCH

LABEL name="angular" \
      vendor="LinuxPolska" \
      url="https://linuxpolska.com/en/"\
      licenses="GPLv2" \
      created="$BUILD_DATE" \
      architecture="$TARGETARCH" \
      summary="NodeJS and Angular CLI on Debian 13 Slim Container" \
      description="Provides NodeJS and Angular on Debian 13 Slim Container" \
      version="19.2.0" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="NodeJS and Angular CLI on Debian 13 Slim Container" \
      io.k8s.description="Provides NodeJS and Angular on Debian 13 Slim Container" \
      io.openshift.tags="nodejs angular debian-13"

RUN npm install -g @angular/cli

EXPOSE 3000

RUN version=$(ng --version) && echo "angular: $version" >> /var/tmp/sourcemation.yml
CMD [ "/bin/bash" ]
