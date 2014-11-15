libfade_la_LDFLAGS = -module -avoid-version -no-undefined
libfade_la_SOURCES = fade.c

libcube_la_LDFLAGS = -module -avoid-version -no-undefined
libcube_la_SOURCES = cube.c

librotate_la_LDFLAGS = -module -avoid-version -no-undefined
librotate_la_SOURCES = rotate.c

libzoom_la_LDFLAGS = -module -avoid-version -no-undefined
libzoom_la_SOURCES = zoom.c

libezoom_la_LDFLAGS = -module -avoid-version -no-undefined
libezoom_la_SOURCES = ezoom.c

libstaticswitcher_la_LDFLAGS = -module -avoid-version -no-undefined
nodist_libstaticswitcher_la_SOURCES = staticswitcher_options.c \
			       staticswitcher_options.h
dist_libstaticswitcher_la_SOURCES = staticswitcher.c

if USE_WALL
libwall_la_LDFLAGS = -module -avoid-version -no-undefined
libwall_la_CFLAGS = @CAIRO_CFLAGS@
libwall_la_LIBADD = @CAIRO_LIBS@
nodist_libwall_la_SOURCES = wall_options.c \
			       wall_options.h
dist_libwall_la_SOURCES = wall.c
libwall_module = libwall.la
endif

libexpo_la_LDFLAGS = -module -avoid-version -no-undefined
nodist_libexpo_la_SOURCES = expo_options.c \
			       expo_options.h
dist_libexpo_la_SOURCES = expo.c

libmousepoll_la_LDFLAGS = -module -avoid-version -no-undefined
libmousepoll_la_SOURCES = mousepoll.c

libscale_la_LDFLAGS = -module -avoid-version -no-undefined
libscale_la_SOURCES = scale.c

libwobbly_la_LDFLAGS = -module -avoid-version -no-undefined
libwobbly_la_SOURCES = wobbly.c

libminimize_la_LDFLAGS = -module -avoid-version -no-undefined
libminimize_la_SOURCES = minimize.c

libmove_la_LDFLAGS = -module -avoid-version -no-undefined
libmove_la_SOURCES = move.c

libresize_la_LDFLAGS = -module -avoid-version -no-undefined
libresize_la_SOURCES = resize.c

libplace_la_LDFLAGS = -module -avoid-version -no-undefined
libplace_la_SOURCES = place.c

libdecoration_la_DEPENDENCIES = $(top_builddir)/libdecoration/libdecoration.la
libdecoration_la_LDFLAGS = -module -avoid-version -no-undefined
libdecoration_la_LIBADD = $(top_builddir)/libdecoration/libdecoration.la
libdecoration_la_SOURCES = decoration.c

libswitcher_la_LDFLAGS = -module -avoid-version -no-undefined
libswitcher_la_SOURCES = switcher.c

libwater_la_LDFLAGS = -module -avoid-version -no-undefined
libwater_la_SOURCES = water.c

libscreenshot_la_LDFLAGS = -module -avoid-version -no-undefined
libscreenshot_la_SOURCES = screenshot.c

libclone_la_LDFLAGS = -module -avoid-version -no-undefined
libclone_la_SOURCES = clone.c

libpng_la_LDFLAGS = -module -avoid-version -no-undefined
libpng_la_LIBADD = @LIBPNG_LIBS@
libpng_la_SOURCES = png.c

libblur_la_DEPENDENCIES = $(top_builddir)/libdecoration/libdecoration.la
libblur_la_LDFLAGS = -module -avoid-version -no-undefined
libblur_la_LIBADD = $(top_builddir)/libdecoration/libdecoration.la -lGLU
libblur_la_SOURCES = blur.c

libregex_la_LDFLAGS = -module -avoid-version -no-undefined
libregex_la_SOURCES = regex.c

libvideo_la_DEPENDENCIES = $(top_builddir)/libdecoration/libdecoration.la
libvideo_la_LDFLAGS = -module -avoid-version -no-undefined
libvideo_la_LIBADD = $(top_builddir)/libdecoration/libdecoration.la
libvideo_la_SOURCES = video.c

libini_la_LDFLAGS = -module -avoid-version -no-undefined
libini_la_SOURCES = ini.c

libobs_la_LDFLAGS = -module -avoid-version -no-undefined
libobs_la_SOURCES = obs.c

libcommands_la_LDFLAGS = -module -avoid-version -no-undefined
libcommands_la_SOURCES = commands.c

libgnomecompat_la_LDFLAGS = -module -avoid-version -no-undefined
libgnomecompat_la_SOURCES = gnomecompat.c

if USE_LIBRSVG
libsvg_la_DEPENDENCIES = $(top_builddir)/libdecoration/libdecoration.la
libsvg_la_LDFLAGS = -module -avoid-version -no-undefined
libsvg_la_LIBADD =				       \
	$(top_builddir)/libdecoration/libdecoration.la \
	@LIBRSVG_LIBS@
libsvg_la_SOURCES = svg.c
libsvg_module = libsvg.la
endif

