# Prometheus PostgreSQL Exporter Container

This image provides a robust **postgres-exporter** environment for Prometheus. It's designed for exporting a wide range of PostgreSQL metrics for monitoring, including performance, resource utilization, and operational health. The image is configured to be flexible, allowing for extensive customization of the metrics you collect.

Maintained by the Sourcemation, this `postgres_exporter` distribution is regularly updated to ensure it's current and secure. It is a lightweight and focused container, designed for easy integration into your existing Prometheus and PostgreSQL monitoring stack.

-----

## Core Features

  * **Extensive PostgreSQL Metrics:** Gathers a wide array of metrics from your PostgreSQL server, with the ability to add custom queries.
  * **Highly Configurable:** Fine-tune the exporter's behavior through environment variables and command-line arguments.
  * **Automatic Database Discovery:** Can be configured to automatically discover and monitor all databases within a PostgreSQL instance.
  * **Prometheus Integration:** Exposes metrics in a format that Prometheus can scrape, for easy integration with your existing monitoring and alerting workflows.

-----

## Operational Use

This image is intended for production environments where monitoring PostgreSQL is critical. It must be configured with the connection details for your PostgreSQL server.

**Example for a local, non-production test:**

```bash
# Start an example database
docker run --net=host -it --rm -e POSTGRES_PASSWORD=password postgres

# Connect to it
docker run \
  --net=host \
  -e DATA_SOURCE_URI="localhost:5432/postgres?sslmode=disable" \
  -e DATA_SOURCE_USER=postgres \
  -e DATA_SOURCE_PASS=password \
  sourcemation/postgres-exporter

# Test it
curl "http://localhost:9187/metrics"
```

## Key Environment Variables

This container uses the following environment variables for configuration:

  * `DATA_SOURCE_NAME`:  the default legacy format. Accepts URI form and key=value form arguments. The URI may contain the username and password to connect with.
  * `DATA_SOURCE_URI`: an alternative to DATA_SOURCE_NAME which exclusively accepts the hostname without a username and password component. For example, my_pg_hostname or my_pg_hostname:5432/postgres?sslmode=disable.
  * `DATA_SOURCE_USER`: When using DATA_SOURCE_URI, this environment variable is used to specify the username.
  * `DATA_SOURCE_PASS`: When using DATA_SOURCE_URI, this environment variable is used to specify the password to connect with.
  * `DATA_SOURCE_PASS_FILE`: The same as above but reads the password from a file.


For a full list of environment variables and configuration options, please refer to the [official documentation](https://github.com/prometheus-community/postgres_exporter).

## Port Exposure

The standard `postgres-exporter` port, **9187**, is exposed by default. Metrics are available at the `/metrics` endpoint.

## Contributing and Reporting Issues

Your contributions are valued! Feel free to suggest enhancements or request new
images by opening an issue, or submit your own contributions via pull requests
to the Sourcemation GitHub repository.

- [Creating issues (bugs) and images requests](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)


## Extra notes

**Disclaimer:** The `sourcemation/postgres-exporter` image is not affiliated with
prometheus-community. The respective entities own the trademarks mentioned in
the offering. The `sourcemation/postgres-exporter` image is a separate project and
is maintained by [Sourcemation](https://sourcemation.com).

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [Sourcemation
platform](https://www.sourcemation.com/products/b95ab2de-202b-45f2-a2a3-086e64968979/deployments).

For more information, check out the [overview of
postgres_exporter](https://github.com/prometheus-community/postgres_exporter) page.


### Licenses

The base license for the solution (postgres_exporter) is the [Apache License 2.0](https://github.com/prometheus-community/postgres_exporter?tab=Apache-2.0-1-ov-file#readme).