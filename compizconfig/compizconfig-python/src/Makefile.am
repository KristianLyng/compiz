INCLUDES=\
		 $(PYTHON_INCLUDES)\
		 @CCS_CFLAGS@

compizconfig.c: compizconfig.pyx
	-pyrexc compizconfig.pyx

compizconfig_la_LDFLAGS = -module -avoid-version -fPIC -export-symbols-regex initcompizconfig -lX11
compizconfig_la_LIBADD = @CCS_LIBS@
compizconfig_la_SOURCES = compizconfig.c
compizconfigdir=$(pyexecdir)
compizconfig_LTLIBRARIES=compizconfig.la

EXTRA_DIST=compizconfig.pyx

clean-local:
	rm -f compizconfig.c