if USE_ANNOTATE
libannotate_la_LDFLAGS = -module -avoid-version -no-undefined
libannotate_la_CFLAGS = @CAIRO_XLIB_XRENDER_CFLAGS@
libannotate_la_LIBADD = @CAIRO_XLIB_XRENDER_LIBS@
libannotate_la_SOURCES = annotate.c
libannotate_module = libannotate.la
endif

if USE_GLIB
libglib_la_LDFLAGS = -module -avoid-version -no-undefined
libglib_la_LIBADD = @GLIB_LIBS@
libglib_la_SOURCES = glib.c
libglib_module = libglib.la
endif

if USE_GCONF
libgconf_la_LDFLAGS = -module -avoid-version -no-undefined
libgconf_la_LIBADD = @GCONF_LIBS@
libgconf_la_SOURCES = gconf.c
libgconf_module = libgconf.la
endif

if USE_KCONFIG
libkconfig_la_LDFLAGS = -module -avoid-version -no-undefined
libkconfig_la_LIBADD = @KCONFIG_LIBS@
libkconfig_la_SOURCES = kconfig.cpp
libkconfig_module = libkconfig.la
endif

if USE_DBUS
libdbus_la_LDFLAGS = -module -avoid-version -no-undefined
libdbus_la_LIBADD = @DBUS_LIBS@
libdbus_la_SOURCES = dbus.c
libdbus_module = libdbus.la
endif

if USE_INOTIFY 
libinotify_la_LDFLAGS = -module -avoid-version -no-undefined
libinotify_la_SOURCES = inotify.c
libinotify_module = libinotify.la
endif

if USE_FUSE
libfs_la_LDFLAGS = -module -avoid-version -no-undefined
libfs_la_LIBADD = @FUSE_LIBS@
libfs_la_SOURCES = fuse.c
libfs_module = libfs.la
endif

staticswitcher_options.h: ../metadata/staticswitcher.xml.in
	xsltproc --stringparam "header" "true" ${top_srcdir}/bcop/bcop.xslt $< > $@

staticswitcher_options.c: ../metadata/staticswitcher.xml.in staticswitcher_options.h
	xsltproc --stringparam "source" "true" ${top_srcdir}/bcop/bcop.xslt $< > $@

wall_options.h: ../metadata/wall.xml.in
	xsltproc --stringparam "header" "true" ${top_srcdir}/bcop/bcop.xslt $< > $@

wall_options.c: ../metadata/wall.xml.in wall_options.h
	xsltproc --stringparam "source" "true" ${top_srcdir}/bcop/bcop.xslt $< > $@

expo_options.h: ../metadata/expo.xml.in
	xsltproc --stringparam "header" "true" ${top_srcdir}/bcop/bcop.xslt $< > $@

expo_options.c: ../metadata/expo.xml.in expo_options.h
	xsltproc --stringparam "source" "true" ${top_srcdir}/bcop/bcop.xslt $< > $@

BUILT_SOURCES = $(nodist_libstaticswitcher_la_SOURCES)

CLEANFILES = *_options.c *_options.h

AM_CPPFLAGS =					\
	@COMPIZ_CFLAGS@				\
	@LIBPNG_CFLAGS@				\
	@LIBRSVG_CFLAGS@			\
	@GCONF_CFLAGS@				\
	@KCONFIG_CFLAGS@			\
	@DBUS_CFLAGS@				\
	@GLIB_CFLAGS@				\
	@FUSE_CFLAGS@				\
	-DFUSE_USE_VERSION=26			\
	-DALL_LINGUAS="\"@ALL_LINGUAS@\""	\
	-DLOCALEDIR="\"@datadir@/locale\""	\
	-DPLUGINDIR=\"$(plugindir)\"		\
	-DIMAGEDIR=\"$(imagedir)\"		\
	-I$(top_srcdir)/include                 \
	-I$(top_builddir)/include               \
	-DMETADATADIR=\"$(metadatadir)\"

moduledir = $(plugindir)

module_LTLIBRARIES =		\
	$(libglib_module)	\
	$(libgconf_module)	\
	$(libkconfig_module)	\
	libdecoration.la	\
	libwobbly.la		\
	libfade.la		\
	libminimize.la		\
	libcube.la		\
	libezoom.la		\
	libmousepoll.la		\
	libstaticswitcher.la	\
	$(libwall_module)	\
	libexpo.la		\
	librotate.la		\
	libzoom.la		\
	libscale.la		\
	libmove.la		\
	libresize.la		\
	libplace.la             \
	$(libdbus_module)	\
	libswitcher.la		\
	libwater.la		\
	libscreenshot.la	\
	libclone.la		\
	libpng.la		\
	libblur.la		\
	libregex.la		\
	libvideo.la		\
	libini.la		\
	libobs.la		\
	libcommands.la		\
	libgnomecompat.la	\
	$(libsvg_module)	\
	$(libannotate_module)	\
	$(libinotify_module)	\
	$(libfs_module)

