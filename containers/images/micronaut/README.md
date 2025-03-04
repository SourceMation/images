# Micronaut CLI packaged by SourceMation

This image contains the Micronaut CLI, Java-21 GraalVM, and SDKMAN on Rocky
Linux 9. This allows you to build and run Micronaut applications using GraalVM.
Everything is installed with SDKMAN, so you can easily switch between different
versions of Java.

## Usage

First, run a container with a shell:

```
$ docker run -p 8080:8080 --rm -it sourcemation/micronaut:latest
```

Being inside the container, create a new Micronaut application:

```
$ mn create-app example.sourcemation.testapp --build=maven --lang=java
```

Then, go to the application's directory, run tests to check if everything is OK
and build a native-image application.

```
$ cd testapp
$ ./mvnw test
$ ./mvnw package -Dpackaging=native-image
```

After running these commands inside your local container, run the application
with `/home/micronaut/testapp/target/testapp`. Example listing:

```
[micronaut@664a3ed677a9 testapp]$ /home/micronaut/testapp/target/testapp
 __  __ _                                  _   
|  \/  (_) ___ _ __ ___  _ __   __ _ _   _| |_ 
| |\/| | |/ __| '__/ _ \| '_ \ / _` | | | | __|
| |  | | | (__| | | (_) | | | | (_| | |_| | |_ 
|_|  |_|_|\___|_|  \___/|_| |_|\__,_|\__,_|\__|
20:54:19.413 [main] INFO  io.micronaut.runtime.Micronaut - Startup completed in 15ms. Server Running: http://664a3ed677a9:8080
```

## Environment Vars, Ports, Volumes

This image exposes the following ports: 

- 8080 : the default Micronaut HTTP server port

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

## Contributing and Issues

We’d love for you to contribute! You can request new features by
creating an issue or submitting a pull request with your contribution to
this image on the SourceMation GitHub repository.

[Creating issues and images requests](https://github.com/SourceMation/images/issues/new/choose)
[Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/micronaut` image is not affiliated with the
Micronaut Foundation. The respective companies and organisations own the
trademarks mentioned in the offering. The `sourcemation/micronaut` image is a
separate project and is maintained by [SourceMation](https://sourcemation.com).

## Extra notes

The base image user is `micronaut`, and the working directory is
`/home/micronaut`.

The native images require the `gcc`, `glibc-devel` and `zlib-devel`; they are
installed in this image by default.

This image does **not** have the `JAVA_HOME` variable set.

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on
the SourceMation platform.

For more information, check out the [official Micronaut
website](https://micronaut.io/), and the "[Creating your first Micronaut
app](https://guides.micronaut.io/latest/creating-your-first-micronaut-app.html)"
guide.

### Licenses

The base license for the solution (Micronaut version 4.5.1) is the [Apache
License, Version
2.0](https://github.com/micronaut-projects/micronaut-core/blob/4.5.x/LICENSE).
The licenses for each component shipped as part of this image can be found on
the image's appropriate SourceMation entry.

