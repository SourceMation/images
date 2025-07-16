# Java packaged by SourceMation

Java is an industry-standard, robust, object-oriented programming language
widely used for enterprise software development.

This image ships the OpenJDK implementation, version 21, and Maven 3.8, all
provided by the downstream Rocky Linux 9 packaging team.

## Usage

Run a temporary container with the Java installation:

```
docker run --rm -it sourcemation/java:latest
```

### Advanced usage examples

To create and run a simple project with Maven, run the following commands
inside your container:

```
$ mkdir -p hello-world/src/{main,test}/java/com/mycompany/

$ echo '<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.mycompany</groupId>
    <artifactId>hello-world</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
    </properties>

    <dependencies>
    </dependencies>

</project>' > hello-world/pom.xml

$ echo 'package com.mycompany;

public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello world");
    }
}' > hello-world/src/main/java/com/mycompany/HelloWorld.java

$ cd hello-world/

$ mvn compile

$ mvn exec:java -Dexec.mainClass="com.mycompany.HelloWorld"
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
JAVA_HOME="/usr/lib/jvm/java-21"
APP_NAME="java"
LANG="en_US.UTF-8"
LANGUAGE="en_US:en"
```

## Contributing and Issues

We welcome your contributions! If you have new feature requests, want to report
a bug, or wish to submit a pull request with your code or an image request, you
can do so via the SourceMation GitHub repository for this image.

- [Open a new issue (for feature requests, bug reports, or image requests)](https://github.com/SourceMation/images/issues/new/choose)
- [Submit a pull request](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/java` image is not affiliated with Oracle,
Inc. or the OpenJDK community. The respective companies and organisations own
the trademarks mentioned in the offering. The `sourcemation/java` image is a
separate project and is maintained by [SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on
the [SourceMation
platform](https://sourcemation.com/products/f10b4231-8a90-40c4-8475-65d7aeb1368a/deployments).

For more information, check out the [official OpenJDK
website](https://openjdk.org/).

### Licenses

The base license for the solution (OpenJDK 21) is the [GPLv2+CPE (GPLv2 with
Classpath Exception)
license](https://github.com/openjdk/jdk21/blob/master/LICENSE). The licenses
for each component shipped as part of this image can be found on [the image's
appropriate SourceMation
entry](https://sourcemation.com/products/f10b4231-8a90-40c4-8475-65d7aeb1368a/deployments).
