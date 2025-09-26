# Keycloak Container on Debian 12 Slim packed by SourceMation

This image, `sourcemation/keycloak`, is built on a minimal Debian base to provide a robust **Keycloak** environment. It's designed for adding authentication to applications and securing services with minimal effort, providing a comprehensive Identity and Access Management (IAM) solution. The image integrates the complete Keycloak server and can be configured for production workloads.

Maintained by the SourceMation automation team, this Keycloak distribution is regularly updated to ensure it's current, secure, and compact. It's built on a minimal Debian Slim base, and cryptographic signatures are used during the build process to guarantee the integrity of all source code and packages.

-----

## Core Features

  * **Identity and Access Management:** Comes with the full Keycloak server for managing users, roles, and permissions.
  * **Standard Protocol Support:** Out-of-the-box support for OpenID Connect, OAuth 2.0, and SAML 2.0.
 * **Centralized Administration:** Provides an easy-to-use web-based console for managing all aspects of the server.

-----

## Operational Use

This image is intended for production environments where centralized authentication and authorization are critical. To start the server for the first time, you must provide an initial admin username and password.

**Example for a local, non-production test:**

```bash
docker run \
    -e KEYCLOAK_ADMIN_USERNAME=admin \
    -e KEYCLOAK_ADMIN_PASSWORD=password \
    -p 8080:8080 \
    -it sourcemation/keycloak \
    start-dev
```

This command runs the Keycloak container in development mode, mapping port `8080` on your local machine to the container's default port `8080`.

-----

## Key Environment Variables

This container uses the following environment variables for initial configuration:

  * `KEYCLOAK_ADMIN`: The username for the initial admin user created on the first boot.
  * `KEYCLOAK_ADMIN_PASSWORD`: The password for the initial admin user.

-----

## Port Exposure
The standard Keycloak port, **8080** and **8443**, are exposed by default.


## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the SourceMation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/keycloak` image is not affiliated with the CNCF or Red Hat. The respective companies and
organisations own the trademarks mentioned in the offering. The `sourcemation/keycloak` image is a separate project and is maintained by [SourceMation](https://sourcemation.com).

## Extra notes
### Image and its components Risk Analysis report

A comprehensive risk analysis report detailing the image and its components can
be accessed on the [SourceMation platform](https://www.sourcemation.com/).

For more information, check out the [overview of Keycloak](https://www.keycloak.org/documentation) page.

### Licenses

The base license for Keycloak is the
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)