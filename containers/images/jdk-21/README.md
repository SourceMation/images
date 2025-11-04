# Java Development Kit (JDK) 21

This image contains the Java Development Kit (JDK) 21 from the Eclipse Temurin
project, which in this case is a compilation of the OpenJDK project. This
includes the Java Runtime Environment (JRE) and development tools necessary for
building, testing, and running Java applications.

This carefully crafted Docker image delivers a pristine and lightweight
installation of JDK 21. It is built upon Sourcemation’s optimized Debian 13 Slim
base, ensuring a minimal footprint and enhanced security.

This image can be used to both run and build Java applications, serving as a
drop-in replacement for the Temurin JDK 21 image.

## Getting Started

To run the base image without any additional configuration, you can use the
following:


This will start a shell inside a container with JDK 21 installed and ready to
use.

## Advanced Usage Scenarios

### Running a Java Application

The following Dockerfile demonstrates how to run a pre-built Java application
using the JDK 21 image:

```Dockerfile
from sourcemation/jdk-21

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
docker run -it --rm -v /path/to/your/application:/app sourcemation/jdk-21 java -jar /app/your-application.jar
```

Lastly, to add custom CA certificates, you can mount a volume (or copy
it to the image during the Containerfile/Dockerfile build) and set the
USE\_SYSTEM\_CA\_CERTS environment variable to 1:

```bash
docker run -v /home/dev/mycerts:/certificates/ -e USE\_SYSTEM\_CA\_CERTS=1 sourcemation/jdk-21
```

```dockerfile
FROM sourcemation/jdk-21
# Copy your CA certificates into the image
COPY mycerts /certificates/
# Set the environment variable to use system CA certificates
ENV USE_SYSTEM_CA_CERTS=1
# Set the working directory
WORKDIR /app
# Run the Java application
CMD ["java", "-jar", "your-application.jar"]
```

### Creating a new user and running application

To enhance security, it is recommended to run your Java application as a
non-root user. To create a new user and run your application as that user, you
can use the following dockerfile:

```dockerfile
FROM sourcemation/jdk-21

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

### Compiling and Running a Java Application

This example demonstrates how to compile a Java source file and then run the
resulting class file within the container.

Create a `Dockerfile`:

```dockerfile
FROM sourcemation/jdk-21

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
        System.out.println("Hello from JDK 21!");
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
Hello from JDK 21\!
```

## Key Environment Variables

Standard encoding is set to en\_US.UTF-8, and other locale variables default
to en\_US. JAVA\_VERSION can help you identify the Java version, and
JAVA\_HOME is set to /opt/java/openjdk.

```bash
JAVA\_VERSION=jdk-21.0.7+6 \# or a newer version depending on the build
JAVA\_HOME=/opt/java/openjdk
PATH=$JAVA\_HOME/bin:$PATH

# Encoding

LANG='en\_US.UTF-8'
LANGUAGE='en\_US:en'
LC\_ALL='en\_US.UTF-8'
```

## Important Considerations

This image was created with the intention of being a drop-in replacement for
the Temurin JDK 21 image. **This image runs as the root user\! You should
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
are available on the [Sourcemation platform](https://www.sourcemation.com/).

### License

The OpenJDK project is licensed under the GNU General Public License, version 2, with the Classpath Exception.
