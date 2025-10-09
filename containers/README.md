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
  the `init.sh` script. Also the `CONTAINER_STARTUP_TIMEOUT` can be set here.
- In `./conf.sh`, the `ENTRYPOINT_CMD` and `CONTAINER_RUN_COMMAND` variables
  can be overridden from the build script defaults. This is useful for testing
  containers that set the entrypoint to a command which does not support
  running `/bin/bash`.
- Then, the container is built. We support aarch64 (arm64) and amd64 (x86_64) architectures.
- The container is pushed to the Docker Hub and Quay.io.

## Adding the new container


- Add the container to the `containers` list in the GitHub workflow file.
- Build the container locally to ensure that it works.
  ```bash
  export TEST_IMAGE=true PUSH_IMAGE=false PUSH_README=false
  ./build.sh super-image-name
  ```
  Example:
  ```bash
  export TEST_IMAGE=true PUSH_IMAGE=false PUSH_README=false
  ./build-container.sh kubectl
  ```
- Add the tests for the container to the `tests` directory and rerun the build (it tests the
  container locally).

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

## Overwritting entrypoint and run command

To overwrite the default entrypoint and run command, you can set the
`ENTRYPOINT_CMD` and `CONTAINER_RUN_COMMAND` variables in the `conf.sh`

```
ENTRYPOINT_CMD="/my/custom/entrypoint"
CONTAINER_RUN_COMMAND="my custom command"
```

Example:

```bash
# We need to set the /bin/bash as entrypoint
ENTRYPOINT_CMD="/bin/bash"
# Do not use /bin/bash as `bash bash` itself fails as /usr/bin/bash is binary
CONTAINER_RUN_COMMAND=""
```

## Problem with environment variables

In rare ocassions (example - `debian-13-slim` base image), the container won't
build because of some environment variable like ones responsible for dates,
example:

```
LC_TIME=pl_PL.UTF-8
```

The easiest way to fix it to run your local build process in the new shell without
these extra environment variables:

```bash
env -i bash
```
of
```bash
env -i fish
```

