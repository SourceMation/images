# Python 3.13 packaged by SourceMation

Python is one of the most popular programming languages. Its simplicity,
emphasis on readability and a dozen of modules make it the perfect choice for
various work domains, ranging from web development to AI/ML.

This Python distribution is compiled from fresh sources by the SourceMation
automation team. The version is 3.13.X and it's regularly updated to the latest
patch version. For user convenience, the pip package manager is shipped as well.

The base image is the latest, at the time of the build,
sourcemation/debian-13-slim image. It's gives you fully independent and
self-contained Python environment, that is regrulary updated and patched.
Lastly the build process takes advantage of cryptographic signatures to ensure
that the source code is not tampered with.

## Usage

Run a temporary container with the Python REPL (don't forget the `-it`
argument).

```bash
docker run --rm -it sourcemation/python-3.13:latest
```

To run the shell in the container, use the following command:

```bash
docker run --rm -it sourcemation/python-3.13:latest
```

### Advanced usage examples

Serve the contents of the current directory with Python's builtin HTTP server
with the port 8000 forwarded:

```bash
docker run --rm -p 8000:8000 -v "${PWD}:/your-project" -w "/your-project" -it sourcemation/python-3.13:latest python3 -m http.server 8000
```

Build an MkDocs project from the current directory and serve it, this time with podman:

```bash
podman run --rm -p 8000:8000 -v "${PWD}:/your-project" -w "/your-project" -it sourcemation/python-3.13:latest sh -c 'pip3 install -r requirements.txt && mkdocs build && mkdocs serve'
```


## Most important environment variables

This image uses the following environment variables:

```
PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
PYTHON_VERSION=3.13.X # example: 3.13.2
```

## Ports

This image does not expose any ports. However, you can expose the ports you
need by using the `-p` option, setting up the ports manually, or with
kubernetes or docker-compose. You can also create an image with the ports
exposed by default.

## Contributing and Reporting Issues

Your contributions are valued! Feel free to suggest enhancements or request new
images by opening an issue, or submit your own contributions via pull requests
to the SourceMation GitHub repository.

- [Creating issues (bugs) and images requests](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/python-3.13` image is not affiliated with the
Python Software Foundation. The respective companies and organisations own the
trademarks mentioned in the offering. The `sourcemation/python-3.13` image is a
separate project and is maintained by [SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of our images and its components might be found
on the [SourceMation
platform](https://www.sourcemation.com/).


However, not all images have a risk analysis report yet. If you need additional
software components or have any questions, please contact us.

### Licenses

The base license for the solution (Python) is the [Python
License](https://docs.python.org/3.13/license.html).

