## Process this file with automake to produce Makefile.in

cc_srcdir = $(top_srcdir)/compizconfig/libcompizconfig
AM_CPPFLAGS =			     \
	@COMPIZ_CFLAGS@ \
	-I$(top_srcdir)/include	     \
	-I$(cc_srcdir)/include	               \
	-I$(top_builddir)/include		\
	-I$(cc_srcdir)/src                    \
	-I$(top_srcdir)				\
	-DPLUGINDIR=\"$(PLUGINDIR)\" \
	-DLIBDIR=\"$(libdir)\"

libini_la_LDFLAGS = -module -avoid-version -no-undefined $(all_libraries)
libini_la_LIBADD  = $(top_builddir)/compizconfig/libcompizconfig/src/libcompizconfig.la
libini_la_SOURCES = ini.c
backenddir = $(libdir)/compizconfig/backends

METASOURCES = AUTO

backend_LTLIBRARIES = libini.la

