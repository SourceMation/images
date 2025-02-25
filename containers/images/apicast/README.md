# APIcast packaged by SourceMation

APIcast is a utility for managing API integrations with the [Red Hat 3scale
Platform](https://www.redhat.com/en/technologies/jboss-middleware/3scale) with
extensive customization and administration options and deployment flexibility.

This APIcast distribution is a proprietary compilation provided by the
[SourceMation](https://sourcemation.com) packaging team.

## Usage

Run a temporary container with APIcast's default development gateway:

```
docker run --rm --ulimit nofile=64000:64000 --ulimit nproc=64000:64000 -it sourcemation/apicast:latest apicast start --dev
```

For a hosted deployment managed by 3scale or OpenShift deployments, refer to
[the "Getting started" section in the upstream
README](https://github.com/3scale/APIcast/tree/c54aa0ba61fe1f41ae0653ea79745a87d27b8dd6?tab=readme-ov-file#getting-started).

## Environment Vars, Ports, Volumes

This image uses the following environment variables:

```
PATH="/home/appuser/APIcast/lua_modules/bin:/usr/local/openresty/luajit/bin/:/home/appuser/APIcast/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
"LUA_PATH=/home/appuser/APIcast/lua_modules/share/lua/5.1/?.lua;/home/appuser/APIcast/lua_modules/bin/lua_modules/share/lua/5.1/?/init.lua;/usr/lib64/lua/5.1/?.lua;/usr/share/lua/5.1/?.lua"
LUA_CPATH="/home/appuser/APIcast/lua_modules/lib/lua/5.1/?.so;;"
LD_LIBRARY_PATH=":/home/appuser/APIcast/local/lib:/home/appuser/APIcast/lua_modules/lib"
```

## Contributing and Issues

We’d love for you to contribute! You can request new features by
creating an issue or submitting a pull request with your contribution to
this image on the SourceMation GitHub repository.

[Creating issues](https://github.com/SourceMation/containers/issues/new)
[Creating pull
requests](https://github.com/SourceMation/containers/compare)

**Disclaimer:** The `sourcemation/apicast` image is not affiliated with,
endorsed by, or supported by Red Hat, Inc. The respective companies and
organisations own the trademarks mentioned in the offering. The
`sourcemation/apicast` image is a separate project and is maintained by
[SourceMation](https://sourcemation.com).

## Extra notes

The publicly available APIcast uses Enterprise Linux 8 and an outdated Lua
version (5.1) with no longer supported libraries. This image attempts to run
APIcast on Rocky Linux 9 (or any other Enterprise Linux 9), what requires many
hacks and workarounds to make it work. There is no guarantee that this image
will work for you, but it’s a good starting point.

This image uses the revision of APIcast from the [upstream commit
`c54aa0ba61fe1f41ae0653ea79745a87d27b8dd6`](https://github.com/3scale/APIcast/tree/c54aa0ba61fe1f41ae0653ea79745a87d27b8dd6)
and was made possible thanks to the hard work of:

- [James McKaskill for luaffi](https://github.com/jmckaskill/luaffi.git)
- the [upstream OpenResty packaging team for the release version
  1.21.4.3](https://openresty.org/en/linux-packages.html)

The application runs as the user `appuser`, UID and GID no. 1000.

- Old unsupported ffi library for lua:
  https://github.com/jmckaskill/luaffi.git
- The reason why we are using a newer commit instead of the older 3.15.0:
  https://github.com/3scale/APIcast/pull/1483

### Image and its components Risk Analysis report

A detailed risk analysis report of the image and its components can be
found on the [SourceMation
platform](https://sourcemation.com).

For more information, check out the [overview of
APIcast](https://docs.redhat.com/en/documentation/red_hat_3scale_api_management/2.3/html/deployment_options/apicast-overview)
page.

### Licenses

The base license for the solution (APIcast revision
`c54aa0ba61fe1f41ae0653ea79745a87d27b8dd6`) is the [Apache License, Version
2.0](https://github.com/3scale/APIcast/blob/c54aa0ba61fe1f41ae0653ea79745a87d27b8dd6/LICENSE).
The licenses for each component shipped as part of this image can be found on
the image's appropriate SourceMation entry.
