# SourceMation containers build process

These containers are built with a GitHub Action workflow/action named Build
Container. The repository contains all the necessary files and secrets to build
the container.

## Build process

- Before building, the `init.sh`, if it exists, is run. The `init.sh` can change
  the Dockerfile or any other file in the repository. It’s mainly used to set
  the version label in the Dockerfile and download necessary files like jar,
  rpm, etc.
- Then, the Dockerfile is read as config, and the image version and name are
  set. Note that it means that **each Dockerfile must have the version and the
  name label.**
- Then, the `./conf.sh`, if it exists, is executed; it could alter the build
  anyway. The most important function of `conf.sh` is to set the
  `DOCKER_TAG_SUFFIX`, which allows the creation of a multi-tag repository. This
  file might not exist in all containers. It can also override anything set in
  the `init.sh` script.
- Then, the container is built. We support aarch64 (arm64) and amd64 (x86_64) architectures.
- The container is pushed to the Docker Hub and Quay.io.

## Creating multiple systems and tags images

To build the container image that supports multiple base os and tags you have
to do the following:

- Add the `conf.sh`, file to the root of the image directory.

The config file `conf.sh` should contain the following:

```bash
DOCKER_TAG_SUFFIX="debian-11"
```

In example above the `DOCKER_TAG_SUFFIX` is set to `debian-11`, so the image
will be tagged as for example
`sourcemation/my-super-image:version-date-arm64-debian11` and
`sourcemation/my-super-image:version-date-amd64-debian11` and also with
versions like `sourcemation/my-super-image:version-debian-11` that should point
to the same image as latest images (it's manifest list. The manifest list will
be overwritten with next build!).

The `DOCKER_TAG_SUFFIX`, as its name suggests, is a suffix to the tag and common
values for it are/will be `debian-11`, `ubuntu-22.04`, `ubuntu-24.04`,
`rocky-9`, etc.

## Skipping tests

Some images - mostly the Kubernetes operators - are not tested in this build
process as they need the Kubernetes cluster up and running.


To disable the tests for the container, add the following to the `conf.sh` file

```bash
TEST_IMAGE="false"
```

Example:

```bash
cat images/redis-operator/conf.sh
TEST_IMAGE="false"
```

## Extra notes

When adding the new container, the following steps should be taken:

- Add the container to the `containers` list in the GitHub workflow file.
- Build the container locally to ensure that it works.
- Add the tests for the container to the `tests` directory.

