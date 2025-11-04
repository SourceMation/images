# Matomo packaged by Sourcemation

> Matomo is a free and open-source web analytics application. It provides detailed reports on your website and its visitors, including the search engines and keywords they used, the language they speak, which pages they like, the files they download and so much more.

This Matomo distribution is provided by the upstream Matomo packaging team.

## Usage

Running Matomo requires a separate database container (e.g., MariaDB or MySQL). The following steps show how to run both containers and connect them using a shared Docker network.

### Step 1: Create a Docker Network

This creates a dedicated network that allows the Matomo and database containers to communicate with each other by name.

```bash
docker network create matomo-net
```

### Step 2: Start the Database Container

Run a MariaDB container on the network, creating the database and user that Matomo will need.

```bash
docker run -d --name matomo-db \
  --network matomo-net \
  -v db_data:/var/lib/mysql \
  -e MARIADB_ROOT_PASSWORD=root \
  -e MARIADB_DATABASE=matomo \
  -e MARIADB_USER=matomo \
  -e MARIADB_PASSWORD=matomo \
  sourcemation/mariadb
```

### Step 3: Start the Matomo Container

Now, run your Matomo image, connecting it to the same network and pointing it to the database container. You must also provide initial credentials for the Matomo superuser.

```bash
docker run -d --name matomo-app \
  --network matomo-net \
  -p 8080:80 \
  -v matomo_files:/var/www/html \
  sourcemation/matomo
```

After a minute, your Matomo instance will be fully installed and available at **http://localhost:8080**. You can log in with the admin credentials you provided.

-----

## Image tags and versions

The `sourcemation/matomo` image itself comes in `debian-13` flavor.
The tag `latest` refers to the Debian-based flavor.

## Environment Vars, Ports, Volumes

### Ports

This image exposes the following ports: 

- 80 - Default Apache port

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

-----

### Volumes

  * `/var/www/html`: The main Matomo installation directory. It stores core files, plugins, and the configuration. **It is essential to use a volume for this path to make your site persistent.**

-----


## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the Sourcemation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/matomo` image is not affiliated with
the Matomo project. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/matomo` image is a separate project and is maintained by
[Sourcemation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [Sourcemation platform](https://sourcemation.com/).

For more information, check out the [Matomo website](https://www.matomo.org/).

### Licenses

The base license for the solution (Matomo) is the
[GPLv3 license](https://matomo.org/licences/).
The licenses for each component shipped as
part of this image can be found on [the image's appropriate Sourcemation
entry](https://sourcemation.com/).
