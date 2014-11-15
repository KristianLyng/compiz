AM_LDFLAGS = -module -avoid-version -no-undefined

# Bcop
%_options.h: ../metadata/%.xml.in
	xsltproc --stringparam "header" "true" ${top_srcdir}/bcop/bcop.xslt $< > $@
%_options.c: ../metadata/%.xml.in %_options.h
	xsltproc --stringparam "source" "true" ${top_srcdir}/bcop/bcop.xslt $< > $@

# Ugh, it's fugly. This is only because foo.c doesn't match libfoo.la. If we
# used libfoo.c instead, then all this would be redundant.
libfade_la_SOURCES = fade.c
libcube_la_SOURCES = cube.c
librotate_la_SOURCES = rotate.c
libzoom_la_SOURCES = zoom.c
libezoom_la_SOURCES = ezoom.c
libmousepoll_la_SOURCES = mousepoll.c
libscale_la_SOURCES = scale.c
libwobbly_la_SOURCES = wobbly.c
libminimize_la_SOURCES = minimize.c
libmove_la_SOURCES = move.c
libresize_la_SOURCES = resize.c
libplace_la_SOURCES = place.c
libswitcher_la_SOURCES = switcher.c
libwater_la_SOURCES = water.c
libscreenshot_la_SOURCES = screenshot.c
libclone_la_SOURCES = clone.c
libvideo_la_SOURCES = video.c
libregex_la_SOURCES = regex.c
libini_la_SOURCES = ini.c
libobs_la_SOURCES = obs.c
libcommands_la_SOURCES = commands.c
libgnomecompat_la_SOURCES = gnomecompat.c
libpng_la_LIBADD = @LIBPNG_LIBS@
libpng_la_SOURCES = png.c

libdecoration_la_DEPENDENCIES = $(top_builddir)/libdecoration/libdecoration.la
libdecoration_la_LIBADD = $(top_builddir)/libdecoration/libdecoration.la
libdecoration_la_SOURCES = decoration.c

libblur_la_DEPENDENCIES = $(top_builddir)/libdecoration/libdecoration.la
libblur_la_LIBADD = $(top_builddir)/libdecoration/libdecoration.la -lGLU
libblur_la_SOURCES = blur.c

libvideo_la_DEPENDENCIES = $(top_builddir)/libdecoration/libdecoration.la
libvideo_la_LIBADD = $(top_builddir)/libdecoration/libdecoration.la

if USE_LIBRSVG
libsvg_la_DEPENDENCIES = $(top_builddir)/libdecoration/libdecoration.la
libsvg_la_LIBADD =				       \
	$(top_builddir)/libdecoration/libdecoration.la \
	@LIBRSVG_LIBS@
libsvg_la_SOURCES = svg.c
libsvg_module = libsvg.la
endif

if USE_ANNOTATE
libannotate_la_CFLAGS = @CAIRO_XLIB_XRENDER_CFLAGS@
libannotate_la_LIBADD = @CAIRO_XLIB_XRENDER_LIBS@
libannotate_la_SOURCES = annotate.c
libannotate_module = libannotate.la
endif

if USE_GLIB
libglib_la_LIBADD = @GLIB_LIBS@
libglib_la_SOURCES = glib.c
libglib_module = libglib.la
endif

if USE_GCONF
libgconf_la_LIBADD = @GCONF_LIBS@
libgconf_la_SOURCES = gconf.c
libgconf_module = libgconf.la
endif

if USE_KCONFIG
libkconfig_la_LIBADD = @KCONFIG_LIBS@
libkconfig_la_SOURCES = kconfig.cpp
libkconfig_module = libkconfig.la
endif

if USE_DBUS
libdbus_la_LIBADD = @DBUS_LIBS@
libdbus_la_SOURCES = dbus.c
libdbus_module = libdbus.la
endif

if USE_INOTIFY 
libinotify_la_SOURCES = inotify.c
libinotify_module = libinotify.la
endif

if USE_FUSE
libfs_la_LIBADD = @FUSE_LIBS@
libfs_la_SOURCES = fuse.c
libfs_module = libfs.la
endif

if USE_WALL
libwall_la_CFLAGS = @CAIRO_CFLAGS@
libwall_la_LIBADD = @CAIRO_LIBS@
nodist_libwall_la_SOURCES = wall_options.c \
			       wall_options.h
dist_libwall_la_SOURCES = wall.c
libwall_module = libwall.la
libwall_built_sources = wall_options.c wall_options.h
endif

nodist_libstaticswitcher_la_SOURCES = staticswitcher_options.c \
			       staticswitcher_options.h
dist_libstaticswitcher_la_SOURCES = staticswitcher.c

nodist_libneg_la_SOURCES = neg_options.c \
			       neg_options.h
dist_libneg_la_SOURCES = neg.c

nodist_libmag_la_SOURCES = mag_options.c \
			       mag_options.h
dist_libmag_la_SOURCES = mag.c

if USE_JPEG
libimgjpeg_la_CFLAGS = @JPEG_CFLAGS@
libimgjpeg_la_LIBADD = @JPEG_LIBS@
nodist_libimgjpeg_la_SOURCES = imgjpeg_options.c \
			       imgjpeg_options.h
dist_libimgjpeg_la_SOURCES = imgjpeg.c
libimgjpeg_module = libimgjpeg.la
endif

nodist_libexpo_la_SOURCES = expo_options.c \
			       expo_options.h
dist_libexpo_la_SOURCES = expo.c

BUILT_SOURCES = \
	$(nodist_libstaticswitcher_la_SOURCES)	\
	$(nodist_libexpo_la_SOURCES)		\
	$(nodist_libmag_la_SOURCES)		\
	$(nodist_libneg_la_SOURCES)		\
	$(nodist_libimgjpeg_la_SOURCES)		\
	$(libwall_built_sources)

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
	libneg.la		\
	libmag.la		\
	$(libimgjpeg_module)	\
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

