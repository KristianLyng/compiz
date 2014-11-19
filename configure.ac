AC_PREREQ(2.57)
#ACLOCAL_AMFLAGS = --install -I m4

dnl compiz package version number
dnl An odd micro number indicates in-progress development.
dnl An even micro number indicates a released version.
m4_define(compiz_version_major, 0)
m4_define(compiz_version_minor, 8)
m4_define(compiz_version_micro, 11)

AC_INIT([compiz],
	[compiz_version_major().compiz_version_minor().compiz_version_micro()],
	[https://github.com/KristianLyng/compiz/issues])
#AC_CONFIG_SRCDIR([src/main.c])
COMPIZ_VERSION_MAJOR=compiz_version_major()
COMPIZ_VERSION_MINOR=compiz_version_minor()
COMPIZ_VERSION_MICRO=compiz_version_micro()
AC_SUBST(COMPIZ_VERSION_MAJOR)
AC_SUBST(COMPIZ_VERSION_MINOR)
AC_SUBST(COMPIZ_VERSION_MICRO)

AM_INIT_AUTOMAKE([foreign])
AM_SILENT_RULES([yes])
AC_CONFIG_MACRO_DIR([m4])
AC_CONFIG_HEADER([config.h])
AC_PROG_INTLTOOL([0.23])
AM_MAINTAINER_MODE
AM_GCONF_SOURCE_2

# Check for rst utilities
AC_ARG_WITH([rst2man],
	       AS_HELP_STRING([--with-rst2man=PATH],
			      [Location of rst2man (auto)]),
	       [RST2MAN="$withval"],
	       [AC_CHECK_PROGS(RST2MAN, [rst2man rst2man.py], "no")
		if test "x$RST2MAN" = "xno"; then
		   AC_MSG_WARN([rst2man not found – not building man pages])
		fi])
AM_CONDITIONAL(HAVE_RST2MAN,[test "x$RST2MAN" != "xno"])

dnl decorator interface version
AC_DEFINE(DECOR_INTERFACE_VERSION, 20080529, [Decorator interface version])

AC_ISC_POSIX
AC_PROG_CC
AC_PROG_CPP
AC_PROG_CXX
AC_PROG_LIBTOOL
AC_HEADER_STDC
AC_CHECK_HEADERS([stdlib.h sys/time.h unistd.h])

ALL_LINGUAS="af ar bg bn bn_IN bs ca cs cy da de el en_GB en_US es eu et fi fr gl gu he hi hr hu id it ja ka km ko lo lt mk mr nb nl or pa pl pt pt_BR ro ru sk sl sr sv ta tr uk vi xh zh_CN zh_TW zu"
AC_SUBST(ALL_LINGUAS)
AM_GLIB_GNU_GETTEXT
GETTEXT_PACKAGE=compiz
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE,"$GETTEXT_PACKAGE", [Gettext package.])
AC_SUBST(GETTEXT_PACKAGE)
missing_optional_deps=""
if test "x$GCC" = "xyes"; then
  case " $CFLAGS " in
  *[[\ \	]]-Wall[[\ \	]]*) ;;
  *) CFLAGS="$CFLAGS -Wall" ;;
  esac

  case " $CFLAGS " in
  *[[\ \	]]-Wpointer-arith[[\ \	]]*) ;;
  *) CFLAGS="$CFLAGS -Wpointer-arith" ;;
  esac

  case " $CFLAGS " in
  *[[\ \	]]-Wstrict-prototypes[[\ \	]]*) ;;
  *) CFLAGS="$CFLAGS -Wstrict-prototypes" ;;
  esac

  case " $CFLAGS " in
  *[[\ \	]]-Wmissing-prototypes[[\ \	]]*) ;;
  *) CFLAGS="$CFLAGS -Wmissing-prototypes" ;;
  esac

  case " $CFLAGS " in
  *[[\ \	]]-Wmissing-declarations[[\ \	]]*) ;;
  *) CFLAGS="$CFLAGS -Wmissing-declarations" ;;
  esac

  case " $CFLAGS " in
  *[[\ \	]]-Wnested-externs[[\ \	]]*) ;;
  *) CFLAGS="$CFLAGS -Wnested-externs" ;;
  esac

  case " $CFLAGS " in
  *[[\ \	]]-D_FORTIFY_SOURCE=2[[\ \	]]*) ;;
  *) CFLAGS="$CFLAGS -D_FORTIFY_SOURCE=2" ;;
  esac

  if test "x$enable_ansi" = "xyes"; then
    case " $CFLAGS " in
    *[[\ \	]]-ansi[[\ \	]]*) ;;
    *) CFLAGS="$CFLAGS -ansi" ;;
    esac

    case " $CFLAGS " in
    *[[\ \	]]-pedantic[[\ \	]]*) ;;
    *) CFLAGS="$CFLAGS -pedantic" ;;
    esac
  fi
