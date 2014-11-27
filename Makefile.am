SUBDIRS = include src libdecoration plugins images gtk kde po metadata bcop compizconfig/libcompizconfig compizconfig/compizconfig-python

EXTRA_DIST =				\
	COPYING				\
	COPYING.GPL			\
	COPYING.LGPL			\
	COPYING.MIT			\
	INSTALL				\
	README.rst			\
	pc/compiz.pc.in			\
	pc/compiz-mousepoll.pc.in	\
	pc/compiz-cube.pc.in		\
	pc/compiz-scale.pc.in		\
	pc/compiz-gconf.pc.in		\
	pc/bcop.pc

DISTCLEANFILES =	 \
	po/stamp-it	 \
	po/.intltool-merge-cache

if USE_GCONF
gconfdata = pc/compiz-gconf.pc
endif

if USE_KCONFIG
kconfigdata = pc/compiz-kconfig.pc
endif

pkgconfigdir = $(libdir)/pkgconfig
pkgconfig_DATA =	    \
	pc/compiz.pc	    \
	pc/compiz-cube.pc   \
	pc/compiz-scale.pc  \
	pc/compiz-mousepoll.pc \
	pc/bcop.pc          \
	$(gconfdata)	    \
	$(kconfigdata)

dist_man_MANS = compiz.1
MAINTAINERCLEANFILES = $(dist_man_MANS)

compiz.1: $(top_srcdir)/README.rst
if HAVE_RST2MAN
	${RST2MAN} $? $@
else
	@echo "========================================"
	@echo "You need rst2man installed to make dist"
	@echo "========================================"
	@false
endif

ACLOCAL_AMFLAGS = -I m4
