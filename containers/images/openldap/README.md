# OpenLDAP packaged by SourceMation

> OpenLDAP is a free, open-source implementation of the Lightweight Directory Access Protocol (LDAP) developed by the OpenLDAP Project.

This OpenLDAP distribution is provided by the SourceMation packaging team. It is built from the latest available source code to ensure up-to-date features and security, all on a secure **Debian 12 Slim** base image. The container is configured on its first run using environment variables.

## Usage

Run a temporary container for quick testing. A random admin password will be generated and printed to the container's logs.

```
docker run --rm -it -p 389:389 sourcemation/openldap:latest
# Check the logs for the random password
docker logs <container_id>
```

### Advanced usage examples

Run OpenLDAP in detached mode with persistent storage using named volumes. This is the recommended method for any real use.

```
docker run -d --name my-ldap-server \
  -p 389:389 -p 636:636 \
  --restart always \
  -v ldap_data:/var/lib/ldap \
  -v ldap_config:/etc/ldap/slapd.d \
  -e LDAP_DOMAIN="mycompany.com" \
  -e LDAP_ORGANISATION="my-company" \
  -e LDAP_ADMIN_PASSWORD="my-secure-password" \
  sourcemation/openldap:latest
```

## Configuration

This image is configured on the first run using environment variables passed to the docker run command.

- LDAP_DOMAIN: Sets the base domain for your LDAP directory (e.g., mycompany.com becomes dc=mycompany,dc=com). Default: example.org.
- LDAP_ORGANISATION: Sets the name of your organization. Default: Example Inc.
- LDAP_ADMIN_PASSWORD: Sets the password for the admin user (cn=admin,dc=...). If omitted, a random password will be generated and printed to the logs on the first run.

## Image tags and versions

The `sourcemation/openldap` image itself comes in `debian-12` flavor.
The tag `latest` refers to the Debian-based flavor.

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
LDAP_CONF_DIR=/etc/ldap
LDAP_DATA_DIR=/var/lib/ldap
```

This image exposes the following ports: 

- 389 - LDAP protocol
- 636 - LDAPS (LDAP over SSL/TLS) protocol

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

Volumes:

- /var/lib/ldap - Data directory for the LDAP database files.
- /etc/ldap/slapd.d - Directory for the dynamic runtime configuration.

It is highly recommended to use volumes to make your data and configuration persistent.


## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the SourceMation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/openldap` image is not affiliated with
the OpenLDAP Project. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/openldap` image is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [SourceMation
platform](https://sourcemation.com/).

For more information, check out the [OpenLDAP Software](https://www.openldap.org/software/) page.

### Licenses

The base license for the solution (OpenLDAP) is the
[OpenLDAP Public License 2.8](https://www.openldap.org/software/release/license.html). The licenses for each component shipped as
part of this image can be found on [the image's appropriate SourceMation
entry](https://sourcemation.com/).
