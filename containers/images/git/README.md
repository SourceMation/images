# Git packaged by SourceMation

> Git is a free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency.

This Git distribution is provided by the downstream Debian 12 packaging team in the version respective to that system.

## Usage

Run a temporary container with Git:

```bash
docker run --rm -it sourcemation/git
```

Run a temporary container with Git as root:

```bash
docker run -u 0 --rm -it sourcemation/git
```

### Advanced usage examples

**Clone a repository to local directory:**
```bash
docker run -u 0 --rm -v $(pwd):/workspace -w /workspace sourcemation/git git clone https://github.com/SourceMation/images.git
```

## Image tags and versions

The `sourcemation/git` image comes in the `debian-12` flavor. The tag `latest` refers to the latest Debian-based image.

Available tags:
- `latest` - Latest Debian 12 based image
- `latest-arm64` - Latest Debian 12 based image for ARM architecture
- `latest-amd64` - Latest Debian 12 based image for x86-64 architecture
- `2.39.5` - Specific Git version on Debian 12

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
LANG=C.UTF-8
DEBIAN_FRONTEND=noninteractive 
HOME=/home/git
```

**Volumes:**
- `/workspace` - Recommended mount point for your project files
- `/home/git` - Git user's home directory for configuration

**User:**
- The container runs as user `git` (non-root) for security
- UID/GID can be mapped using Docker's `--user` or `-u` flag if needed

This image does not expose any ports as Git is primarily a command-line tool.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or submit a pull request with your contribution to this image on the SourceMation GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/git` image is not affiliated with the Git project or the Git development team. Git and its logo are trademarks of the Git project. The `sourcemation/git` image is a separate project and is maintained by [SourceMation](https://sourcemation.com).

## Extra notes

### Security Features

- Runs as non-root user (`git`) for improved security
- Minimal attack surface with only essential packages installed
- Regular security updates from Debian repositories
- CA certificates included for secure HTTPS operations

### What's Included

- Minimal Debian 12 base system
- Git (latest available in Debian 12 repositories)
- Curl for HTTPS operations
- OpenSSL for cryptographic operations
- CA certificates for secure connections

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on the [SourceMation platform](https://sourcemation.com/catalog/git).
For more information, check out the [overview of Git](https://git-scm.com) page.

### Licenses

The base license for the solution (Git) is the [GNU General Public License v2.0](https://github.com/git/git/blob/master/COPYING). The licenses for each component shipped as part of this image can be found on [the image's appropriate SourceMation entry](https://sourcemation.com/catalog/git).

### Additional Resources

- [Official Git Documentation](https://git-scm.com/doc)
- [Pro Git Book](https://git-scm.com/book)
- [Git Reference Manual](https://git-scm.com/docs)
- [Debian Git Package Information](https://packages.debian.org/bookworm/git)