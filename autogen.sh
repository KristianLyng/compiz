#!/bin/sh

set -xe
autoreconf --install
glib-gettextize --copy --force
intltoolize --copy --force --automake
