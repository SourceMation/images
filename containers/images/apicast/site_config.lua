local site_config = { }

local openresty = [[/usr/local/openresty]]
local luajit = openresty .. [[/luajit]]

site_config.LUAROCKS_SYSCONFIG=openresty .. [[/config-5.1.lua]]
site_config.LUA_INTERPRETER=[[resty]]
site_config.LUA_DIR_SET=false
site_config.LUAROCKS_PREFIX= [[/usr]]
site_config.LUA_INCDIR= luajit .. [[/include/luajit-2.1]]
site_config.LUA_LIBDIR= luajit .. [[/lib/5.1]]
site_config.LUA_BINDIR= openresty .. [[/bin]]
site_config.LUAROCKS_SYSCONFDIR=[[/etc/luarocks]]
site_config.LUAROCKS_ROCKS_TREE=[[/usr/local/openresty/luajit]]
site_config.LUAROCKS_ROCKS_SUBDIR=[[/luarocks/rocks]]
site_config.LUAROCKS_UNAME_S=[[Linux]]
site_config.LUAROCKS_UNAME_M=[[x86_64]]
site_config.LUAROCKS_DOWNLOADER=[[curl]]
site_config.LUAROCKS_MD5CHECKER=[[md5sum]]

site_config.LUAROCKS_EXTERNAL_DEPS_SUBDIRS={ bin="bin", lib={ "lib", [[lib64]] }, include="include" }
site_config.LUAROCKS_RUNTIME_EXTERNAL_DEPS_SUBDIRS={ bin="bin", lib={ "lib", [[lib64]] }, include="include" }

return site_config
