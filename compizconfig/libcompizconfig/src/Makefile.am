if USE_PROTOBUF

PROTOBUF_LIB = -lprotobuf
PROTOBUF_DEFINES = \
	-DUSE_PROTOBUF=1

# protoc and family are retarded. That's it, why the hell are anyone using
# them.

compizconfig.pb.cc: compizconfig.proto
	protoc --cpp_out=. -I $(srcdir)/ $(srcdir)/compizconfig.proto

compizconfig.pb.h: compizconfig.pb.cc

nodist_libcompizconfig_la_SOURCES =	\
	compizconfig.pb.cc		\
	compizconfig.pb.h

BUILT_SOURCES =				\
	compizconfig.pb.cc		\
	compizconfig.pb.h

CLEANFILES =	\
	$(nodist_libcompizconfig_la_SOURCES)
endif
cc_srcdir = $(top_srcdir)/compizconfig/libcompizconfig
EXTRA_DIST = compizconfig.proto

AM_CPPFLAGS =			               \
	@COMPIZ_CFLAGS@                        \
	@LIBX11_CFLAGS@                        \
	@LIBXML2_CFLAGS@                       \
	-I$(cc_srcdir)/include	               \
	-I$(top_srcdir)/include	               \
	-I$(top_builddir)/include		\
	-I$(cc_srcdir)/src                    \
	-I$(top_srcdir)				\
	-DPLUGINDIR=\"$(PLUGINDIR)\"           \
	-DMETADATADIR=\"$(METADATADIR)\"       \
	-DLIBDIR=\"$(libdir)\"                 \
	$(PROTOBUF_DEFINES)                    \
	-DSYSCONFDIR=\"$(sysconfdir)\"


libcompizconfig_la_SOURCES = \
	main.c 		\
	lists.c 	\
	compiz.cpp 	\
	config.c 	\
	iniparser.c 	\
	ini.c 		\
	bindings.c 	\
	filewatch.c 	\
	ccs-private.h	\
	iniparser.h

libcompizconfig_la_LIBADD = @LIBXML2_LIBS@ @LIBX11_LIBS@ $(PROTOBUF_LIB)

lib_LTLIBRARIES=libcompizconfig.la

