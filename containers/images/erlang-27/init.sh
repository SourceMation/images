#!/usr/bin/env bash
# -----------------------------------
# Author: Marek Janosz
# e-mail: marek.janosz@linuxpolska.pl
# Date: 2025-09-24
# -----------------------------------

set -eu

echo "-> Preparing openssl variables"
OPENSSL_VER_SRC="https://api.github.com/repos/openssl/openssl/releases/latest"
OPENSSL_VERSION=$(curl -s ${OPENSSL_VER_SRC} |grep -o '"tag_name": "[^"]*' |cut -d'"' -f4 |sed 's/openssl-//')
OPENSSL_DOWNLOAD_SHA256="https://github.com/openssl/openssl/releases/download/openssl-${OPENSSL_VERSION}/openssl-${OPENSSL_VERSION}.tar.gz.sha256"
OPENSSL_SHA256=$(curl -fsL ${OPENSSL_DOWNLOAD_SHA256}|awk '{print $1}')

sed -i "s#^ARG OPENSSL_VERSION=.*#ARG OPENSSL_VERSION=${OPENSSL_VERSION}#" Dockerfile || exit 1
sed -i "s#^ARG OPENSSL_SHA256=.*#ARG OPENSSL_SHA256=${OPENSSL_SHA256}#" Dockerfile || exit 1

echo "-> Preparing erlang variables"
ERLANG_VER_SRC="https://api.github.com/repos/erlang/otp/releases"
ERLANG_VERSION=$(curl -s ${ERLANG_VER_SRC} | grep -o '"tag_name": "OTP-27[^"]*"' | cut -d'"' -f4 | sed 's/OTP-//' | sort -V | tail -1)
ERLANG_DOWNLOAD_SHA256=https://github.com/erlang/otp/releases/download/OTP-${ERLANG_VERSION}/SHA256.txt
ERLANG_SHA256=$(curl -fsL ${ERLANG_DOWNLOAD_SHA256} | grep 'otp_src' | awk '{print $1}')

sed -i "s#^ARG ERLANG_VERSION=.*#ARG ERLANG_VERSION=${ERLANG_VERSION}#" Dockerfile || exit 1
sed -i "s#^ARG ERLANG_SHA256=.*#ARG ERLANG_SHA256=${ERLANG_SHA256}#" Dockerfile || exit 1
sed -i "s/version=\"[^\"]*\"/version=\"$ERLANG_VERSION\"/" Dockerfile || exit 1
sed -i "s/APP_VERSION=\"[^\"]*\"/APP_VERSION=\"$ERLANG_VERSION\"/" Dockerfile || exit 1
sed -i "s/APP_VERSION=\"[^\"]*\"/APP_VERSION=\"$ERLANG_VERSION\"/" README.md || exit 1
