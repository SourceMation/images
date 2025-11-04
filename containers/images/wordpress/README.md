# WordPress packaged by Sourcemation

> WordPress is the world's most popular content management system (CMS), built on PHP and MySQL/MariaDB.

This WordPress distribution is provided by the upstream WordPress packaging team.

## Usage

Running WordPress requires a separate database container. The following steps show how to run both the WordPress and database containers and connect them using a shared Docker network.

### Step 1: Create a Docker Network

This command creates a dedicated network that allows the WordPress and database containers to communicate with each other by name.
```bash
docker network create wordpress-net
```

### Step 2: Start the Database Container

```bash
docker run -d --name wordpress-db \
  --network wordpress-net \
  -v db_data:/var/lib/mysql \
  -e MARIADB_ROOT_PASSWORD=root \
  -e MARIADB_DATABASE=wordpress \
  -e MARIADB_USER=wordpress \
  -e MARIADB_PASSWORD=wordpress \
  sourcemation/mariadb
```

### Step 3: Start the WordPress Container

Now, run your WordPress image, connecting it to the same network and pointing it to the database container using its name (`wordpress-db`) as the host.

```bash
docker run -d --name wordpress-app \
  --network wordpress-net \
  -p 8080:80 \
  -v wp_files:/var/www/html \
  -e WORDPRESS_DB_HOST=wordpress-db \
  -e WORDPRESS_DB_USER=wordpress \
  -e WORDPRESS_DB_PASSWORD=wordpress \
  -e WORDPRESS_DB_NAME=wordpress \
  sourcemation/wordpress
```

### Step 4: Complete the Installation in the Browser

After a minute, your WordPress site will be available at **http://localhost:8080**. You can now open this address in your web browser to complete the installation (setting your site title, admin user, etc.).


## Image tags and versions

The `sourcemation/wordpress` image itself comes in `debian-13` flavor.
The tag `latest` refers to the Debian-based flavor.

## Environment Vars, Ports, Volumes

The container is configured at startup using the following environment variables:

| Variable | Description | Example |
| :--- | :--- | :--- |
| **`WORDPRESS_DB_HOST`** | **Required.** The hostname or IP of the database server. In this case, it's the name of the database container. | `wordpress-db` |
| **`WORDPRESS_DB_USER`** | **Required.** The database username that WordPress should use. | `wordpress` |
| **`WORDPRESS_DB_PASSWORD`** | **Required.** The password for the database user. | `wordpress` |
| **`WORDPRESS_DB_NAME`** | **Required.** The name of the database that WordPress should use. | `wordpress` |
| **`WORDPRESS_TABLE_PREFIX`** | Optional. A custom prefix for the WordPress tables in the database. | `wp_` |

-----

This image exposes the following ports: 

- 80 - Default Apache port

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

-----

### Volumes

| Path in Container | Description |
| :--- | :--- |
| **`/var/www/html`** | **Critical.** The main WordPress installation directory. It stores core files, themes, plugins, and all user-uploaded media. Using a volume for this path is **essential** to make your site persistent. |
| **`/var/lib/mysql`** | (For the database container) Stores all of your database data. Also critical for data persistence. |

-----

## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the Sourcemation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/Sourcemation/images/issues/new/choose)
- [Creating pull requests](https://github.com/Sourcemation/images/compare)

**Disclaimer:** The `sourcemation/wordpress` image is not affiliated with
the WordPress project. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/wordpress` image is a separate project and is maintained by
[Sourcemation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [Sourcemation platform](https://sourcemation.com/).

For more information, check out the [WordPress website](https://wordpress.org/).

### Licenses

The base license for the solution (Wordpress) is the
[GPLv2 (or later)](https://wordpress.org/about/license/).
The licenses for each component shipped as
part of this image can be found on [the image's appropriate Sourcemation
entry](https://sourcemation.com/).
