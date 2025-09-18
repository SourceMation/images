# Elasticsearch packaged by SourceMation

> Elasticsearch is a distributed, free and open search and analytics engine for all types of data, including textual, numerical, geospatial, structured, and unstructured.

This Elasticsearch distribution is provided by the upstream Elasticsearch packaging
team.

## Usage

Run a temporary container with the Elasticsearch

```
docker run --rm -it -p 9200:9200 -p 9300:9300 sourcemation/elasticsearch
```

### Advanced usage examples

Run Elasticsearch with persistent storage

```
docker run -d --name elasticsearch \
  -p 9200:9200 -p 9300:9300 \
  -v /path/to/your/data:/usr/share/elasticsearch/data \
  -v /path/to/your/logs:/usr/share/elasticsearch/logs \
  sourcemation/elasticsearch
```

Run with a custom configuration file

```
docker run -d --name elasticsearch \
  -p 9200:9200 -p 9300:9300 \
  -v /path/to/your/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml \
  -v /path/to/your/data:/usr/share/elasticsearch/data \
  sourcemation/elasticsearch
```

## Image tags and versions

The `sourcemation/elasticsearch` image itself comes in `debian-12` flavor.
The tag `latest` refers to the Debian-based flavor.

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ELASTICSEARCH_HOME=/usr/share/elasticsearch
```

This image exposes the following ports: 

- 9200 - HTTP REST API
- 9300 - Transport protocol for node-to-node communication

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the SourceMation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/elasticsearch` image is not affiliated with
the Elasticsearch. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/elasticsearch` image is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [SourceMation
platform](https://sourcemation.com/).

For more information, check out the [overview of
Elasticsearch](https://www.elastic.co/elasticsearch) page.

### Licenses

The base license for the solution (Elasticsearch) is the
[Elastic License 2.0](https://www.elastic.co/licensing/elastic-license). The licenses for each component shipped as
part of this image can be found on [the image's appropriate SourceMation
entry](https://sourcemation.com/).
