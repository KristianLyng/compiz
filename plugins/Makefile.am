AM_LDFLAGS = -module -avoid-version -no-undefined

# Bcop
%_options.h: ../metadata/%.xml.in
	xsltproc --stringparam "header" "true" ${top_srcdir}/bcop/bcop.xslt $< > $@
%_options.c: ../metadata/%.xml.in %_options.h
	xsltproc --stringparam "source" "true" ${top_srcdir}/bcop/bcop.xslt $< > $@

# Ugh, it's fugly. This is only because foo.c doesn't match libfoo.la. If we
# used libfoo.c instead, then all this would be redundant.

nodist_libcolorfilter_la_SOURCES = colorfilter_options.c \
			    colorfilter_options.h
dist_libcolorfilter_la_SOURCES = colorfilter.c \
			    colorfilter-parser.c              \
			    colorfilter-parser.h

nodist_libthumbnail_la_SOURCES = thumbnail_options.c \
			  thumbnail_options.h
dist_libthumbnail_la_SOURCES = thumbnail.c \
			  thumbnail_tex.h

nodist_libscaleaddon_la_SOURCES = scaleaddon_options.c scaleaddon_options.h
dist_libscaleaddon_la_SOURCES = scaleaddon.c

nodist_libkdecompat_la_SOURCES = kdecompat_options.c kdecompat_options.h
dist_libkdecompat_la_SOURCES = kdecompat.c

nodist_libvpswitch_la_SOURCES = vpswitch_options.c vpswitch_options.h
dist_libvpswitch_la_SOURCES = vpswitch.c

nodist_libshift_la_SOURCES = shift_options.c shift_options.h
dist_libshift_la_SOURCES = shift.c

nodist_libtitleinfo_la_SOURCES = titleinfo_options.c titleinfo_options.h
dist_libtitleinfo_la_SOURCES = titleinfo.c

nodist_libput_la_SOURCES = put_options.c put_options.h
dist_libput_la_SOURCES = put.c

nodist_libsnap_la_SOURCES = snap_options.c snap_options.h
dist_libsnap_la_SOURCES = snap.c

nodist_libring_la_SOURCES = ring_options.c ring_options.h
dist_libring_la_SOURCES = ring.c

nodist_libopacify_la_SOURCES = opacify_options.c opacify_options.h
dist_libopacify_la_SOURCES = opacify.c

libsession_la_SOURCES = session.c
libwinrules_la_SOURCES = winrules.c
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
liblolconf_la_SOURCES = lolconf.c

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

if USE_RESIZEINFO
libresizeinfo_la_LIBADD = @COMPIZ_LIBS@ @PANGO_LIBS@
libresizeinfo_la_CFLAGS = @COMPIZ_CFLAGS@ @PANGO_CFLAGS@
nodist_libresizeinfo_la_SOURCES = resizeinfo_options.c \
			   resizeinfo_options.h
dist_libresizeinfo_la_SOURCES = resizeinfo.c
resizeinfo_module = libresizeinfo.la
endif

if USE_TEXT
libtext_la_LIBADD = @COMPIZ_LIBS@ @PANGO_LIBS@
libtext_la_CFLAGS = @COMPIZ_CFLAGS@ @PANGO_CFLAGS@
nodist_libtext_la_SOURCES = text_options.c text_options.h
dist_libtext_la_SOURCES = text.c
text_module = libtext.la
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

nodist_libworkarounds_la_SOURCES = workarounds_options.c \
			    workarounds_options.h
dist_libworkarounds_la_SOURCES = workarounds.c

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
	$(nodist_libsnap_la_SOURCES)		\
	$(nodist_libshift_la_SOURCES)		\
	$(nodist_libtitleinfo_la_SOURCES)	\
	$(nodist_libscaleaddon_la_SOURCES)	\
	$(nodist_libthumbnail_la_SOURCES)	\
	$(nodist_libcolorfilter_la_SOURCES)	\
	$(nodist_libput_la_SOURCES)		\
	$(nodist_libopacify_la_SOURCES)		\
	$(nodist_libworkarounds_la_SOURCES)	\
	$(nodist_libresizeinfo_la_SOURCES)	\
	$(nodist_libring_la_SOURCES)		\
	$(nodist_libvpswitch_la_SOURCES)	\
	$(nodist_libkdecompat_la_SOURCES)	\
	$(nodist_libtext_la_SOURCES)		\
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
	-DDATADIR=\"$(compdatadir)\"		\
	-DMETADATADIR=\"$(metadatadir)\"

moduledir = $(plugindir)

module_LTLIBRARIES =		\
	$(libglib_module)	\
	$(libgconf_module)	\
	$(libkconfig_module)	\
	libdecoration.la	\
	libput.la		\
	libopacify.la		\
	libworkarounds.la	\
	libwinrules.la		\
	libtitleinfo.la		\
	$(resizeinfo_module)    \
	$(text_module)          \
	libsession.la		\
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
	liblolconf.la		\
	libpng.la		\
	libblur.la		\
	libregex.la		\
	libvideo.la		\
	libini.la		\
	libobs.la		\
	libcommands.la		\
	libgnomecompat.la	\
	libring.la		\
	libsnap.la		\
	libshift.la		\
	libvpswitch.la		\
	libkdecompat.la		\
	libscaleaddon.la	\
	libthumbnail.la		\
	libcolorfilter.la	\
	$(libsvg_module)	\
	$(libannotate_module)	\
	$(libinotify_module)	\
	$(libfs_module)

SUBDIRS = animation
