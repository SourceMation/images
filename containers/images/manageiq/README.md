# ManageIQ repacked by Sourcemation

ManageIQ is an open-source cloud management platform that provides a unified
view of your hybrid cloud environment. This repository contains a repacked
version of ManageIQ, tailored for easier deployment and management.

## Usage

The easiest way to start the ManageIQ appliance is to use the provided image.
To start **temporary** image with the latest version of ManageIQ, you can use the
following command:

```bash
docker run --rm -it -p 8080:443 quay.io/sourcemation/manageiq:latest-amd64
```

The ManageIQ web interface will be available at [https://localhost:8080](https://localhost:8080).

#### **The default username is `admin` and the password is `smartvm`.**

## Persistence

The container has two volumes

- `/var/www/miq/vmdb`
- `/var/lib/pgsql/data`

These volumes are used to used to create a persistent storage for the ManageIQ
database and application data. You can mount these volumes to your host or a to
your kubernetes cluster to ensure that your data is not lost when the container
is stopped or removed.

Example with podman:

```bash
podman run -d --name manageiq \
  -p 8080:443 \
  -v /path/to/your/data:/var/www/miq/vmdb \
  -v /path/to/your/db:/var/lib/pgsql/data \
  quay.io/sourcemation/manageiq:radjabov-1
```

Note usage of the `radjabov-1` tag. You can use particular tag to run a specific
version of ManageIQ. The `latest` tag will always point to the latest version of
ManageIQ.

## Environment Vars, Ports

The only port that is exposed by the container is `443`, which is used for HTTPS
traffic. The container does not expose any other ports.

The environment variables that are used by the container are:

```bash
ANSIBLE_LOCAL_TEMP=/tmp/.ansible_local_tmp
ANSIBLE_REMOTE_TEMP=/tmp/.ansible_remote_tmp
APPLIANCE=true
APPLIANCE_PG_CTL=/usr/bin/pg_ctl
APPLIANCE_PG_DATA=/var/lib/pgsql/data
APPLIANCE_PG_MOUNT_POINT=/var/lib/pgsql
APPLIANCE_PG_PACKAGE_NAME=postgresql-server
APPLIANCE_PG_SERVICE=postgresql
APPLIANCE_SOURCE_DIRECTORY=/opt/manageiq/manageiq-appliance
APPLIANCE_TEMPLATE_DIRECTORY=/opt/manageiq/manageiq-appliance/TEMPLATE
APP_ROOT=/var/www/miq/vmdb
BUNDLE_GEMFILE=/var/www/miq/vmdb/Gemfile
CONTAINER=true
DATABASE_URL=postgresql://root@localhost/vmdb_production?encoding=utf8&pool=5&wait_timeout=5
EXECJS_RUNTIME=Node
GEM_HOME=/opt/manageiq/manageiq-gemset
GEM_PATH=/opt/manageiq/manageiq-gemset:/usr/share/gems:/usr/local/share/gems
KEY_ROOT=/var/www/miq/vmdb/certs
LANG=en_US.UTF-8
LANGUAGE=en_US.UTF-8
LC_CTYPE=en_US.UTF-8
LESSOPEN=||/usr/bin/lesspipe.sh %s
MALLOC_ARENA_MAX=1
PATH=/root/.local/bin:/root/bin:/opt/manageiq/manageiq-gemset/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin
RAILS_ENV=production
RUBY_GC_HEAP_GROWTH_FACTOR=1.25
RUBY_GC_HEAP_GROWTH_MAX_SLOTS=300000
RUBY_GC_HEAP_INIT_SLOTS=600000
SHLVL=1
TERM=xterm
TERRAFORM_RUNNER_URL=https://localhost:6000
container=oci
```

The most important ones are `DATABASE_URL`, which is used to connect to the
ManageIQ database, and `RAILS_ENV`, which is set to `production` by default.
Also the language and locale settings are set to `en_US.UTF-8` to ensure the
default language is English and the locale is set to UTF-8.


## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the Sourcemation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/manageiq` image is not affiliated with the
official GitHub organization. The respective companies and organisations
own the trademarks mentioned in the offering. The `sourcemation/manageiq` image
is a separate project and is maintained by
[Sourcemation](https://sourcemation.com).

## Extra notes

- This ManageIQ distribution is shipped **from original images**, it's not typical fully independent sourcemation rebuild
- This image add a few extra features, such as:
  - Installing the `pyvmomi` Python package, which is used to interact with VMware vSphere and ESXi hosts.
  - Installing the `passlib[bcrypt]` Python package, which is used for password hashing.
  - Installing the `community.vmware` Ansible collection, which provides modules and plugins for managing VMware infrastructure.
- This image is tagged in same way as all Sourcemation images with `latest` `verson-x` and `version-x-builddate` tags.


## License

The base license for the solution (ManageIQ) is the Apache License Version 2.0.
The licenses for each component shipped as part of this image must be found
separately from RPM or other resources.
