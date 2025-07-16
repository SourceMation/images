# Maven packed by SourceMation

This image provides a ready-to-use environment for Apache Maven, a powerful
project management tool used primarily for Java projects. Maven can manage a
project's build, reporting and documentation from a central piece of
information.

Built upon a secure and lightweight sourcemation debian slim base image, this
Maven container allows you to easily build, test, and package your Java
projects without the need for local Maven installation.

## Getting Started

To quickly start a shell inside a container with Maven available in the PATH:

```bash
docker run -it --rm sourcemation/maven:latest /bin/bash
```

You can replace `latest` with a specific version tag.

## Advanced Usage Scenarios

### Building a Maven Project

To build a Maven project located on your host machine, you can mount your
project directory into the container:

```bash
docker run -it --rm -v /path/to/project:/usr/src/project -w /usr/src/project sourcemation/maven:latest mvn clean install
```

In this command:
- `-v /path/to/project:/usr/src/project` mounts your local project directory to `/usr/src/project` inside the container.
- `-w /usr/src/project` sets the working directory inside the container to the mounted project directory.
- `mvn clean install` executes the Maven build lifecycle goals.

### Running Maven Commands

You can execute any Maven command by appending it to the `docker run` command:

```bash
docker run -it --rm -v /path/to/project:/usr/src/project -w /usr/src/project sourcemation/maven:latest mvn dependency:tree
```

This example shows how to generate the dependency tree of your project.

### Using a Custom `settings.xml`

If you need to use a custom Maven `settings.xml` file (e.g., for configuring a
private repository), you can mount it into the container:

```bash
docker run -it --rm -v /path/to/your/settings.xml:/root/.m2/settings.xml -v /path/to/project:/usr/src/project -w /usr/src/project sourcemation/maven:latest mvn clean install
```

This mounts your local `settings.xml` to the default Maven configuration
directory inside the container, mounting your project directory as well and
running the `mvn clean install` command.

### Creating a New Maven Project

You can also use the Maven archetype plugin to generate a new project structure:

```bash
docker run -it --rm -v /path/to/output:/usr/src/out -w /usr/src/out your-maven-image-name mvn archetype:generate -DgroupId=com.example -DartifactId=my-new-app -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
```

This command will generate a basic Maven project in the `/path/to/output` directory on your host.

## Key Environment Variables

While this image aims to be straightforward, you might find these environment variables relevant:

- `MAVEN_CONFIG`: Specifies the location of the Maven configuration directory (defaults to `/root/.m2`).
- `MAVEN_HOME`: Points to the Maven installation directory (defaults to `/usr/share/maven`).
- `MAVEN_VERSION`: The version of Maven installed in the image (e.g., `3.9.9`).

## Important Considerations

- **User Context:** This image may run as the root user by default. For
  enhanced security in production environments, consider extending this image
  to run Maven as a non-root user. You can achieve this by adding user creation
  and switching instructions in your own Dockerfile.
- **Performance:** For frequent builds, consider using Docker volumes to
  persist the local Maven repository (`/root/.m2/repository`) to speed up
  dependency resolution.

## Contributions and Issue Reporting

Contributions are welcome! Propose new features by creating issues or submit
pull requests on the SourceMation GitHub repository.

- [Open a new issue (for feature requests, bug reports, or image requests)](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

## Extra information

For more details on Apache Maven, please refer to the official Maven documentation: https://maven.apache.org/.

### Sourcemation

Sourcemation offers a range of open-source projects and Docker images with
extensive risk assessment of open-source software. We are committed to providing
high-quality images. Comprehensive risk analysis reports for selected images
are available on the [SourceMation platform](https://www.sourcemation.com/).

### License

The Maven is licensed under the Apache License 2.0
