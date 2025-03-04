# Mosquitto packaged by SourceMation

This container image contains the Mosquitto MQTT broker and client tools
installed from EPEL repositories.

## Running the container

Additional information to keep in mind

### Using custom configuration

1. Set your custom configuration file in the `mosquitto.conf` file.
2. Mount your configuration file to the `/etc/mosquitto/mosquitto.conf` location:
   ```bash
   docker ... -v mosquitto.conf:/etc/mosquitto/mosquitto.conf ...
   ```

### Data persistence

1. Add the proper config lines into the `mosquitto.conf` file:
   ```ini
   persistence true
   persistence_location /mosquitto/data/
   ```
2. Mount the `/mosquitto/data/` directory to the host filesystem:
   ```bash
   docker ... -v mosquitto-data:/mosquitto/data ...
   ```

### Logging

By default, mosquitto logs are captured/written to standard system logs (systemd
journal). You can change this behavior by adding the following line to the
`mosquitto.conf` file:

```ini
log_dest file DEST
```

You can use the previously mentioned `/mosquitto/` directory to store logs. For example:

```ini
log_dest file /mosquitto/log/mosquitto.log
```

Packaged mosquitto also has access to /var/log/mosquitto directory so you can use it as well:

```ini
log_dest file /var/log/mosquitto/mosquitto.log
```

Note that only one log destination can be used at a time.

---

Then, you can start the container with the following option:

```bash
docker ... -v mosquitto-log:/mosquitto/log ...
```

or similar package default:

```bash
docker ... -v mosquitto-log:/var/log/mosquitto ...
```

### Practical examples

To run a temporary container with default configuration, execute the following
command:

```bash
docker run --rm --name el9-mosquitto -p 1883:1883 sourcemation/mosquitto:latest
```

**The `/mosquito/logs` and `/mosquito/data` directories were added, and the
proper permissions were set for ease of modification. It’s similar to the
Eclipse Foundation Original image except for the standard configuration
residing in the `/etc/mosquito/mosquito.conf` instead of
`/mosquito/config/mosquitto.conf`**

To run the container with custom configuration, logging and data persistence
properly configured, execute the following command:

```bash
docker run --name el9-mosquitto -p 1883:1883 -v mosquitto.conf:/etc/mosquitto/mosquitto.conf -v DATA_PATH:/mosquitto/data -v LOG_PATH:/mosquitto/log sourcemation/mosquitto:latest
```

Where `mosquitto.conf` is your custom configuration file, `DATA_PATH` is the
path to the directory where you want to store mosquitto data and, `LOG_PATH` is
the path to the directory where you want to store mosquitto logs.

Example custom configuration file:

```ini
persistence true
persistence_location /mosquitto/data/
log_dest file /mosquitto/log/mosquitto.log
# Log types = debug, error, warning, notice, information, none, subscribe, unsubscribe, websockets, all
log_type information
log_type notice
log_type subscribe
log_type unsubscribe
log_type warning
log_type error
```

Please note that you can override the default configuration file located at
`/etc/mosquitto/mosquitto.conf` by mounting your own configuration file at this
location with `-v` option like this:

```bash
docker ... -v mosquitto.conf:/mosquitto/config/mosquitto.conf ...
```

Lastly by adding the `-d` option you can run the container in the background.

```bash
docker run -d --name el9-mosquitto ...
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
APP_VERSION="XXX - set during build"
APP_NAME="mosquitto"
```

This image exposes the following ports:

- 1883 : default port for unencrypted, unauthenticated MQTT connections

Please note that the ports need to be either manually forwarded with the `-p`
option, like in the examples above, or let Docker choose some for you with the
`-P` option.

## Contributing and Issues

We’d love for you to contribute! You can request new features by
creating an issue or submitting a pull request with your contribution to
this image on the SourceMation GitHub repository.

[Creating issues and images requests](https://github.com/SourceMation/images/issues/new/choose)
[Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/mosquitto` image is not affiliated with the
The Eclipse Foundation. The respective companies and organisations own the
trademarks mentioned in the offering. The `sourcemation/mosquitto` image is a
separate project and is maintained by [SourceMation](https://sourcemation.com).

## Extra notes

1. Mosquitto is running as a non-root user `mosquitto` with UID/GID 984:985
2. **Mosquitto will not start if log or data directories are not writable by
   the `mosquitto` user. It will also not create these directories even if
   proper permissions on parent directories are set.**  If you want to use
   directories different from the one provided in this short guide, you must
   create them manually and set proper permissions.
3. The Eclipse Foundation Original image is available at [Docker
   Hub](https://hub.docker.com/_/eclipse-mosquitto). The guide for their image
   recommends adding the useless `9001` port, which requires additional
   configuration to work properly (it's not mentioned in their image guide).
4. Mosquitto configuration file in pristine form is always available in
   container at `/etc/mosquitto/mosquitto.conf`.

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on
the SourceMation platform.

For more information, check out the [official Mosquitto
website](https://mosquitto.org/).

### Licenses

The base licenses for the solution (Eclipse Mosquitto) are the [Eclipse Public
License 2.0 and the Eclipse Distribution License
1.0](https://github.com/eclipse-mosquitto/mosquitto/blob/master/LICENSE.txt).
The licenses for each component shipped as part of this image can be found on
the image's appropriate SourceMation entry.
