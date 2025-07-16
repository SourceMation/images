# Python packaged by SourceMation

Python is one of the most popular programming languages. Its simplicity,
emphasis on readability and a dozen of modules make it the perfect choice for
various work domains, ranging from web development to AI/ML.

This Python distribution is provided by the downstream Rocky Linux 9
packaging team in the version respective to that system (3.9.18). For
user convenience, the pip package manager is shipped as well.

## Usage

Run a temporary container with the Python REPL (don't forget the `-it`
argument).

```bash
docker run --rm -it sourcemation/python:latest
```

To run the shell in the container, use the following command:

```bash
docker run --rm -it sourcemation/python:latest
```
### Advanced usage examples

Serve the contents of the current directory with Python's builtin HTTP
server with the port 8000 forwarded:

```bash
docker run --rm -p 8000:8000 -v "${PWD}:/your-project" -w "/your-project" -it sourcemation/python:latest python3 -m http.server 8000
```

Build an MkDocs project from the current directory and serve it:

```
docker run --rm -p 8000:8000 -v "${PWD}:/your-project" -w "/your-project" -it sourcemation/python:latest sh -c 'pip3 install -r requirements.txt && mkdocs build && mkdocs serve'
```

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
APP_VERSION="3.9.X - set during build"
APP_NAME="python"
```

This image exposes the following ports:

- 8000 : the default Python's http.server port

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

## Contributing and Reporting Issues

Your contributions are valued! Feel free to suggest enhancements or request new
images by opening an issue, or submit your own contributions via pull requests
to the SourceMation GitHub repository.

- [Creating issues (bugs) and images requests](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/python` image is not affiliated with
the Python Software Foundation. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/python` image is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [SourceMation
platform](https://www.sourcemation.com/products/b9c4054f-f7f7-4e2e-83ea-f764e723cea2/report).

For more information, check out the [overview on the
Python](https://www.python.org/doc/essays/blurb/) page.

### Licenses

The base license for the solution (Python) is the [Python
License](https://docs.python.org/3.9/license.html). The licenses for
each component shipped as part of this image can be found on [the
image's appropriate SourceMation
entry](https://www.sourcemation.com/products/b9c4054f-f7f7-4e2e-83ea-f764e723cea2/report).

