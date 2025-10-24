# External-DNS packaged by SourceMation

> External-DNS synchronizes exposed Kubernetes Services and Ingresses with DNS providers. It automatically configures DNS records based on Kubernetes resources, making your services discoverable via DNS.

This external-DNS is compiled from the source provided by the Kubernetes Special Interest Group (SIG) team.

## Usage

Run a temporary container with external-dns to see available options:

```bash
docker run --rm -it sourcemation/external-dns --help
```

### Advanced usage examples

#### AWS Route53 Provider

```bash
docker run --rm \
  -e AWS_ACCESS_KEY_ID=your_access_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret_key \
  -e AWS_REGION=us-west-2 \
  sourcemation/external-dns \
  --provider=aws \
  --aws-zone-type=public \
  --source=service \
  --source=ingress \
  --txt-owner-id=my-cluster \
  --log-level=info \
  --dry-run
```

#### Google Cloud DNS Provider

```bash
docker run --rm \
  -v /path/to/service-account.json:/etc/credentials/service-account.json \
  -e GOOGLE_APPLICATION_CREDENTIALS=/etc/credentials/service-account.json \
  sourcemation/external-dns \
  --provider=google \
  --google-project=your-project-id \
  --source=service \
  --source=ingress \
  --txt-owner-id=my-cluster \
  --log-level=info \
  --dry-run
```

#### Azure DNS Provider

```bash
docker run --rm \
  -e AZURE_CLIENT_ID=your_client_id \
  -e AZURE_CLIENT_SECRET=your_client_secret \
  -e AZURE_TENANT_ID=your_tenant_id \
  -e AZURE_SUBSCRIPTION_ID=your_subscription_id \
  sourcemation/external-dns \
  --provider=azure \
  --azure-resource-group=your-resource-group \
  --source=service \
  --source=ingress \
  --txt-owner-id=my-cluster \
  --log-level=info \
  --dry-run
```

#### Running with Configuration File

```bash
# Create configuration file
cat > external-dns-config.yaml << EOF
interval: 1m
log-level: info
provider: aws
aws-zone-type: public
txt-owner-id: my-cluster
sources:
  - service
  - ingress
EOF

# Run with config file
docker run --rm \
  -v $(pwd)/external-dns-config.yaml:/etc/external-dns/config.yaml \
  -e AWS_ACCESS_KEY_ID=your_access_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret_key \
  -e AWS_REGION=us-west-2 \
  sourcemation/external-dns \
  --config=/etc/external-dns/config.yaml
```

## Image tags and versions

The `sourcemation/external-dns` image itself comes in two flavors: `debian-12`. The tag `latest` refers to the Debian-based flavor.

## Environment Vars, Ports, Volumes

This image uses the following environment variables depending on the DNS provider:

### AWS Route53
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
AWS_PROFILE (optional)
```

### Google Cloud DNS
```
GOOGLE_APPLICATION_CREDENTIALS
GOOGLE_PROJECT (optional, can be specified via --google-project flag)
```

### Azure DNS
```
AZURE_CLIENT_ID
AZURE_CLIENT_SECRET
AZURE_TENANT_ID
AZURE_SUBSCRIPTION_ID
AZURE_RESOURCE_GROUP (optional, can be specified via flag)
```

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the SourceMation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/external-dns` image is not affiliated with
the Kubernetes SIG Network. The respective organizations own the
trademarks mentioned in the offering. The
`sourcemation/external-dns` image is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [SourceMation
platform](https://sourcemation.com/catalog/external-dns).

For more information, check out the [overview of
external-dns](https://kubernetes-sigs.github.io/external-dns/) page.

### Licenses

The base license for the solution (external-dns) is the
[Apache License 2.0](https://github.com/kubernetes-sigs/external-dns/blob/master/LICENSE). The licenses for each component shipped as
part of this image can be found on [the image's appropriate SourceMation
entry](https://sourcemation.com/catalog/external-dns).