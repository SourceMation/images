# Ghost packaged by SourceMation

> Ghost is a powerful app for new-media creators to publish, share, and grow a business around their content. It comes with modern tools to build a website, publish content, send newsletters & offer paid subscriptions to members.

This Ghost distribution is provided by the upstream Ghost packaging team.

## Usage

Running Ghost requires a separate database container (MySQL or MariaDB). The following steps show how to run both containers and connect them using a shared Docker network.

### Step 1: Create a Docker Network

This creates a dedicated network that allows the Matomo and database containers to communicate with each other by name.

```bash
docker network create ghost-net
```

### Step 2: Start the Database Container

Run a MariaDB container on the network. **Ghost requires the `root` user for initial setup**, so we provide its password directly.

```bash
docker run -d --name ghost-db \
  --network ghost-net \
  -v db_data:/var/lib/mysql \
  -e MARIADB_ROOT_PASSWORD=root \
  sourcemation/mariadb
```

### Step 3: Start the Ghost Container

Now, run your Ghost image, connecting it to the same network and pointing it to the database container. You must provide the database credentials and the public URL where your blog will be accessible.

```bash
docker run -d --name ghost-app \
  --network ghost-net \
  -p 8080:2368 \
  -v ghost_content:/var/lib/ghost/content \
  -e url="http://localhost:8080" \
  -e database__client="mysql" \
  -e database__connection__host="ghost-db" \
  -e database__connection__user="root" \
  -e database__connection__password="root" \
  -e database__connection__database="ghost" \
  sourcemation/ghost
```

After a minute, your Ghost blog will be available at **http://localhost:8080**.
To access the admin panel and create your administrator account, navigate to **http://localhost:8080/ghost**.

-----

## Environment Vars, Ports, Volumes

### Variables

Ghost is configured using environment variables that follow the `ghost config` command structure. Use a double underscore (`__`) to represent nested keys.

| Variable | Description |
| :--- | :--- |
| **`url`** | **Required.** The full public URL where your blog will be accessible. |
| **`database__client`** | **Required.** The type of database client. **Note:** Use `mysql` for both MySQL and MariaDB connections. |
| **`database__connection__host`** | **Required.** The hostname of the database server (usually the container name). |
| **`database__connection__user`** | **Required.** The username for the database. **Must be `root` for initial setup.** |
| **`database__connection__password`** | **Required.** The password for the database `root` user. |
| **`database__connection__database`** | **Required.** The name of the database Ghost should create and use. |

### Ports

This image exposes the following ports: 

- 2368 - The default HTTP port for the Ghost application.

Please note that the ports need to be either manually forwarded with the
`-p` option or let Docker choose some for you with the `-P` option.

-----

### Volumes

  * `/var/lib/ghost/content`: This directory contains all your site's content, including themes, images, and internal data. **Using a volume for this path is essential to make your site persistent.**

-----


## Contributing and Issues

We'd love for you to contribute! You can request new features, report bugs, or
submit a pull request with your contribution to this image on the SourceMation
GitHub repository.

- [Creating issues, feature requests, and bug reports](https://github.com/SourceMation/images/issues/new/choose)
- [Creating pull requests](https://github.com/SourceMation/images/compare)

**Disclaimer:** The `sourcemation/ghost` image is not affiliated with
the Ghost Foundation. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/ghost` image is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

## Extra notes

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [SourceMation platform](https://sourcemation.com/).

For more information, check out the [Ghost website](https://ghost.org/).

### Licenses

The base license for the solution (Matomo) is the
[MIT License](https://github.com/TryGhost/Ghost/blob/main/LICENSE).
The licenses for each component shipped as
part of this image can be found on [the image's appropriate SourceMation
entry](https://sourcemation.com/).
