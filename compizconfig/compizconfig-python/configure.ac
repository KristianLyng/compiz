AC_PREREQ(2.57)
AC_INIT([compizconfig-python],esyscmd(. ./VERSION;echo -n $VERSION), [livinglatexkali@gmail.com])

AM_INIT_AUTOMAKE([1.9 dist-bzip2])
AC_CONFIG_HEADER([config.h])
AM_MAINTAINER_MODE

AC_ISC_POSIX
AC_PROG_CC
AC_PROG_CPP
AC_PROG_LIBTOOL
AC_HEADER_STDC

CCS_REQUIRES="\
libcompizconfig >= 0.6.99 \
glib-2.0 >= 2.6 "

PKG_CHECK_MODULES(CCS,$CCS_REQUIRES)

AC_SUBST(CCS_REQUIRES)

dnl PYTHON SPECIFIC

m4_define(required_python_abi,2.4)

AM_PATH_PYTHON
if test "$PYTHON_VERSION" = "2.4"
then
	AM_PATH_PYTHON_VERSION(2.4,2.4.0)
else
	AM_PATH_PYTHON_VERSION(2.5,2.5.0)
fi

AC_CHECK_PROGS(PYREX, pyrexc)
if test -z "$PYREX"
then
	AC_MSG_ERROR([Couldn't find Pyrex])
fi

AC_CONFIG_FILES([
	compizconfig-python.pc
	Makefile
	src/Makefile
])

AC_OUTPUT
