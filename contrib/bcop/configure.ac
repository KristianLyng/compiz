AC_PREREQ(2.57)

AC_INIT([compiz-bcop],esyscmd(. ./VERSION;echo -n $VERSION), [onestone@beryl-project.org])

AC_DEFINE_UNQUOTED(VERSION,"$VERSION",[Version])

AM_INIT_AUTOMAKE([1.9 dist-bzip2])
AC_CONFIG_HEADER([config.h])
AM_MAINTAINER_MODE

AC_ISC_POSIX
AC_PROG_CC
AC_HEADER_STDC

AC_C_BIGENDIAN

PKG_CHECK_MODULES(LIBXSLT, libxslt)

xsltdir=$datadir/bcop
AC_SUBST(xsltdir)

AC_OUTPUT([
bcop.pc
Makefile
src/Makefile
src/bcop
])
