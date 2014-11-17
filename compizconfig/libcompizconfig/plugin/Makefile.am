cc_srcdir = $(top_srcdir)/compizconfig/libcompizconfig
AM_CPPFLAGS =			     \
	@COMPIZ_CFLAGS@ \
	-I$(top_srcdir)/include	     \
	-I$(top_srcdir)/src \
	-I$(cc_srcdir)/include	               \
	-I$(cc_srcdir)/src                    \
	-I$(top_builddir)/include		\
	-DPLUGINDIR=\"$(plugindir)\" \
	-DLIBDIR=\"$(libdir)\"

libccp_la_LDFLAGS = -module -avoid-version -no-undefined
libccp_la_LIBADD = $(top_builddir)/compizconfig/libcompizconfig/src/libcompizconfig.la
libccp_la_SOURCES = ccp.c

moduledir = $(plugindir)

module_LTLIBRARIES = libccp.la

