# Nginx Mainline by SourceMation

Nginx (pronounced "engine-x") stands as a robust and high-performing solution
for HTTP serving, reverse proxying, and load balancing tasks. Celebrated for
its exceptional stability, a comprehensive suite of features, straightforward
configuration syntax, and remarkably low consumption of system resources, Nginx
has become a cornerstone of modern web infrastructure.

This carefully crafted Docker image delivers a pristine and lightweight
installation of the Nginx **mainline release**. It is built upon SourceMation’s
optimized Debian 12 Slim base, ensuring a minimal footprint and enhanced
security.

## Getting Started

**To quickly launch a temporary Nginx container for testing:**

```bash
docker run --rm -it sourcemation/nginx-mainline
```

## Advanced Usage Scenarios

**Customizing Nginx with a Specific Configuration:**

To integrate your own `nginx.conf` file, create a Dockerfile like this:

```dockerfile
FROM sourcemation/nginx-mainline

COPY nginx.conf /etc/nginx/nginx.conf
```

**Serving Static Content by Mounting a Local Directory:**


Mount your local `./content` directory to a container named `static-website`:

```bash
docker run -v ./content:/usr/share/nginx/html:ro --name static-website sourcemation/nginx-mainline
```

**Creating a Custom Image with Embedded Static Content:**


Alternatively, build a new image with your content directly included:

```dockerfile
FROM sourcemation/nginx-mainline
COPY ./content /usr/share/nginx/html
```

## Dynamic Configuration with Templating

This image provides powerful templating capabilities, allowing you to
dynamically generate Nginx configurations. While you can directly modify the
base `nginx.conf`, you can also create template files that leverage environment
variables for flexible deployments. The `envsubst` utility is integrated to
perform the substitution of these variables within your templates.

Place your template files within the `/etc/nginx/templates` directory of your
custom image. You can also adjust this default directory using the
`NGINX_TEMPLATES_DIR` environment variable.

To gain deeper insight into the templating mechanism, examine the relevant
entrypoint script (remember to adjust the image tag as needed):

```bash
docker run --rm -it sourcemation/nginx-mainline /usr/bin/cat /docker-entrypoint.d/20-envsubst-on-templates.sh
```

## Available Image Variants

This image is offered in several variants to cater to different needs:

- `nginx-mainline:TAG`: This variant provides the standard mainline version of
  Nginx, incorporating the latest mainline release available at the time of the
  image's creation.
- `nginx-mainline:TAG-perl`: This variant includes the mainline version of
  Nginx along with essential Perl-related packages, built against the most
  recent mainline release.
- `nginx-mainline:TAG-otel`: This variant extends the mainline Nginx with
  OpenTelemetry-related modules, based on the latest mainline release at build
  time.

## Key Environment Variables

The most significant environment variable for configuration is:

```bash
NGINX_VERSION=X.YY.Z # For example: 1.27.5
```

While other `VERSION` variables exist, they primarily serve internal image building processes.

## Contributing and Issues

We welcome your contributions! If you have new feature requests, want to report
a bug, or wish to submit a pull request with your code or an image request, you
can do so via the SourceMation GitHub repository for this image.

- [Open a new issue (for feature requests, bug reports, or image requests)](https://github.com/SourceMation/images/issues/new/choose)
- [Submit a pull request](https://github.com/SourceMation/images/compare)

## Important Considerations

A key distinction of this image is that it retains the original Nginx
repository configuration. This allows you to easily install additional
Nginx-related packages as required, offering greater flexibility.

## Further Information

### Image Component Security Assessment

Comprehensive risk analysis reports detailing the security posture of our
images and their constituent components can be accessed on the [SourceMation
platform](https://www.sourcemation.com/).

Please note: Risk analysis reports are not yet available for all images. For
information on specific software components or further inquiries, please do not
hesitate to contact us.

### Licensing Details

The fundamental license governing Nginx is the [2-clause BSD
License](https://nginx.org/LICENSE).
