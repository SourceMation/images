# phpMyAdmin packaged by SourceMation

> phpMyAdmin is a free and open-source administration tool for MySQL and MariaDB. As a portable web application written primarily in PHP, it has become one of the most popular database management tools.

This phpMyAdmin distribution is provided by the upstream phpMyAdmin packaging team.

## Usage

phpMyAdmin is a database client and needs to connect to a database server. The following examples show how to run it.

### Scenario 1: Connect to an Existing Database

If you have a database running on your host machine or elsewhere on your network, you can point this container to it using the `PMA_HOST` environment variable.

```bash
docker run -d --name myadmin \
  -p 8080:80 \
  -e PMA_HOST="<ip_address_of_your_db>" \
  sourcemation/phpmyadmin
````

You can now access phpMyAdmin at **http://localhost:8080**.

### Scenario 2: Running with Docker Network (Recommended)

The best way to use this image is to run it on the same Docker network as your database container.

**Step 1: Create a Docker Network**

```bash
docker network create my-app-net
```

**Step 2: Start your Database Container**
Make sure your MariaDB or MySQL container is connected to this network.

```bash
docker run -d --name my-db \
  --network my-app-net \
  -e MARIADB_ROOT_PASSWORD=root \
  -e MARIADB_DATABASE=mariadb \
  -e MARIADB_USER=mariadb \
  -e MARIADB_PASSWORD=mariadb \
  sourcemation/mariadb
```

**Step 3: Start the phpMyAdmin Container**

Run the phpMyAdmin container, pointing it to the database container using its name (`my-db`) as the host.

```bash
docker run -d --name myadmin \
  --network my-app-net \
  -p 8080:80 \
  -e PMA_HOST=my-db \
  sourcemation/phpmyadmin
```

Now, navigate to **http://localhost:8080**, and you can log in to your `my-db` server.

**Arbitrary Server Login:** If you omit the `PMA_HOST` variable, the login page will show a field where you can manually enter any database server address.

-----

## Image tags and versions

The `sourcemation/phpmyadmin` image itself comes in `debian-13` flavor.
The tag `latest` refers to the Debian-based flavor.

## Environment Vars, Ports, Volumes

| Variable | Description | Default |
| :--- | :--- | :--- |
| **`PMA_HOST`** | The hostname or IP address of the MySQL/MariaDB server to connect to. | (not set) |
| **`PMA_PORT`** | Optional. The port of the database server. | (not set) |

If `PMA_HOST` is not set, `AllowArbitraryServer` will be enabled, allowing you to specify the host on the login page.

-----

This image exposes the following ports: 

- 80 - Default Apache port

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

-----

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the SourceMation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/phpmyadmin` image is not affiliated with
the phpMyAdmin project. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/phpmyadmin` image is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [SourceMation platform](https://sourcemation.com/).

For more information, check out the [phpMyAdmin website](https://www.phpmyadmin.net/).

### Licenses

The base license for the solution (phpMyAdmin) is the
[GNU General Public License v2.0](https://www.phpmyadmin.net/license/)).
The licenses for each component shipped as
part of this image can be found on [the image's appropriate SourceMation
entry](https://sourcemation.com/).
