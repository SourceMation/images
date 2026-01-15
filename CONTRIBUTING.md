# Contributing to Sourcemation Images

Thank you for your interest in contributing to the Sourcemation Images repository! This document provides guidelines for contributing and instructions on how to set up your local development environment.

## Getting Started

To start contributing, you should have the following tools installed:
- `docker` or `podman`
- `bash`
- `git`

### Building Images Locally

If you want to fix a bug in an existing image or add a new one, you should verify your changes locally using the provided build scripts.

1. Navigate to the `containers` directory:
   ```bash
   cd containers
   ```
2. Run the build script for a specific image. Set `TEST_IMAGE=true` to run tests after the build and `PUSH_IMAGE=false` to prevent pushing to registries:
   ```bash
   export TEST_IMAGE=true PUSH_IMAGE=false PUSH_README=false
   ./build-container.sh <image-name>
   ```
   Example for `kubectl`:
   ```bash
   export TEST_IMAGE=true PUSH_IMAGE=false PUSH_README=false
   ./build-container.sh kubectl
   ```

### Working with Problematic Images

If you are looking to help with images listed as "Problematic" in the main `README.md`, follow these steps:
1. Identify the image name (e.g., `activemq`).
2. Try to build it locally using the command above.
3. Observe the build or test errors.
4. Modify the `Dockerfile`, `init.sh`, or `conf.sh` in the image directory (`containers/images/<image-name>`) to fix the issue.
5. Re-run the build script until it passes.

## Adding a New Container

1. Create a new directory under `containers/images/` using the name of your image. You can use `containers/images/_template/` as a base.
2. Ensure your `Dockerfile` includes `version` and `name` labels.
3. (Optional) Add `init.sh` if you need to download assets or modify the `Dockerfile` before building.
4. (Optional) Add `conf.sh` if you need custom build configurations (e.g., multi-tagging, custom entrypoints).
5. Add a test file in `containers/tests/test_<image-name>.py`.
6. Add the image name to the list in `.github/workflows/build-manual.yml`.
7. Test it locally as described above.

## Multiple Systems and Tags

If your image supports multiple base OS or requires specific tags, use the `conf.sh` file:
```bash
DOCKER_TAG_SUFFIX="debian-11"
```

## Pull Request Process

1. Fork the repository and create your branch from `main`.
2. Ensure your changes pass local builds and tests.
3. Submit a Pull Request with a clear description of your changes.
4. Our team will review your PR and provide feedback.

## Coding Standards

- Follow existing naming conventions for directories and tags.
- Keep `Dockerfile`s clean and well-commented where necessary.
- Respect the license of the base images and software you are packaging.
