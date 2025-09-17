# Kibana packaged by SourceMation

> Kibana is an open-source data visualization and exploration tool used for log and time-series analytics, application monitoring, and operational intelligence use cases.

This Kibana distribution is provided by the upstream Kibana packaging
team.

## Usage

Run a temporary container with the Kibana

```
docker run --rm -it -p 5601:5601 sourcemation/kibana
```

### Advanced usage examples

Run Kibana with persistent storage

```
docker run -d --name kibana \
  -p 5601:5601 \
  -v /path/to/your/data:/usr/share/kibana/data \
  sourcemation/kibana
```

Run with a custom configuration file

```
docker run -d --name kibana \
  -p 5601:5601 \
  -v /path/to/your/kibana.yml:/usr/share/kibana/config/kibana.yml \
  -v /path/to/your/data:/usr/share/kibana/data \
  sourcemation/kibana
```

## Image tags and versions

The `sourcemation/kibana` image itself comes in `debian-12` flavor.
The tag `latest` refers to the Debian-based flavor.

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
KIBANA_HOME=/usr/share/kibana
```

This image exposes the following ports: 

- 5601 - Kibana web interface and API

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the SourceMation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/kibana` image is not affiliated with
the Kibana. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/kibana` image is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [SourceMation
platform](https://sourcemation.com/).

For more information, check out the [overview of
Kibana](https://www.elastic.co/kibana) page.

### Licenses

The base license for the solution (Kibana) is the
[Elastic License 2.0](https://www.elastic.co/licensing/elastic-license). The licenses for each component shipped as
part of this image can be found on [the image's appropriate SourceMation
entry](https://sourcemation.com/).
