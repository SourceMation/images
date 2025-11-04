# Java Runtime Environment (JRE) 17

This image provides the Java Runtime Environment (JRE) 17 from the Eclipse
Temurin project, built as a compilation of the OpenJDK project.

This optimized Docker image offers a clean and lightweight JRE 17 installation.
Built on Sourcemation's streamlined Debian 13 Slim base, it ensures minimal
resource usage and improved security.

This image serves as a drop-in replacement for the Temurin JRE 17 image.

## Getting Started

To run the base image with default settings, use the following command:

```bash
docker run -it --rm --name jre17 sourcemation/jre-17
```

This launches a shell within a container that has JRE 17 installed and ready
for use.

## Advanced Usage Scenarios
Running a Java Application

This Dockerfile example shows how to execute a Java application with the
JRE 17 image:

```dockerfile
from sourcemation/jre-17

# Copy your Java application JAR file into the image
COPY your-application.jar /app/your-application.jar
# Set the working directory
WORKDIR /app
# Run the Java application
CMD ["java", "-jar", "your-application.jar"]
```

Alternatively, execute a Java application directly via command line by mounting
a volume:

```bash
docker run -it --rm -v /path/to/your/application:/app sourcemation/jre-17

java -jar /app/your-application.jar
```

For adding custom CA certificates, mount a volume (or copy certificates
during the Containerfile/Dockerfile build) and configure the
USE_SYSTEM_CA_CERTS environment variable to 1:

```bash
docker run -v /home/dev/mycerts:/certificates/ -e USE_SYSTEM_CA_CERTS=1 sourcemation/jre-17
```

```Dockerfile
FROM sourcemation/jre-17
# Copy your CA certificates into the image
COPY mycerts /certificates/
# Set the environment variable to use system CA certificates
ENV USE_SYSTEM_CA_CERTS=1
# Set the working directory
WORKDIR /app
# Run the Java application
CMD ["java", "-jar", "your-application.jar"]
```

### Creating a new user and run application

To enhance security, it is recommended to run your Java application as a
non-root user. To create a new user and run your application as that user, you
can use the following dockerfile

```dockerfile
FROM sourcemation/jre-17

# Create a new user
RUN useradd -m -s /bin/bash myuser
# Copy your Java application JAR file into the image
COPY your-application.jar /app/your-application.jar
# Set the working directory
WORKDIR /app
# Change ownership of the application files
RUN chown -R myuser:myuser /app
# Switch to the new user
USER myuser
# Run the Java application
CMD ["java", "-jar", "your-application.jar"]
```

## Key Environment Variables

Standard encoding is set to en_US.UTF-8, and other locale variables default
to en_US. JAVA_VERSION can help you identify the Java version, and
JAVA_HOME is set to /opt/java/openjdk.

```bash
JAVA_VERSION=jdk-17.0.17+10 # or a newer version depending on the build
JAVA_HOME=/opt/java/openjdk
PATH=$JAVA_HOME/bin:$PATH
# Encoding
LANG='en_US.UTF-8'
LANGUAGE='en_US:en'
LC_ALL='en_US.UTF-8'
```

## Important Considerations

This image was created with the intention of being a drop-in replacement for
the Temurin JRE 17 image. **This image runs as the root user! You should
extend it to run your application as a non-root user.**

## Contributing and Issues

We welcome your contributions! If you have new feature requests, want to report
a bug, or wish to submit a pull request with your code or an image request, you
can do so via the Sourcemation GitHub repository for this image.

- [Open a new issue (for feature requests, bug reports, or image requests)](https://github.com/Sourcemation/images/issues/new/choose)
- [Submit a pull request](https://github.com/Sourcemation/images/compare)

## Extra Information

### Sourcemation

Sourcemation offers a range of open-source projects and Docker images with
extensive risk assessment of open-source software. We are committed to providing
high-quality images. Comprehensive risk analysis reports for selected images
are available on the [Sourcemation platform](https://www.sourcemation.com/catalog/jre-17).

### License

The OpenJDK project is licensed under the GNU General Public License, version
2, with the Classpath Exception.
