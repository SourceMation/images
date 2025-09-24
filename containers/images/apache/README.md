# Apache HTTP Server Container on Debian 12 Slim packed by SourceMation

This image, `sourcemation/apache`, is built on a minimal Debian base to provide a robust **Apache HTTP Server** environment. It's designed for serving web content, handling dynamic requests, and acting as a powerful and flexible web server. The image integrates an essential Apache configuration and can be easily extended with custom modules and site setups.

Maintained by the SourceMation automation team, this Apache HTTP Server distribution (version 2.4.X) is regularly updated to ensure it's current, secure, and compact. It's built on a minimal Debian Slim base, and cryptographic signatures are used during the build process to guarantee the integrity of all source code and packages.

-----

## Core Features

  * **Apache HTTP Server Integration:** Comes with a pre-configured Apache server ready to serve content and handle web traffic.
  * **Modular Architecture:** Enables extending functionality with a wide array of official and third-party modules.
  * **Custom Configuration:** Allows for easy overriding of default configurations by mounting custom `httpd.conf` files and web content.

-----

## Operational Use

This image is intended for production environments where serving web applications and static content is critical. It must be configured by providing your website's content.

**Example for a local, non-production test:**

```bash
docker run -p 8080:8080 -it apache
```

This command runs the Apache container, mapping port `8080` on your local machine to the container's default HTTP port `8080`.

-----

## Configuration via Volume Mounts

This container is typically configured by mounting your files into it.

  * **Serving custom web content:** Mount your website's files to `/opt/apache2/htdocs/`.
  * **Using a custom configuration:** Mount your custom `httpd.conf` file to `/opt/apache2/conf/httpd.conf`.

-----

## Port Exposure
The standard Apache HTTP Server port, **8080**, is exposed by default.


## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the SourceMation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/apache` image is not affiliated with the Apache Software Foundation. The respective companies and
organisations own the trademarks mentioned in the offering. The `sourcemation/apache` image is a separate project and is maintained by [SourceMation](https://sourcemation.com).

## Extra notes
### Image and its components Risk Analysis report

A comprehensive risk analysis report detailing the image and its components can
be accessed on the [SourceMation platform](https://www.sourcemation.com/).

For more information, check out the [overview of the Apache HTTP Server](https://httpd.apache.org/docs/2.4/) page.

### Licenses

The base license for the Apache HTTP Server is the
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)