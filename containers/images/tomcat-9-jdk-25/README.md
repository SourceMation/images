# Apache Tomcat 9 on JDK 25 Container

This container image provides Apache Tomcat 9 based on JDK 25 (Sourcemation).

## Features

- Apache Tomcat 9.0.x
- JDK 25 (Adoptium Temurin)
- Tomcat Native (APR) support
- CA certificates injection via `sourcemation/jdk-25` entrypoint

## Usage

### Running the container

```bash
docker run -d -p 8080:8080 sourcemation/tomcat-9:latest
```

### Customizing configuration

You can mount your own configuration to `/usr/local/tomcat/conf`:

```bash
docker run -d \
  -v ./my-server.xml:/usr/local/tomcat/conf/server.xml \
  -p 8080:8080 \
  sourcemation/tomcat-9:latest
```

### Deploying applications

Mount your `.war` files to `/usr/local/tomcat/webapps`:

```bash
docker run -d \
  -v ./my-app.war:/usr/local/tomcat/webapps/my-app.war \
  -p 8080:8080 \
  sourcemation/tomcat-9:latest
```

## Environment Variables

- `CATALINA_OPTS`: Options passed to Tomcat startup.
- `JAVA_OPTS`: Options passed to the JVM.
- `USE_SYSTEM_CA_CERTS`: If set, the entrypoint will import CA certificates from `/certificates`.

## License

Apache-2.0
