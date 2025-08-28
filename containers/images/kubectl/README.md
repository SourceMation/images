# Kubectl packed by Sourcemation

**kubectl** is the official command-line tool for Kubernetes. It allows you to
run commands against Kubernetes clusters to deploy applications, inspect and
manage cluster resources, and view logs.

This kubectl distribution is an image provided by the
[SourceMation](https://sourcemation.com) packaging team.

## Usage

To run temporary container with the image and print `kubectl` help:

```bash
docker run --rm -it sourcemation/kubectl:latest
```

You can also run kubectl commands directly, for example:

```bash
docker run --rm -it sourcemation/kubectl:latest version --client
```

You can also mount your kubeconfig file to the container to interact with your
Kubernetes cluster. For example:

```bash
docker run --rm -it -v $HOME/.kube:/home/appuser/.kube sourcemation/kubectl:latest get pods
```

Or more interactively by changin the entrypoint to bash:

```bash
docker run --rm -it --entrypoint bash -v $HOME/.kube:/home/appuser/.kube sourcemation/kubectl:latest
```

This will open a shell inside the container, where you can then run your
kubectl commands as needed, for example:

```bash
kubectl get nodes
```

All above commands can be run with `podman` as well :).


## Aliasing the image to `kubectl` command

You can create an alias in your shell to simplify the usage of the `sourcemation/kubectl`
image. Add the following line to your shell configuration file (e.g., `.bashrc`, `.zshrc`):

```bash
alias kubectl='docker run --rm -it -v $HOME/.kube:/home/appuser/.kube sourcemation/kubectl:latest'
```

and then reload your shell configuration (just start a new shell or source the
file). Use it carefully and only if you are comfortable with:

- Not having the shell hinting for `kubectl` commands
- Not having any local `kubectl` installation that will be shadowed by the alias

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
KUBECTL_VERSION=v1.34.0
```

There is single volume `/home/appuser/.kube` to potentially persist kubectl
config.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the SourceMation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/kubectl` image is not affiliated with the
Cloud Native Computing Foundation (CNCF).. The respective companies and organisations
own the trademarks mentioned in the offering. The `sourcemation/kubectl` image
is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

## Extra notes

The application runs as the `appuser`.
You force usage of the root user with the docker `--user root` flag.


### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on
the SourceMation platform.

For more information, check out the [Official Kubectl Documentation](https://kubernetes.io/docs/reference/kubectl/).

### Licenses

The base license for the kubectl is the [Apache License
Version 2.0](https://github.com/kubernetes/kubectl/blob/master/LICENSE).
