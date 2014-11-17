CFLAGS="-Wall"
AM_CPPFLAGS=\
		 @PYTHON_CFLAGS@\
		 @GLIB_CFLAGS@

compizconfig.c: $(top_srcdir)/compizconfig/compizconfig-python/src/compizconfig.pyx
	-pyrexc $(top_srcdir)/compizconfig/compizconfig-python/src/compizconfig.pyx -o compizconfig.c

compizconfig_la_LDFLAGS = -module -avoid-version -fPIC -export-symbols-regex initcompizconfig -lX11
compizconfig_la_LIBADD = @GLIB_LIBS@ $(top_builddir)/compizconfig/libcompizconfig/src/libcompizconfig.la
compizconfig_la_SOURCES = compizconfig.c
compizconfigdir=$(pyexecdir)
compizconfig_LTLIBRARIES=compizconfig.la

EXTRA_DIST=compizconfig.pyx

clean-local:
	rm -f compizconfig.c
