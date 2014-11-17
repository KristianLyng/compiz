
AM_LDFLAGS = -module -avoid-version -no-undefined

libanimation_la_LIBADD = @COMPIZ_LIBS@
libanimation_la_SOURCES = animation.c \
			  animation-internal.h \
			  curvedfold.c \
			  dodge.c \
			  dream.c \
			  fade.c \
			  focusfade.c \
			  glide.c \
			  horizontalfold.c \
			  magiclamp.c \
			  options.c \
			  rollup.c \
			  wave.c \
			  zoomside.c

AM_CPPFLAGS =					\
	-I$(top_srcdir)/include             \
	-I$(top_builddir)/include               \
	@COMPIZ_CFLAGS@                     \
	-DDATADIR='"$(compdatadir)"'        \
	-DLIBDIR='"$(libdir)"'              \
	-DLOCALEDIR="\"@datadir@/locale\""  \
	-DIMAGEDIR='"$(imagedir)"'          

moduledir = $(plugindir)

module_LTLIBRARIES=libanimation.la
