# Java Development Kit (JDK) 17 Container Image

This Docker image provides the Java Development Kit (JDK) 17 from the Eclipse 
Temurin project, based on the OpenJDK implementation. It includes the Java 
Runtime Environment (JRE) plus essential development tools for building, 
testing, and deploying Java applications.

Built on Sourcemation's optimized Debian 13 Slim base, this lightweight Docker 
image delivers a secure and efficient JDK 17 installation with minimal footprint 
and enhanced security features.

Use this container image to run and build Java applications as a reliable 
drop-in replacement for the Eclipse Temurin JDK 17 image.

## Getting Started

To quickly run the JDK 17 Docker image with default settings, use the following 
command:


This launches an interactive shell inside a container with JDK 17 fully 
installed and ready for development.

## Advanced Usage Scenarios

### Running a Java Application

Here's how to run a pre-built Java application using this JDK 17 container 
image with a simple Dockerfile:

```Dockerfile
from sourcemation/jdk-17

# Copy your Java application JAR file into the image
COPY your-application.jar /app/your-application.jar
# Set the working directory
WORKDIR /app
# Run the Java application
CMD ["java", "-jar", "your-application.jar"]
```

Alternatively, execute your Java application directly from the command line 
using a volume mount:

```bash
docker run -it --rm -v /path/to/your/application:/app sourcemation/jdk-17 java -jar /app/your-application.jar
```

Lastly, to add custom CA certificates, you can mount a volume (or copy
it to the image during the Containerfile/Dockerfile build) and set the
USE\_SYSTEM\_CA\_CERTS environment variable to 1:

```bash
docker run -v /home/dev/mycerts:/certificates/ -e USE\_SYSTEM\_CA\_CERTS=1 sourcemation/jdk-17
```

```dockerfile
FROM sourcemation/jdk-17
# Copy your CA certificates into the image
COPY mycerts /certificates/
# Set the environment variable to use system CA certificates
ENV USE_SYSTEM_CA_CERTS=1
# Set the working directory
WORKDIR /app
# Run the Java application
CMD ["java", "-jar", "your-application.jar"]
```

### Running Java Applications as Non-Root User

For enhanced security, we recommend running your Java application as a 
non-root user. Create a dedicated user account and execute your application 
with reduced privileges using this Dockerfile example:

```dockerfile
FROM sourcemation/jdk-17

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

### Compiling and Running Java Applications

This example demonstrates how to compile a Java source file and then run the
resulting class file within the container.

Create a `Dockerfile`:

```dockerfile
FROM sourcemation/jdk-17

# Create a directory for the application source
WORKDIR /app

# Copy the Java source file into the container
COPY MyApp.java .

# Compile the Java source file
RUN javac MyApp.java

# Command to run the compiled Java application
CMD ["java", "MyApp"]
```

Create a simple Java application file named `MyApp.java`:

```java
public class MyApp {
    public static void main(String[] args) {
        System.out.println("Hello from JDK 17!");
    }
}
```

Build the Docker image:

```bash
docker build -t myjdkapp .
```

Run the Docker image:

```bash
docker run --rm myjdkapp
```

This will output:

```
Hello from JDK 17!
```

## Environment Variables Configuration

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
the Temurin JDK 17 image. **This image runs as the root user\! You should
extend it to run your application as a non-root user.**

## Contributing and Support

We value community contributions! Whether you have feature requests, bug 
reports, or wish to submit pull requests with improvements, you can engage 
with us through the official Sourcemation GitHub repository.

- [Open a new issue (for feature requests, bug reports, or image requests)](https://github.com/Sourcemation/images/issues/new/choose)
- [Submit a pull request](https://github.com/Sourcemation/images/compare)


## Extra Information

### About Sourcemation

Sourcemation delivers enterprise-grade open-source Docker images and container 
solutions with comprehensive security risk assessment. We maintain high-quality, 
production-ready container images. Detailed vulnerability analysis and compliance 
reports for our images are accessible through the 
[Sourcemation platform](https://www.sourcemation.com/).

### License

The OpenJDK project is licensed under the GNU General Public License, version 2, with the Classpath Exception.