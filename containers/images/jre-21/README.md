# Java Runtime Environment (JRE) 21

This image contains the Java Runtime Environment (JRE) 21 from the Eclipse
Temurin project, which in this case is a compilation of the OpenJDK project.

This carefully crafted Docker image delivers a pristine and lightweight
installation of JRE 21. It is built upon SourceMation’s optimized Debian 12 Slim
base, ensuring a minimal footprint and enhanced security.

This image was built to be a drop-in replacement for the Temurin JRE 21 image.

## Getting Started

To run the base image without any additional configuration, you can use the
following:

```bash
docker run -it --rm --name jre21 sourcemation/jre-21
```

This will start a shell inside a container with JRE 21 installed and ready to
use.

## Advanced Usage Scenarios
Running a Java Application

The following Dockerfile demonstrates how to run a Java application using the
JRE 21 image:

```dockerfile
from sourcemation/jre-21

# Copy your Java application JAR file into the image
COPY your-application.jar /app/your-application.jar
# Set the working directory
WORKDIR /app
# Run the Java application
CMD ["java", "-jar", "your-application.jar"]
```

You can also run a Java application directly from the command line by mounting
the volume:

```bash
docker run -it --rm -v /path/to/your/application:/app sourcemation/jre-21

java -jar /app/your-application.jar
```

Lastly, to add custom CA certificates, you can mount a volume (or copy
it to the image during the Containerfile/Dockerfile build) and set the
USE_SYSTEM_CA_CERTS environment variable to 1:

```bash
docker run -v /home/dev/mycerts:/certificates/ -e USE_SYSTEM_CA_CERTS=1 sourcemation/jre-21
```

```Dockerfile
FROM sourcemation/jre-21
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
FROM sourcemation/jre-21

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
JAVA_VERSION=jdk-21.0.7+6 # or a newer version depending on the build
JAVA_HOME=/opt/java/openjdk
PATH=$JAVA_HOME/bin:$PATH
# Encoding
LANG='en_US.UTF-8'
LANGUAGE='en_US:en'
LC_ALL='en_US.UTF-8'
```

## Important Considerations

This image was created with the intention of being a drop-in replacement for
the Temurin JRE 21 image. **This image runs as the root user! You should
extend it to run your application as a non-root user.**

## Extra Information

## Sourcemation

Sourcemation offers a range of open-source projects and Docker images with
extensive risk assessment of open-source software. We are committed to providing
high-quality images. Comprehensive risk analysis reports for selected images
are available on the [SourceMation platform](https://www.sourcemation.com/).

## License

The OpenJDK project is licensed under the GNU General Public License, version 2, with the Classpath Exception.