fi

if test "x$GCC" = "xyes"; then
  case " $CXXFLAGS " in
  *[[\ \	]]-Wall[[\ \	]]*) ;;
  *) CXXFLAGS="$CXXFLAGS -Wall" ;;
  esac

  case " $CXXFLAGS " in
  *[[\ \	]]-D_FORTIFY_SOURCE=2[[\ \	]]*) ;;
  *) CXXFLAGS="$CXXFLAGS -D_FORTIFY_SOURCE=2" ;;
  esac
fi
CFLAGS="$CFLAGS -Wshadow -Werror"
AC_C_BIGENDIAN

stylesheetdir=$datadir/compiz
AC_SUBST(stylesheetdir)

compdatadir=$datadir/compiz
AC_SUBST(compdatadir)

plugindir=$libdir/compiz
AC_SUBST(plugindir)

AC_ARG_WITH(default-plugins, 
	       AS_HELP_STRING([--with-default-plugins=PLUGINS],
			      [Comma-separated list of default plugins(mousepoll,ezoom,png,cube,rotate,staticswitcher,move,resize,place,decoration)]),
		       [default_plugins="$withval"],
		       [default_plugins="mousepoll,ezoom,png,cube,rotate,staticswitcher,move,resize,place,decoration"])
AC_SUBST(default_plugins)

imagedir=$datadir/compiz
AC_SUBST(imagedir)

metadatadir=$datadir/compiz
AC_SUBST(metadatadir)

COMPIZ_REQUIRES="x11        \
		 xcomposite \
		 xext       \
		 xfixes	    \
		 xdamage    \
		 xrandr	    \
		 xinerama   \
		 ice	    \
		 sm	    \
		 libxml-2.0 \
		 libxslt    \
		 libstartup-notification-1.0 >= 0.7"

PKG_CHECK_MODULES(COMPIZ, $COMPIZ_REQUIRES)
AC_SUBST(COMPIZ_REQUIRES)

PKG_CHECK_MODULES(LIBX11, "x11")
DECORATION_REQUIRES="xrender"

PKG_CHECK_MODULES(DECORATION, $DECORATION_REQUIRES)
AC_SUBST(DECORATION_REQUIRES)

PKG_CHECK_EXISTS(xrender >= 0.9.3,
		 [have_xrender_0_9_3=yes], [have_xrender_0_9_3=no])

if test "$have_xrender_0_9_3" = yes; then
  AC_DEFINE(HAVE_XRENDER_0_9_3, 1,
	    [Define to 1 if xrender version >= 0.9.3])
fi

AC_MSG_CHECKING(for GL_CFLAGS)
AC_ARG_WITH(gl-cflags, [  --with-gl-cflags=CFLAGS ],
		       [GL_CFLAGS="$withval"],
		       [GL_CFLAGS=""])

AC_MSG_RESULT($GL_CFLAGS)
AC_MSG_CHECKING(for GL_LIBS)
AC_ARG_WITH(gl-libs, [  --with-gl-libs=LIBS ],
		     [GL_LIBS="$withval"],
		     [GL_LIBS="-lGL"])
AC_MSG_RESULT($GL_LIBS)

AC_SUBST(GL_CFLAGS)
AC_SUBST(GL_LIBS)

