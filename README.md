# Sourcemation main image repository


This repository contains the images delivered/tested and scored by the
Sourcemation platform. The aim is to provide a central location for the images
you can test, use and deploy in your projects and solutions.

## Issues and PRs

Your contributions are welcome. If you have an idea for a new image or
encounter a problem with the existing images, please open an issue or a pull
request. Our team is monitoring the repository and will respond to your
requests.


We have provided a template for the issues and pull requests for your
convenience. Please use it, but do not feel limited by it. If you have a
different need, you can always create a blank issue or PR—it’s up to you
:octocat:.

## Repository structure

Each type of image is stored in a separate directory. The directory name
corresponds to the image type. Most of them should contain a README.md file or
similar documentation that describes the image and how to use it.


- `containers` - Container images that are base blocks for your applications. Available on Docker Hub and Quay.io.
- `vmi` - Virtual Machine Images that can be used in your virtualization
  environment. They are available on the GitHub releases page on separate
  repositories and tags.
- `wsl` - Windows Subsystem for Linux images that can be used in your Windows
  environment. They are deployed on the GitHub releases page on separate
  repositories and tags.
- `vagrant` - Vagrant images can be used in your Vagrant environment. They are
  deployed on HashiCorp Cloud Platform.

## Technologies

- We are using docker and podman to build and test the container images.
- We are using Packer to build the Virtual Machine Images. **Because of the
  license changes, we are using old frozen versions of Packer. Your PR must run
  against Packer 1.9.2, the last version supporting the old license.**
- GitHub Actions are used to build and test the container images.
- Jenkins is used to build VMI and Vagrant images. Our Jenkins is not public,
  and we do not plan to make it public. You can use the provided scripts to
  recreate the images without Jenkins, or you can use the Jenkinsfile to
  replicate the Jenkins pipeline in your own Jenkins instance.

## Problematic images
### Based on Rocky9
- activemq
- apicast
- camel-karavan
- helidon
- java
- jenkins
- kafka
- karaf
- kong
- micronaut
- mongodb
- mosquitto
- nodejs
- openapi-generator-cli
- postgresql
- python
- quarkus
- rabbitmq
- rocky-9
- rocky-9-minimal
- ruby
- servicemix

### Other problems
- angular - need to create init.sh
- azure-cli - not available right now (packages.microsoft.com/repos/azure-cli/dists/)
- camel-k - on debian13 there is no openjdk-17-headless but openjdk-21 & 25
- cassandra - on debian13 there is no openjdk-17-headless but openjdk-21 & 25
- hugo - Checksum NODEJS problem
- manageiq - base image is not ours
- mysql - GPG key problem (no new key)
