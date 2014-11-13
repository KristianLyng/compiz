#!/bin/sh

autoreconf -v --install || exit 1
glib-gettextize --copy --force || exit 1
intltoolize --copy --force --automake || exit 1
