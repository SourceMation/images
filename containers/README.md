# SourceMation containers build process

These containers are built with a GitHub Action workflow/action named Build
Container. The repository contains all the necessary files and secrets to build
the container.

## Build process

- Before building, the `init.sh`, if it exists, is run. The `init.sh` can change
  the Dockerfile or any other file in the repository. It’s used mostly to set
  the version label in the Dockerfile and download necessary files like jar,
  rpm, etc.
- Then, the Dockerfile is read as config, and the image version and name are
  set. Note that it means that **each Dockerfile must have the version and the
  name label.**
- Then the `./conf.sh`, if it exists, is executed; it could alter the build anyway. The most important
  function of `conf.sh` is to set the DOCKER_SUFFIX that allows to create multi-tag repository. This file
  might not exist in all containers.
- Then, the container is built, and we support aarch64 (arm64) and amd64
  (x86_64) architectures.
- The container is pushed to the Docker Hub and Quay.io.

## Extra notes

When adding the new container, the following steps should be taken:

- Add the container to the `containers` list the github workflow file.
- Build the container locally to ensure that it works.
- Add the tests for the container to the `tests` directory.