# Apache Tomcat 10.1 Container on Debian 13 Slim packed by Sourcemation

This image, `sourcemation/tomcat-10`, provides a robust and secure **Apache Tomcat 10.1** environment built on a minimal Debian 13 Slim base. It is designed for modern Java applications using the `jakarta.*` namespace (Jakarta EE 10).

Maintained by the Sourcemation automation team, this Tomcat distribution is regularly updated to ensure it's current, secure, and compact. It includes **Tomcat Native (APR)** support for high-performance production workloads and integrates with Sourcemation's CA certificate injection system.

-----

## Core Features

*   **Specification Support:**
    *   **Servlet Spec:** 6.0
    *   **JSP Spec:** 3.1
    *   **EL Spec:** 5.0
    *   **WebSocket Spec:** 2.1
    *   **Authentication Spec:** 2.0
*   **Runtime:** JRE 25 (Adoptium Temurin) provided by `sourcemation/jre-25`.
*   **Performance:** Built with **Tomcat Native (APR) 2.x** library for optimized I/O.
*   **Security:** Minimal attack surface, verified builds, and support for automated CA certificate management.

-----

## Operational Use

### Running the container

To start a basic Tomcat instance:

```bash
docker run -d -p 8080:8080 sourcemation/tomcat-10:latest
```

### Deploying Applications

#### 1. Mounting Applications
Instead of creating a new image for every code change, you can mount your `.war` file or application directory from the host to the container:

```bash
docker run -d \
  -v ./my-app.war:/usr/local/tomcat/webapps/my-app.war:ro \
  -p 8080:8080 \
  sourcemation/tomcat-10:latest
```

#### 2. Custom Dockerfiles
For production, it is recommended to "bake" the application into the image:

```dockerfile
FROM sourcemation/tomcat-10:latest
COPY my-app.war /usr/local/tomcat/webapps/
```

### Custom Configuration

You can customize Tomcat's behavior by mounting configuration files over the defaults in `/usr/local/tomcat/conf/`:

```bash
docker run -d \
  -v ./server.xml:/usr/local/tomcat/conf/server.xml:ro \
  -p 8080:8080 \
  sourcemation/tomcat-10:latest
```

-----

## Key Environment Variables

*   **`CATALINA_OPTS`**: Options passed to the Tomcat startup command. Recommended for memory settings (e.g., `-Xmx1G`).
*   **`JAVA_OPTS`**: Options passed to the JVM.
*   **`USE_SYSTEM_CA_CERTS`**: If set to `true`, the container will automatically import CA certificates from the `/certificates` directory into the Java truststore.

-----

## Port Exposure

The default Tomcat port **8080** is exposed.

-----

## Security Notes

*   **Default Webapps:** For security, the default Tomcat applications (ROOT, docs, examples, etc.) have been moved to `/usr/local/tomcat/webapps.dist`. The `/usr/local/tomcat/webapps` directory is empty by default to reduce the attack surface.
*   **Non-Root Execution:** This image is designed to be compatible with non-root execution. In production, it is a best practice to run the Tomcat process as a non-privileged user.
*   **Logging:** Tomcat logs to standard output (`stdout`) by default, allowing `docker logs` to capture all relevant information.

-----

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or submit a pull request with your contribution to this image on the Sourcemation GitHub repository.

*   [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
*   [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/tomcat-10` image is not affiliated with the Apache Software Foundation. The respective companies and organisations own the trademarks mentioned in the offering. The `sourcemation/tomcat-10` image is a separate project and is maintained by [Sourcemation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A comprehensive risk analysis report detailing the image and its components can be accessed on the [Sourcemation platform](https://www.sourcemation.com/).

### Licenses

The base license for Apache Tomcat is the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).
