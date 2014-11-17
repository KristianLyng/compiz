#! /bin/sh

srcdir=`dirname $0`
test -z "$srcdir" && srcdir=.

ORIGDIR=`pwd`
cd $srcdir

autoreconf -v --install || exit 1
glib-gettextize --copy --force || exit 1 
intltoolize --automake --copy --force || exit 1

cd $ORIGDIR || exit $?

$srcdir/configure --enable-debug=full --enable-maintainer-mode "$@"

