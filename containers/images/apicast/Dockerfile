FROM sourcemation/rocky-9:latest

LABEL name="apicast" \
      vendor="SourceMation" \
      url="https://sourcemation.com"\
      licenses="Apache-2.0" \
      created="$(date +%Y%m%d)" \
      architecture="$(uname -m)" \
      summary="APIcast on EL9 Container" \
      description="Provides APICast Rocky Linux 9 Container" \
      version="3.15.0" \
      org.opencontainers.image.source="https://github.com/Sourcemation/images" \
      io.k8s.display-name="APIcast on EL9 Container" \
      io.k8s.description="Provides APICast on Rocky Linux 9 Container" \
      io.openshift.tags="apicast rockylinux api gateway"

# Install dependencies
RUN yum install -y yum-utils gcc git epel-release

# Enable OpenResty repo (see RHEL section at https://openresty.org/en/linux-packages.html)
RUN yum-config-manager --add-repo https://openresty.org/package/centos/openresty2.repo

# Upgrade yum
RUN yum update -y

# Install OpenResty
RUN export OPENRESTY_RPM_VERSION="1.21.4.3-1.el9" \
  && yum install -y \
     openresty-${OPENRESTY_RPM_VERSION} \
     openresty-resty-${OPENRESTY_RPM_VERSION}

# Install LuaRocks
RUN yum install --enablerepo='crb' -y  lua5.1 lua5.1-devel luajit luajit-devel libyaml-devel make gcc-c++ make m4 which iputils bind-utils expat-devel m4\
    wget tar unzip libyaml libyaml-devel \
    perl-local-lib perl-App-cpanminus \
    openssl-devel libev-devel \
    kernel-headers kernel-devel kernel-debug \
    redis systemtap \
    python3-pip elfutils-devel perl-Crypt-JWT
RUN yum install -y luarocks --setopt=install_weak_deps=0 --setopt=tsflags=nodocs  && rpm -evh --nodeps lua
RUN ln -s /usr/bin/lua-5.1 /usr/bin/lua

# Configure Lua environment
RUN mkdir -p /usr/share/lua/5.1/luarocks/ share/lua/5.1/luarocks/
COPY ./site_config.lua /usr/share/lua/5.1/luarocks/
COPY ./site_config.lua /share/lua/5.1/luarocks/

RUN adduser appuser

WORKDIR /home/appuser
# Make luaffi-Makefile
COPY ./luaffi-Makefile /
RUN git clone https://github.com/jmckaskill/luaffi.git && cd luaffi && mv /luaffi-Makefile Makefile && make && cp -v ffi.so /usr/lib64/lua/5.1/

# Download the v3.2.0 release (Red Hat 3scale API Management v2.2) and extract it
RUN git clone https://github.com/3scale/APIcast.git && \
  cd APIcast && git reset --hard c54aa0b  && sed -i 's/lua-rover/lua-rover-old/' Makefile && \
  make dependencies && rm -rf /root/.cpanm/

RUN version=$(git -C /home/appuser/APIcast/ describe --tags --abbrev=0 | tr -d 'v') && \
    echo "apicast: $version" >> /var/tmp/sourcemation.yml

# Fix keepalive pool that is not supported in OpenResty
RUN sed -e '/keepalive_pool/ s/^#*/#/' -i /home/appuser/APIcast/gateway/http.d/upstream.conf

ENV PATH="/home/appuser/APIcast/bin:${PATH}"
ENV PATH="/home/appuser/APIcast/lua_modules/bin:/usr/local/openresty/luajit/bin/:${PATH}" \
    LUA_PATH="/home/appuser/APIcast/lua_modules/share/lua/5.1/?.lua;/home/appuser/APIcast/lua_modules/bin/lua_modules/share/lua/5.1/?/init.lua;/usr/lib64/lua/5.1/?.lua;/usr/share/lua/5.1/?.lua" \
    LUA_CPATH="/home/appuser/APIcast/lua_modules/lib/lua/5.1/?.so;;" \
    LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/home/appuser/APIcast/local/lib:/home/appuser/APIcast/lua_modules/lib"

RUN chown -R appuser:appuser /home/appuser
USER appuser

CMD apicast -h
