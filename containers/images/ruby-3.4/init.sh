#!/usr/bin/env bash
# ---------------------------------------------------
# Automated build process for the ruby 3.4 image
# Author: Alex Baranowski
# e-mail: aleksander.baranowski@yahoo.pl
# ---------------------------------------------------

APP="ruby-3.4"

# Updating repository metadata and downloading the latest available version of the application
echo "Checking the latest available version of the $APP"
VERSION=$(git ls-remote --refs --tags https://github.com/ruby/ruby.git | grep -o 'v3_4_[0-9]*$' | tr -d 'v' | tr '_' '.' | sort --version-sort --reverse | head -1)

# Exit with an error if the returned version contains anything other than digits and dots
[[ ! $VERSION =~ ^[0-9.]+$ ]] && exit 1

# Now get the SHA256 sum
echo "Fetching and computing SHA256 for ruby-$VERSION"
SHA256_SUM=$(curl -s "https://cache.ruby-lang.org/pub/ruby/3.4/ruby-${VERSION}.tar.xz" | sha256sum | awk '{print $1}')

# Replacing the version number and SHA256 in the Dockerfile
sed -i "s/version=\"[^\"]*\"/version=\"$VERSION\"/" Dockerfile || exit 1
sed -i "s/ENV RUBY_VERSION [0-9.]*/ENV RUBY_VERSION $VERSION/" Dockerfile || exit 1
sed -i "s|ENV RUBY_DOWNLOAD_URL .*|ENV RUBY_DOWNLOAD_URL https://cache.ruby-lang.org/pub/ruby/3.4/ruby-${VERSION}.tar.xz|" Dockerfile || exit 1
sed -i "s/ENV RUBY_DOWNLOAD_SHA256 [a-f0-9]*/ENV RUBY_DOWNLOAD_SHA256 $SHA256_SUM/" Dockerfile || exit 1

# Replacing the version number in README.md
sed -i "s/APP_VERSION=\"[^\"]*\"/APP_VERSION=\"$VERSION\"/" README.md || exit 1

echo "Finished setting up the $APP $VERSION image"
