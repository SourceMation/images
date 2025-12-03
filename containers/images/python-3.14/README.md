# Python 3.14 packaged by Sourcemation

Python is a top choice among programming languages, valued for its clear
syntax, focus on readability, and extensive module ecosystem. It excels across
many fields, from web development to artificial intelligence and machine
learning.

This container provides a Python 3.14.X environment, built from the latest sources by the Sourcemation
automation team. Updates are applied regularly to ensure the newest patch version is included, and pip
is pre-installed for package management.

The image is based on the most recent `sourcemation/debian-13-slim` release
available at build time, offering a fully isolated and frequently maintained
Python setup. Additionally, cryptographic signatures are used during the build
to verify the integrity of the source code.

## Usage

Run a temporary container with the Python REPL (remember about `-it` argument).
**One of the new cool features in Python 3.14 are colors in the REPL!**

```bash
docker run --rm -it sourcemation/python-3.14:latest
```

To run the shell in the container, use the following command:

```bash
docker run --rm -it sourcemation/python-3.14:latest /bin/bash
```

### Advanced usage examples

Serve the contents of the current directory with Python's builtin HTTP server
with the port 8000 forwarded:

```bash
docker run --rm -p 8000:8000 -v "${PWD}:/your-project" -w "/your-project" -it sourcemation/python-3.14:latest python3 -m http.server 8000
```

Build an MkDocs project from the current directory and serve it, this time with podman:

```bash
podman run --rm -p 8000:8000 -v "${PWD}:/your-project" -w "/your-project" -it sourcemation/python-3.14:latest sh -c 'pip3 install -r requirements.txt && mkdocs build && mkdocs serve'
```


## Most important environment variables

This image uses the following environment variables:

```
PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
PYTHON_VERSION=3.14.X # example: 3.14.0
```

## Ports

This image does not expose any ports. However, you can expose the ports you
need by using the `-p` option, setting up the ports manually, or with
kubernetes or docker-compose. You can also create an image with the ports
exposed by default.

## Contributing and Reporting Issues

Your contributions are valued! Feel free to suggest enhancements or request new
images by opening an issue, or submit your own contributions via pull requests
to the Sourcemation GitHub repository.

- [Creating issues (bugs) and images requests](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/python-3.14` image is not affiliated with the
Python Software Foundation. The respective companies and organisations own the
trademarks mentioned in the offering. The `sourcemation/python-3.14` image is a
separate project and is maintained by [Sourcemation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of our images and its components might be found
on the [Sourcemation
platform](https://www.sourcemation.com/).


However, not all images have a risk analysis report yet. If you need additional
software components or have any questions, please contact us.

### Licenses

The base license for the solution (Python) is the [Python
License](https://docs.python.org/3.14/license.html).

