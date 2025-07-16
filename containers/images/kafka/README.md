# Apache Kafka packaged by SourceMation

Kafka is a utility for managing, transforming, forwarding and appropriately
reacting to data being streamed as events. Comparable to other message brokers,
Kafka's durability make it a great choice for software, that processes messages
at a large scale.

This image is based on the official Apache Kafka image. It is built for
SourceMation content delivery and open source analysis platform.

## Usage

Run a temporary container with the Apache Kafka broker:

```
docker run --rm -d --name kafka-broker -it sourcemation/kafka:latest
```

### Advanced usage examples

Simple commands to create topics and produce/consume messages:

Create a topic with the name *test*:

```
./kafka-topics.sh --bootstrap-server localhost:9092 --create --topic test
```

Send the message 'Hi mom!' to the topic *test*:

```
echo 'Hi mom!' | ./kafka-console-producer.sh --bootstrap-server localhost:9092 --topic test
```

Consume messages from the topic *test* (Use Ctrl+C to stop):

```
./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
```

## Environment Vars, Ports, Volumes

This image exposes the following ports: 

- 9092 : the default Kafka port for listeners

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

This image has the following volumes set:

- /var/lib/kafka/data
- /mnt/shared/config
- /etc/kafka/secrets

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the SourceMation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/kafka` image is not affiliated with the
Apache Software Foundation. The respective companies and organisations own the
trademarks mentioned in the offering. The `sourcemation/kafka` image is a
separate project and is maintained by [SourceMation](https://sourcemation.com).

## Extra notes

The image is based on the [Apache Kafka Official Docker
Image](https://hub.docker.com/r/apache/kafka). For more information and
advanced use cases consult that image's documentation.

Our image has set the `WORKDIR` to `/opt/kafka/bin`. You can skip the
`--workdir /opt/kafka/bin` option.

The Kafka server runs as the system user `appuser`, UID and GID 1000.

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on
the SourceMation platform.

For more information about Kafka, check out the [Apache Kafka
Introduction](https://kafka.apache.org/intro) page. For more advanced usage
examples, check out the [Apache Kafka
Quickstart](https://kafka.apache.org/quickstart) page.

### Licenses

The base license for the solution (Apache Kafka 3.9.0) is the [Apache License,
Version 2.0](https://github.com/apache/kafka/blob/3.9.0/LICENSE-binary). Please
visit that link for a more in-depth information about the licensing of the
third-party components used as part of the upstream product. The licenses for
additional components shipped as part of this image can be found on the image's
appropriate SourceMation entry.
