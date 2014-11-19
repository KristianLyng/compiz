compizincludedir = $(includedir)/compiz
compizinclude_HEADERS = \
	compiz.h	\
	compiz-plugin.h	\
	compiz-core.h	\
	compiz-cube.h   \
	compiz-scale.h	\
	compiz-mousepoll.h \
	decoration.h

nodist_compizinclude_HEADERS = \
	compiz-common.h		\
	compiz-version.h

BUILT_SOURCES = compiz-version.h compiz-common.h
MAINTAINERCLEANFILES = compiz-version.h

# compiz-version.h is generated using git and tags. It's very clever.
#
# Stolen galantly from varnish-agent 2 (MIT, copyright Varnish Software,
# written by KristianL), where I stole some of it galantly from
# varnish-cache and possible the varnish training material. I'm a pretty
# good thief, but it was all MIT and written largely by me. By now, the
# comment is almost bigger than the "code" anyway. If you are still reading
# this, you should go fix some bugs instead. Shoo, off with you.

compiz-version.h: FORCE
	if [ -d "$(top_srcdir)/.git" ]; then \
		V="$$(git describe --always --tags --dirty)" \
		H="$$(head -n 1 compiz-version.h 2>/dev/null || true)"; \
		echo "V: $$V"; \
		if [ "/* $$V */" != "$$H" ]; then \
		( \
		  echo "/* $$V */" ;\
		  echo '/*' ;\
		  echo ' * NB:  This file is machine generated, DO NOT EDIT!' ;\
		  echo ' *' ;\
		  echo ' * Run make to regenerate' ;\
		  echo ' *'  ;\
		  echo ' */' ;\
		  echo "/* $$V */" ;\
		  echo '' ;\
		  echo "#define COMPIZ_Version \"$$V\"" \
		) > compiz-version.h ; \
		fi \
	else \
		if [ ! -f compiz-version.h ]; then \
		( \
		  echo "/* NOGIT */" ; \
		  echo '/* No git commit ID available, see include/Makefile.am for explanation */' ; \
		  echo '#define COMPIZ_Version "NOGIT"' \
		) >  compiz-version.h ; \
		fi \
	fi
DISTCLEANFILES = compiz-common.h

FORCE:
