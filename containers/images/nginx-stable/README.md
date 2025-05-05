# Nginx stable packaged by SourceMation

Nginx (engine x) is a high-performance HTTP server, reverse proxy and load
balancer. It’s known for its stability, rich feature set, simple configuration,
and low resource consumption.


This Docker image provides a clean, lightweight Nginx stable release installed
on SourceMation’s Debian 12 Slim.

## Usage

Run a temporary container with Nginx:

```bash
docker run --rm -it sourcemation/nginx-stable
```

## Advanced usage examples


Creating customized Nginx with a custom configuration file:

```dockerfile
FROM sourcemation/nginx-stable

COPY nginx.conf /etc/nginx/nginx.conf
```

Mounting a local directory `./content` to the container named `static-website`:

```bash
docker run -v ./content:/usr/share/nginx/html:ro --name static-website sourcemation/nginx
```

Or create a custom image with the same content:

```dockerfile
FROM sourcemation/nginx-stable
COPY ./content /usr/share/nginx/html
```

## Templating the configuration

You can use the `nginx.conf` file as a template to create custom
configurations, but you can also create templates that use environment
variables. This image uses the `envsubst` to substitute environment variables in
the templating file.


The templates should be stored in the `/etc/nginx/templates` directory of your
customized image (it's also changeable with the `NGINX_TEMPLATES_DIR`
environment).


For more information about templating read the templating script (you should
probably change the image tag):


```bash
docker run --rm -it sourcemation/nginx-stable /usr/bin/cat /docker-entrypoint.d/20-envsubst-on-templates.sh
```

## Image variants

- nginx-stable:TAG - The stable version of Nginx based on the latest stable release available
  at the time of the image build.
- nginx-stable:TAG-perl - The stable version of Nginx based on the latest mainline release available
  during the image build with Perl-related packages.
- nginx-stable:TAG-otel - The stable version of Nginx, based on the latest mainline release available
  during the image build with OpenTelemetry-related modules.


## Environment Variables

The most important environment variables are:

```
NGINX_VERSION=X.YY.Z # Example: 1.27.5
```

There are also other VERSION variables, but they are more for building the
image.

## Extra notes

This image, unlike other images, does not remove the Nginx repository from its
configuration, so it is possible to install additional Nginx-related packages.

## Additional Information

### Image Component Risk Analysis

Detailed risk analysis reports for our images and their components are
available on the [SourceMation platform](https://www.sourcemation.com/).

Note: Risk analysis reports are not yet available for all images. Contact us
for additional software components or inquiries.

### Licensing

The core license for Nginx is the [2-clause BSD
License](https://nginx.org/LICENSE).
