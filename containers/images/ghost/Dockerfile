FROM sourcemation/nodejs-22:latest

ARG TARGETARCH
ARG BUILD_DATE
ARG LONGNAME="Ghost on Nojde.js 22 Container"

LABEL name="ghost" \
      vendor="Sourcemation" \
      url="https://sourcemation.com" \
      source="https://github.com/Sourcemation/images/issues" \
      licenses="MIT" \
      created="${BUILD_DATE}" \
      architecture="${TARGETARCH}" \
      summary="${LONGNAME}" \
      description="Provides ${LONGNAME}" \
      version="6.8.1" \
      io.k8s.display-name="${LONGNAME}" \
      io.k8s.description="Provides ${LONGNAME}" \
      io.openshift.tags="ghost nodejs-22"


ENV NODE_ENV=development
ARG GHOST_VERSION=6.8.1
ENV GHOST_INSTALL=/var/lib/ghost
ENV GHOST_CONTENT=/var/lib/ghost/content

RUN set -ex; \
    apt-get update; \
    apt-get upgrade -y; \
    apt-get install -y --no-install-recommends gosu; \
    npm install -g ghost-cli@latest; \
    rm -rf /var/lib/apt/lists/*; \
    mkdir -p ${GHOST_INSTALL}; \
    chown -R node:node ${GHOST_INSTALL}

WORKDIR ${GHOST_INSTALL}

RUN gosu node ghost install "${GHOST_VERSION}" --db mysql --no-prompt --no-stack --no-setup --no-start --dir ${GHOST_INSTALL}

RUN gosu node ghost config --no-prompt --ip '::' --port 2368 --url 'http://localhost:2368'

RUN mv ${GHOST_CONTENT} ${GHOST_INSTALL}/content.orig && \
    mkdir -p ${GHOST_CONTENT} && \
    chown node:node ${GHOST_CONTENT}

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 2368

VOLUME ${GHOST_CONTENT}

ENTRYPOINT ["entrypoint.sh"]

CMD ["node", "current/index.js"]