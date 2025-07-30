# Python 3.8 packaged by SourceMation
Python is one of the most popular programming languages, known for its
simplicity, readability, and extensive module ecosystem. It's a versatile
choice for a wide range of applications, from web development to AI/ML.

## Important Note: Python 3.8 is End-of-Life (EOL)

This Python distribution, version 3.8.X, is provided specifically for
compatibility workflows that require an older Python environment. **Python 3.8 is
no longer officially supported by the Python Software Foundation and does not
receive security updates.**

While the Python 3.8 environment itself is outdated, this SourceMation image is
built on our regularly updated and patched `sourcemation/debian-12-slim` base
image. This ensures that the underlying system components are current, even
though the Python version itself is EOL.

This distribution is compiled from fresh sources by the SourceMation automation
team, and the pip package manager is included for your convenience. The build
process leverages cryptographic signatures to guarantee the integrity of the
source code.


## Usage

You can run a temporary container with the Python REPL (Read-Eval-Print Loop)
using the following command. Remember to include the `-it` argument for
interactive mode.

```bash
docker run --rm -it sourcemation/python-3.8:latest
```

To access the shell within the container, use:

```bash
docker run --rm -it sourcemation/python-3.8:latest sh
```

## Advanced Usage Examples

Serve the contents of your current directory using Python's built-in HTTP
server, forwarding port 8000:

```bash
docker run --rm -p 8000:8000 -v "${PWD}:/your-project" -w "/your-project" -it sourcemation/python-3.8:latest python3 -m http.server 8000
```

Build an MkDocs project from your current directory and serve it, demonstrating with Podman:

```bash
podman run --rm -p 8000:8000 -v "${PWD}:/your-project" -w "/your-project" -it sourcemation/python-3.8:latest sh -c 'pip3 install -r requirements.txt && mkdocs build && mkdocs serve'
```

## Most Important Environment Variables

This image utilizes the following environment variables:

```
PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
PYTHON_VERSION=3.8.X # example: 3.8.20
```

## Ports
This image does not expose any ports by default. You can expose the ports you
need using the `-p` option with Docker/Podman, by manually configuring ports,
or through orchestration tools like Kubernetes or Docker Compose. You also have
the flexibility to create a custom image with pre-exposed ports.

## Contributing and Reporting Issues
Your contributions are valuable! If you have suggestions for enhancements or
requests for new images, please open an issue. You can also submit your own
contributions via pull requests to the SourceMation GitHub repository.

[Creating issues (bugs) and image requests](https://github.com/SourceMation/images/issues/new/choose)

[Creating pull requests](https://github.com/SourceMation/images/compare)

Disclaimer: The `sourcemation/python-3.8` image is not affiliated with the
Python Software Foundation. The respective companies and organizations own the
trademarks mentioned in this offering. The `sourcemation/python-3.8` image is a
separate project and is maintained by [SourceMation](https://sourcemation.com).

## Extra Notes
A detailed risk analysis report of our images and their components may be found
on the [SourceMation platform](https://www.sourcemation.com/).

Please note that not all images currently have a risk analysis report
available. If you require additional software components or have any questions,
please contact us.

## Licenses
The base license for the solution (Python) is the [Python License](https://docs.python.org/3.8/license.html).
