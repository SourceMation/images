FROM sourcemation/debian-12-slim:latest AS build

ENV PATH /usr/local/go/bin:$PATH

ENV GOLANG_VERSION="1.24.1"
# The bellow URL is set in the init.sh script!
ENV GO_URL="https://dl.google.com/go/go1.24.1.linux-amd64.tar.gz"
ENV GO_SHA256="cb2396bae64183cdccf81a9a6df0aea3bce9511fc21469fb89a0c00470088073"


RUN set -eux; \
	apt-get update && apt-get install -y --no-install-recommends \
                ca-certificates \
                dirmngr \
                gnupg \
                wget ; \
	now="$(date '+%s')"; \
	wget -O go.tgz.asc "$GO_URL.asc"; \
	wget -O go.tgz "$GO_URL" --progress=dot:giga; \
	echo "$GO_SHA256 *go.tgz" | sha256sum -c -; \
	\
# https://github.com/golang/go/issues/14739#issuecomment-324767697
	GNUPGHOME="$(mktemp -d)"; export GNUPGHOME; \
# https://www.google.com/linuxrepositories/
	gpg --batch --keyserver keyserver.ubuntu.com --recv-keys 'EB4C 1BFD 4F04 2F6D DDCC  EC91 7721 F63B D38B 4796'; \
# let's also fetch the specific subkey of that key explicitly that we expect "go.tgz.asc" to be signed by, just to make sure we definitely have it
	gpg --batch --keyserver keyserver.ubuntu.com --recv-keys '2F52 8D36 D67B 69ED F998  D857 78BD 6547 3CB3 BD13'; \
	gpg --batch --verify go.tgz.asc go.tgz; \
	gpgconf --kill all; \
	rm -rf "$GNUPGHOME" go.tgz.asc; \
	\
	tar -C /usr/local -xzf go.tgz; \
	rm go.tgz; \
	\
# save the timestamp from the tarball so we can restore it for reproducibility, if necessary (see below)
	SOURCE_DATE_EPOCH="$(stat -c '%Y' /usr/local/go)"; \
	export SOURCE_DATE_EPOCH; \
	touchy="$(date -d "@$SOURCE_DATE_EPOCH" '+%Y%m%d%H%M.%S')"; \
# for logging validation/edification
	date --date "@$SOURCE_DATE_EPOCH" --rfc-2822; \
# sanity check (detected value should be older than our wall clock)
	[ "$SOURCE_DATE_EPOCH" -lt "$now" ]; \
	\
# ideally at this point, we would just "COPY --link ... /usr/local/go/ /usr/local/go/" but BuildKit insists on creating the parent directories (perhaps related to https://github.com/opencontainers/image-spec/pull/970), and does so with unreproducible timestamps, so we instead create a whole new "directory tree" that we can "COPY --link" to accomplish what we want
	mkdir -p /target/usr/local; \
	mv -vT /usr/local/go /target/usr/local/go; \
	ln -svfT /target/usr/local/go /usr/local/go; \
	touch -t "$touchy" /target/usr/local /target/usr /target; \
	\
# smoke test
	go version; \
# make sure our reproducibile timestamp is probably still correct (best-effort inline reproducibility test)
	epoch="$(stat -c '%Y' /target/usr/local/go)"; \
	[ "$SOURCE_DATE_EPOCH" = "$epoch" ]; \
	find /target -newer /target/usr/local/go -exec sh -c 'ls -ld "$@" && exit "$#"' -- '{}' +


FROM sourcemation/debian-12-slim:latest

LABEL name="golang-1.24" \
      vendor="SourceMation" \
      url="https://sourcemation.com"\
      licenses="BSD 3-Clause \"New\" or \"Revised\" License" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="Golang on debian-12-slim container" \
      description="Provides golang on Debian 12 Slim Container" \
      version="1.24.1" \
      io.k8s.display-name="Golang on Debian 12 Slim Container" \
      io.k8s.description="Provides golang on Debian 12 Slim Container" \
      io.openshift.tags="golang debian-12-slim"

RUN set -eux; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
		g++ \
		gcc \
		libc6-dev \
		make \
		pkg-config \
	; \
	rm -rf /var/lib/apt/lists/*


ENV GOLANG_VERSION="1.24.1"

# don't auto-upgrade the gotoolchain
# https://github.com/docker-library/golang/issues/472
ENV GOTOOLCHAIN=local

ENV GOPATH /go
ENV PATH $GOPATH/bin:/usr/local/go/bin:$PATH
# (see notes above about "COPY --link")
COPY --from=build --link /target/ /
RUN mkdir -p "$GOPATH/src" "$GOPATH/bin" && chmod -R 1777 "$GOPATH"
WORKDIR $GOPATH
