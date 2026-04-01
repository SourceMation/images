# Apache Tomcat 10 on JRE 25 Container

This container image provides Apache Tomcat 10 based on JRE 25 (Sourcemation).

## Features

- Apache Tomcat 10.1.x
- JRE 25 (Adoptium Temurin)
- Tomcat Native (APR) support
- CA certificates injection via `sourcemation/jre-25` entrypoint

## Usage

### Running the container

```bash
docker run -d -p 8080:8080 sourcemation/tomcat-10:latest
```

## License

Apache-2.0
