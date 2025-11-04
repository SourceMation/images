FROM docker.io/sourcemation/debian-13-slim:latest AS ruby

ARG VERSION=1.19.0
ARG RUBY_INSTALL=https://github.com/postmodern/ruby-install/releases/download/v0.10.1/ruby-install-0.10.1.tar.gz

ADD ${RUBY_INSTALL} /tmp/

RUN << EOF
apt-get update
apt-get install curl -y
mkdir /tmp/ruby-install/
tar -xf /tmp/*tar.gz --strip 1 -C /tmp/ruby-install
/tmp/ruby-install/bin/ruby-install -i /opt/ruby ruby
PATH="$PATH:/opt/ruby/bin"
gem update --system
gem install fluentd -v ${VERSION}
EOF

FROM docker.io/sourcemation/debian-13-slim:latest

ARG TARGETARCH
ARG BUILD_DATE
ARG LONGNAME="fluentd on Debian 13 Slim Container"

LABEL name="fluentd" \
  vendor="Sourcemation" \
  url="https://sourcemation.com"\
  source="https://github.com/Sourcemation/images/issues"\
  licenses="Apache-2.0" \
  created="${BUILD_DATE}" \
  architecture="${TARGETARCH}" \
  summary="${LONGNAME}" \
  description="Provides ${LONGNAME}" \
  version="1.19.0" \
  io.k8s.display-name="${LONGNAME}" \
  io.k8s.description="Provides ${LONGNAME}" \
  io.openshift.tags="fluentd debian-13-slim"

# INSTAL OR COPY --from=builder /builder/path /path
COPY --from=ruby /opt/ruby    /opt/ruby

ENV PATH="$PATH:/opt/ruby/bin"

# RUN update and setup user
RUN << EOF
set -e
apt-get update
apt-get upgrade -y
apt-get install libssl3 libyaml-0-2 -y
rm -rf /var/lib/apt/lists/*
fluentd --setup /etc/fluent
EOF
# END INSTALL

USER       nobody
VOLUME     [ "/etc/fluent" ]
EXPOSE     24224
ENTRYPOINT [ "fluentd" ]
