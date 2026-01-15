# pgBadger packaged by Sourcemation

> pgBadger is a PostgreSQL log analyzer built for speed with fully detailed reports and graphs.

This pgBadger distribution is provided by the upstream GitHub repository.

## Usage

Run a temporary container with pgBadger to analyze a log file:

```bash
docker run --rm -v /path/to/your/postgresql.log:/log.txt sourcemation/pgbadger /log.txt -o /report.html
```

Or pipe the log content:

```bash
cat postgresql.log | docker run --rm -i sourcemation/pgbadger - -o - > report.html
```

## Image tags and versions

The `sourcemation/pgbadger` image comes in `debian-13` flavor. The tag `latest` refers to the Debian-based flavor.

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or submit a pull request with your contribution to this image on the Sourcemation GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/pgbadger` image is not affiliated with the pgBadger project. The `sourcemation/pgbadger` image is a separate project and is maintained by [Sourcemation](https://sourcemation.com).

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be found on the [Sourcemation platform](https://sourcemation.com/catalog/pgbadger).

For more information, check out the [pgBadger website](https://pgbadger.darold.net/).

### Licenses

The base license for the solution (pgBadger) is the [PostgreSQL License](https://github.com/darold/pgbadger/blob/master/LICENSE). The licenses for each component shipped as part of this image can be found on [the image's appropriate Sourcemation entry](https://sourcemation.com/catalog/pgbadger).