AC_CHECK_PROGS(XSLTPROC, xsltproc)
if test -z "$XSLTPROC"; then
  AC_MSG_ERROR([Couldn't find xsltproc])
fi

AM_PATH_PYTHON
PKG_CHECK_MODULES(LIBPNG, libpng)
PKG_CHECK_MODULES(PYTHON, python)
PKG_CHECK_MODULES(LIBXML2, "libxml-2.0", [have_xml2=yes],[have_xml2=no])
PKG_CHECK_MODULES(GLIB, glib-2.0,[have_glib=yes],[have_glib=no])
PKG_CHECK_MODULES(GCONF, gconf-2.0, [have_gconf2=yes],[have_gconf2=no])
PKG_CHECK_MODULES(DBUS, dbus-1 libxml-2.0, [have_dbus=yes], [have_dbus=no])
PKG_CHECK_MODULES(DBUS_GLIB, dbus-glib-1, [have_dbus_glib=yes], [have_dbus_glib=no])
PKG_CHECK_MODULES(JPEG, libjpeg, [have_jpeg=yes], [have_jpeg=no])

AC_CHECK_HEADERS([sys/inotify.h], [have_inotify=yes], [have_inotify=no])
PKG_CHECK_MODULES(FUSE, fuse, [have_fuse=yes], [have_fuse=no])
PKG_CHECK_MODULES(CAIRO_XLIB_XRENDER, cairo-xlib-xrender, [have_cairo_xlib_xrender=yes], [have_cairo_xlib_xrender=no])
PKG_CHECK_MODULES(CAIRO, cairo-xlib-xrender cairo >= 1.0, [have_cairo=yes], [have_cairo=no])
PKG_CHECK_MODULES(PANGO, pangocairo, [have_pango=yes], [have_pango=no])

AC_ARG_ENABLE(debug,
  [  --enable-debug	     Enable debug mode],
  [use_debug=$enableval], [use_debug=false])
if test "x$use_debug" = "xyes"; then
    AC_DEFINE(DEBUG, 1, [Enable debug output])
fi
AC_ARG_ENABLE(text,
  [  --disable-text          Disable text],
  [use_text=$enableval], [use_text=yes])
AC_ARG_ENABLE(resizeinfo,
  [  --disable-resizeinfo    Disable resizeinfo],
  [use_resizeinfo=$enableval], [use_resizeinfo=yes])
AC_ARG_ENABLE(dbus-glib,
  [  --disable-dbus-glib     Disable dbus-glib support in gtk-window-decorator],
  [use_dbus_glib=$enableval], [use_dbus_glib=yes])
AC_ARG_ENABLE(annotate,
  [  --disable-annotate      Disable annotate plugin],
  [use_annotate=$enableval], [use_annotate=yes])
AC_ARG_ENABLE(jpeg,
  [  --disable-jpeg          Disable jpeg plugin],
  [use_jpeg=$enableval], [use_jpeg=yes])
AC_ARG_ENABLE(wall,
  [  --disable-wall          Disable wall plugin],
  [use_wall=$enableval], [use_wall=yes])
AC_ARG_ENABLE(fuse,
  [  --disable-fuse          Disable fuse plugin],
  [use_fuse=$enableval], [use_fuse=yes])
AC_ARG_ENABLE(inotify,
  [  --disable-inotify       Disable inotify plugin],
  [use_inotify=$enableval], [use_inotify=yes])
AC_ARG_ENABLE(glib,
  [  --disable-glib          Disable glib plugin],
  [use_glib=$enableval], [use_glib=yes])
AC_ARG_ENABLE(gconf,
  [  --disable-gconf         Disable gconf plugin],
  [use_gconf=$enableval], [use_gconf=yes])
AC_ARG_ENABLE(dbus,
  [  --disable-dbus          Disable dbus plugin],
  [use_dbus=$enableval], [use_dbus=yes])

if test "x$have_pango" != "xyes"; then
  use_resizeinfo="no"
  use_text="no"
  missing_optional_deps="${missing_optional_deps} pango(text, resizeinfo)"
fi
if test "x$have_jpeg" != "xyes"; then
  use_jpeg="no"
  missing_optional_deps="${missing_optional_deps} libjpeg"
fi
if test "x$have_glib" != "xyes"; then
  use_glib="no"
  missing_optional_deps="${missing_optional_deps} glib"
fi

if test "x$have_dbus" != "xyes"; then
    use_dbus=no
    missing_optional_deps="${missing_optional_deps} dbus"
fi

if test "x$have_inotify" != "xyes"; then
   use_inotify="no"
   missing_optional_deps="${missing_optional_deps} inotify"
fi

if test "x$have_fuse" != "xyes"; then
   use_fuse="no"
   missing_optional_deps="${missing_optional_deps} fuse"
fi

if test "x$have_cairo" != "xyes"; then
    use_wall="no"
    missing_optional_deps="${missing_optional_deps} cairo(wall plugin)"
fi

if test "x$have_cairo_xlib_xrender" != "xyes"; then
    use_annotate="no"
    missing_optional_deps="${missing_optional_deps} cairo_xlib_xrender(annotate plugin)"
fi

if test "x$have_gconf2" != "xyes"; then
  use_gconf="no"
  missing_optional_deps="${missing_optional_deps} gconf"
else
  AC_PATH_PROG(GCONFTOOL, gconftool-2, no)
  if test x"$GCONFTOOL" = xno; then
    AC_MSG_ERROR([gconftool-2 executable not found in your path - should be installed with GConf])
  fi
fi

if test "x$have_dbus_glib" != "xyes"; then
  use_dbus_glib="no"
  missing_optional_deps="${missing_optional_deps} dbus-glib(gtk-window-decorator)"
fi

if test "x$use_dbus_glib" = "xyes"; then
  AC_DEFINE(USE_DBUS_GLIB, 1, [Build dbus glib support])
fi

AM_CONDITIONAL(USE_TEXT, test "x$use_text" = "xyes")
AM_CONDITIONAL(USE_RESIZEINFO, test "x$use_resizeinfo" = "xyes")
AM_CONDITIONAL(USE_DBUS_GLIB, test "x$use_dbus_glib" = "xyes")
AM_CONDITIONAL(USE_GLIB, test "x$use_glib" = "xyes")
AM_CONDITIONAL(USE_GCONF, test "x$use_gconf" = "xyes")
AM_CONDITIONAL(USE_DBUS, test "x$use_dbus" = "xyes")
AM_CONDITIONAL(USE_INOTIFY, test "x$use_inotify" = "xyes")
AM_CONDITIONAL(USE_FUSE, test "x$use_fuse" = "xyes")
AM_CONDITIONAL(USE_WALL, test "x$use_wall" = "xyes")
AM_CONDITIONAL(USE_ANNOTATE, test "x$use_annotate" = "xyes")
AM_CONDITIONAL(USE_JPEG, test "x$use_jpeg" = "xyes")

AC_ARG_ENABLE(librsvg,
  [  --disable-librsvg       Disable svg support],
  [use_librsvg=$enableval], [use_librsvg=yes])

if test "x$use_librsvg" = "xyes"; then
  PKG_CHECK_MODULES(LIBRSVG, [cairo >= 1.0 librsvg-2.0 >= 2.14.0], [use_librsvg=yes], [use_librsvg=no])
fi

AM_CONDITIONAL(USE_LIBRSVG, test "x$use_librsvg" = "xyes")
if test "$use_librsvg" = yes; then
  AC_DEFINE(USE_LIBRSVG, 1, [librsvg for SVG support])
fi

AC_ARG_ENABLE(gtk,
  [  --disable-gtk           Disable gtk window decorator],
  [use_gtk=$enableval], [use_gtk=yes])

AC_ARG_ENABLE(metacity,
  [  --disable-metacity      Disable metacity theme support],
  [use_metacity=$enableval], [use_metacity=yes])

AC_ARG_ENABLE(gnome,
  [  --disable-gnome         Disable gnome settings module],
  [use_gnome=$enableval], [use_gnome=yes])

AC_ARG_ENABLE(gnome-keybindings,
  [  --disable-gnome-keybindings Disable gnome keybindings],
  [use_gnome_keybindings=$enableval], [use_gnome_keybindings=yes])

# compizconfig
AC_ARG_ENABLE(protobuf,
  [  --disable-protobuf      Disable Protocol Buffers],
  [use_protobuf=$enableval], [use_protobuf=yes])

if test "x$use_protobuf" = "xyes"; then
  protobuf_error_msg="\nWARNING: You need to install Protocol Buffers to get faster program startup.\n        Sources are available at http://code.google.com/p/protobuf/downloads/list\n         Package names for Ubuntu/Debian: libprotobuf0, libprotobuf-dev, protobuf-compiler\n         Package names for other distributions: protobuf, protobuf-devel\n        Disabling protobuf.\n"
  AC_CHECK_PROG(have_protoc, protoc, yes, no)
  if test "x$have_protoc" = "xno"; then
    echo -e $protobuf_error_msg; use_protobuf=no
  else
    AC_CHECK_LIB(protobuf, _ZN6google8protobuf7MessageD2Ev, [], [
      echo -e $protobuf_error_msg; use_protobuf=no ], -lpthread)
    if test "x$use_protobuf" = "xyes"; then
      AC_LANG([C++])
      AC_CHECK_HEADER([google/protobuf/message.h],,[
        echo -e $protobuf_error_msg; use_protobuf=no ])
      AC_LANG([C])
    fi
  fi
fi
AM_CONDITIONAL([USE_PROTOBUF], [test "x$use_protobuf" = "xyes"])
AC_CHECK_HEADERS([sys/inotify.h], [have_inotify=yes], [have_inotify=no])


AC_CHECK_PROGS(PYREX, pyrexc)
if test -z "$PYREX"
then
	AC_MSG_ERROR([Couldn't find Pyrex])
fi


if test "x$use_gtk" = "xyes"; then
  PKG_CHECK_MODULES(GTK_WINDOW_DECORATOR,
		    xrender >= 0.8.4  \
		    gtk+-2.0 >= 2.8.0 \
		    libwnck-1.0	      \
		    pangocairo,
		    [use_gtk=yes], [use_gtk=no])
  if test "x$use_gtk" = "xyes"; then
    save_CFLAGS="$CFLAGS"
    save_LIBS="$LIBS"
    CFLAGS="$CFLAGS $GTK_WINDOW_DECORATOR_CFLAGS"
    LIBS="$LIBS $GTK_WINDOW_DECORATOR_LIBS"
    AC_CHECK_FUNCS(wnck_window_has_name)
    CFLAGS="$save_CFLAGS"
    LIBS="$save_LIBS -lm -ldl"

    PKG_CHECK_EXISTS(libwnck-1.0 >= 2.18.1,
		     [have_libwnck_2_18_1=yes], [have_libwnck_2_18_1=no])

	PKG_CHECK_EXISTS(libwnck-1.0 >= 2.19.4,
		     [have_libwnck_2_19_4=yes], [have_libwnck_2_19_4=no])

    if test "x$use_metacity" = "xyes"; then
      PKG_CHECK_MODULES(METACITY, libmetacity-private,
			[use_metacity=yes], [use_metacity=no])
      PKG_CHECK_EXISTS(libmetacity-private >= 2.15.21,
		       [have_metacity_2_15_21=yes], [have_metacity_2_15_21=no])
      PKG_CHECK_EXISTS(libmetacity-private >= 2.17.0,
		       [have_metacity_2_17_0=yes], [have_metacity_2_17_0=no])
      PKG_CHECK_EXISTS(libmetacity-private >= 2.23.2,
		       [have_metacity_2_23_2=yes], [have_metacity_2_23_2=no])
    fi

    if test "x$use_gnome" = "xyes"; then
      PKG_CHECK_MODULES(GNOME_WINDOW_SETTINGS,
			gnome-window-settings-2.0 gnome-desktop-2.0 gconf-2.0,
			[use_gnome=yes], [use_gnome=no])
    fi

    if test "x$use_gnome_keybindings" = "xyes"; then
      PKG_CHECK_MODULES(GNOME_KEY_BINDINGS,
			gnome-keybindings,
			[use_gnome_keybindings=yes], [use_gnome_keybindings=no])
    fi

    windowsettingsdatadir=`pkg-config --variable=prefix gnome-window-settings-2.0`/share
    windowsettingslibdir=`pkg-config --variable=libdir gnome-window-settings-2.0`    keybindingsdir=`pkg-config --variable=keysdir gnome-keybindings`
  else
    use_metacity="no"
    use_gnome="no"
  fi
else
  use_metacity="no"
  use_gnome="no"
fi

AC_SUBST(windowsettingsdatadir)
AC_SUBST(windowsettingslibdir)
AC_SUBST(keybindingsdir)

AM_CONDITIONAL(USE_GTK, test "x$use_gtk" = "xyes")
if test "$use_gtk" = yes; then
  AC_DEFINE(USE_GTK, 1, [Build gtk window decorator])
  if test "$have_libwnck_2_18_1" = yes; then
    AC_DEFINE(HAVE_LIBWNCK_2_18_1, 1,
	      [Define to 1 if libwnck version >= 2_18_1])
  fi
  if test "$have_libwnck_2_19_4" = yes; then
    AC_DEFINE(HAVE_LIBWNCK_2_19_4, 1,
	      [Define to 1 if libwnck version >= 2_19_4])
  fi
fi

AM_CONDITIONAL(USE_METACITY, test "x$use_metacity" = "xyes")
if test "$use_metacity" = yes; then
  AC_DEFINE(USE_METACITY, 1, [Build metacity theme support])
  if test "$have_metacity_2_15_21" = yes; then
    AC_DEFINE(HAVE_METACITY_2_15_21, 1,
	      [Define to 1 if metacity version >= 2.15.21])
  fi
  if test "$have_metacity_2_17_0" = yes; then
    AC_DEFINE(HAVE_METACITY_2_17_0, 1,
	      [Define to 1 if metacity version >= 2.17.0])
  fi
  if test "$have_metacity_2_23_2" = yes; then
    AC_DEFINE(HAVE_METACITY_2_23_2, 1,
	      [Define to 1 if metacity version >= 2.23.2])
  fi
fi

AM_CONDITIONAL(USE_GNOME, test "x$use_gnome" = "xyes")
if test "$use_gnome" = yes; then
  AC_DEFINE(USE_GNOME, 1, [Build gnome settings module])
fi

AM_CONDITIONAL(USE_GNOME_KEYBINDINGS, test "x$use_gnome_keybindings" = "xyes")
if test "$use_gnome_keybindings" = yes; then
  AC_DEFINE(USE_GNOME_KEYBINDINGS, 1, [Install custom keybindings])
fi

AC_ARG_ENABLE(kde,
  [  --disable-kde           Disable kde window decorator],
  [use_kde=$enableval], [use_kde=yes])

if test "x$use_kde" = "xyes"; then
  qt_incdirs="$QTINC /usr/local/qt/include /usr/include/qt /usr/include /usr/X11R6/include/X11/qt /usr/X11R6/include/qt /usr/lib/qt3/include /usr/lib/qt/include /usr/share/qt3/include"
  qt_libdirs="$QTLIB /usr/local/qt/lib /usr/lib/qt /usr/lib /usr/X11R6/lib/X11/qt /usr/X11R6/lib/qt /usr/lib/qt3/lib /usr/lib/qt/lib /usr/share/qt3/lib"

  if test -n "$QTDIR" ; then
    qt_incdirs="$QTDIR/include $qt_incdirs"
    qt_libdirs="$QTDIR/lib $qt_libdirs"
  fi

  qt_test_include="qstyle.h"
  qt_test_library="libqt-mt.so"

  dnl Check for Qt headers
  AC_MSG_CHECKING([for Qt headers])
  qt_incdir="no"
  for it in $qt_incdirs ; do
    if test -r "$it/$qt_test_include" ; then
      qt_incdir="$it"
      break
    fi
  done
  AC_MSG_RESULT([$qt_incdir])

  dnl Check for Qt libraries
  AC_MSG_CHECKING([for Qt libraries])
  qt_libdir="no"
  for qt_check in $qt_libdirs ; do
    if test -r "$qt_check/$qt_test_library" ; then
      qt_libdir="$qt_check"
      break
    fi
  done
  AC_MSG_RESULT([$qt_libdir])

  use_kde=no;
  if test "x$qt_libdir" != "xno" ; then
    if test "x$qt_incdir" != "xno" ; then
      use_kde=yes;
    fi
  fi

  QT_CXXFLAGS="-I$qt_incdir"
  QT_LIBS="-L$qt_libdir"

  if test "x$use_kde" = xyes; then
    kdedir=`kde-config --prefix --expandvars 2>/dev/null`
    kdelibs=`kde-config --install lib --expandvars 2>/dev/null`
    kdeincs=`kde-config --install include --expandvars 2>/dev/null`
    if test -d "$kdelibs"; then
      PKG_CHECK_MODULES(KDE_WINDOW_DECORATOR,
			dbus-1 xdamage xcomposite,
			[use_kde=yes], [use_kde=no])

      KDE_CFLAGS="$QT_CXXFLAGS -I$kdeincs"
      KDE_LIBS="$QT_LIBS -L$kdelibs -lkdecore -lkdecorations -ldbus-qt-1"

      QT_MOC=$QTDIR/bin/moc
      DCOPIDL=$kdedir/bin/dcopidl
      DCOPIDL2CPP=$kdedir/bin/dcopidl2cpp
    else
      use_kde=no;
    fi
  fi
fi

AM_CONDITIONAL(USE_KDE, test "x$use_kde" = "xyes")
if test "$use_kde" = yes; then
  AC_DEFINE(USE_KDE, 1, [Build kde window decorator])
fi

AC_SUBST(KDE_CFLAGS)
AC_SUBST(KDE_LIBS)
AC_SUBST(QT_MOC)
AC_SUBST(DCOPIDL)
AC_SUBST(DCOPIDL2CPP)

AC_ARG_ENABLE(kde4,
  [  --disable-kde4          Disable kde4 window decorator],
  [use_kde4=$enableval], [use_kde4=yes])

if test "x$use_kde4" = "xyes"; then
  
  kde4dir=`kde4-config --prefix --expandvars 2>/dev/null`
  kde4libs=/usr/lib64/kde4/devel #`kde4-config --install lib --expandvars 2>/dev/null`
  kde4incs=`kde4-config --install include --expandvars 2>/dev/null`

  kde4_test_includes="kdecoration.h kcommondecoration.h kdecorationbridge.h plasma/framesvg.h"

  dnl Check for KWin headers
  AC_MSG_CHECKING([for KWin headers])

  kde4_notfound=""
  for file in $kde4_test_includes ; do
    status=" $file"
    for it in $kde4incs ; do
      if test -r "$it/$file" ; then
        status=""
        break;
      fi
    done
    kde4_notfound="$kde4_notfound$status"
  done
  if test -z "$kde4_notfound" ; then
      kde4_notfound="yes"
  else
      kde4_notfound="$kde4_notfound not found"
      kde4libs=""
  fi

  AC_MSG_RESULT([$kde4_notfound])

  if test -d "$kde4libs"; then
    PKG_CHECK_MODULES(KDE4_WINDOW_DECORATOR,
		      dbus-1 xdamage xext xcomposite QtCore >= 4.5.0 QtGui QtDBus,
			[use_kde4=yes], [use_kde4=no])

    KDE4_CFLAGS="-I$kde4incs"
    KDE4_LIBS="-L$kde4libs -lkdecore -lkdecorations -lkdeui -lplasma"

    QT4_MOC=`pkg-config QtGui --variable=moc_location`
    QDBUSXML2CPP=`pkg-config QtGui --variable=exec_prefix`"/bin/qdbusxml2cpp"
  else
    use_kde4=no;
  fi
fi

AM_CONDITIONAL(USE_KDE4, test "x$use_kde4" = "xyes")
if test "$use_kde4" = yes; then
  AC_DEFINE(USE_KDE4, 1, [Build kde4 window decorator])
fi

AC_SUBST(KDE4_CFLAGS)
AC_SUBST(KDE4_LIBS)
AC_SUBST(QT4_MOC)
AC_SUBST(QDBUSXML2CPP)

AC_ARG_ENABLE(kconfig,
  [  --disable-kconfig       Disable kconfig plugin],
  [use_kconfig=$enableval], [use_kconfig=yes])

if test "x$use_kde" != "xyes"; then
  use_kconfig=no;
fi

if test "x$use_kconfig" = "xyes"; then
  KCONFIG_CFLAGS=$KDE_CFLAGS
  KCONFIG_LIBS=$KDE_LIBS
  KDE_KCFG_DIR=`kde-config --install kcfg --expandvars 2>/dev/null`
  KDE_KCONFIG_DIR=`kde-config --install config --expandvars 2>/dev/null`
fi

AM_CONDITIONAL(USE_KCONFIG, test "x$use_kconfig" = "xyes")
if test "$use_kconfig" = yes; then
  AC_DEFINE(USE_KCONFIG, 1, [Build kconfig plugin])
fi

AC_SUBST(KCONFIG_CFLAGS)
AC_SUBST(KCONFIG_LIBS)
AC_SUBST(KDE_KCFG_DIR)
AC_SUBST(KDE_KCONFIG_DIR)

kcfgdir=$KDE_KCFG_DIR
AC_SUBST(kcfgdir)

AC_ARG_WITH(max-desktops,
  [  --with-max-desktops     Max reasonable desktops],
  [MAX_DESKTOPS=$withval],
  [MAX_DESKTOPS=36])

if test -n "$MAX_DESKTOPS"; then
  AC_DEFINE_UNQUOTED(MAX_DESKTOPS, $MAX_DESKTOPS, [Max reasonable desktops])
fi

AC_CONFIG_COMMANDS([include/compiz-common.h],
[
	commonfile=include/compiz-common.h
	outfile=$commonfile.tmp
	AC_MSG_NOTICE([creating $commonfile])
	cat > $outfile <<_EOF
#ifndef COMPIZ_COMMON_H
#define COMPIZ_COMMON_H

#ifdef  __cplusplus
# define COMPIZ_BEGIN_DECLS  extern "C" {
# define COMPIZ_END_DECLS    }
#else
# define COMPIZ_BEGIN_DECLS
# define COMPIZ_END_DECLS
#endif


_EOF
	echo '#endif' >> $outfile

	if cmp -s $outfile $commonfile; then
	  AC_MSG_NOTICE([$commonfile is unchanged])
	  rm -f $outfile
	else
	  mv $outfile $commonfile
	fi
],[
	COMPIZ_VERSION_MAJOR=$COMPIZ_VERSION_MAJOR
	COMPIZ_VERSION_MINOR=$COMPIZ_VERSION_MINOR
	COMPIZ_VERSION_MICRO=$COMPIZ_VERSION_MICRO
])

AC_OUTPUT([
pc/compiz.pc
pc/compiz-cube.pc
pc/compiz-scale.pc
pc/compiz-gconf.pc
pc/compiz-kconfig.pc
pc/compiz-mousepoll.pc
pc/bcop.pc
Makefile
src/Makefile
libdecoration/Makefile
libdecoration/libdecoration.pc
include/Makefile
plugins/Makefile
plugins/animation/Makefile
bcop/Makefile
bcop/bcop
images/Makefile
gtk/Makefile
gtk/window-decorator/Makefile
gtk/gnome/Makefile
kde/Makefile
kde/window-decorator/Makefile
kde/window-decorator-kde4/Makefile
po/Makefile.in
metadata/Makefile
compizconfig/libcompizconfig/libcompizconfig.pc
compizconfig/libcompizconfig/Makefile
compizconfig/libcompizconfig/src/Makefile
compizconfig/libcompizconfig/backend/Makefile
compizconfig/libcompizconfig/plugin/Makefile
compizconfig/libcompizconfig/include/Makefile
compizconfig/libcompizconfig/metadata/Makefile
compizconfig/libcompizconfig/config/Makefile
compizconfig/compizconfig-python/Makefile
compizconfig/compizconfig-python/src/Makefile
])

echo ""
echo "the following optional plugins will be compiled:"
echo "  glib:        $use_glib"
echo "  gconf:       $use_gconf"
echo "  kconfig:     $use_kconfig"
echo "  dbus:        $use_dbus"
echo "  annotate:    $use_annotate"
echo "  wall:        $use_wall"
echo "  svg:         $use_librsvg"
echo "  inotify:     $use_inotify"
echo "  fuse:        $use_fuse"
echo "  jpeg:        $use_jpeg"
echo "  text:        $use_text"
echo "  resizeinfo:  $use_resizeinfo"
echo ""
echo "and the following optional features will be compiled:"
echo "  gtk:      $use_gtk"
echo "  metacity: $use_metacity"
echo "  gnome:    $use_gnome"
echo "  kde:      $use_kde"
echo "  kde4:     $use_kde4"
echo ""
echo "Known missing optional dependencies: $missing_optional_deps"
