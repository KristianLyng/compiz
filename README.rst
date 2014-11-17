======
compiz
======

------
Compiz
------

:Manual section: 1
:Author: Kristian Lyngstol
:Date: 17-11-2014
:Version: 0.8.11

SYNOPSIS
========

::

	compiz [--display DISPLAY] [--bg-image PNG] [--refresh-rate RATE]
               [--fast-filter] [--indirect-rendering] [--no-detection]
               [--keep-desktop-hints] [--loose-binding] [--replace]
               [--sm-disable] [--sm-client-id ID] [--only-current-screen]
               [--use-root-window] [--debug] [--version] [--help] [PLUGIN]...

DESCRIPTION
===========

Compiz is a plugin-based compositing window manager for the X desktop.

This particular repository is a work in progress to merge various
Compiz-components and make things easier for users and developers alike.

OPTIONS
=======

--display DISPLAY
	The X display to run at. E.g. ``--display :0.0``


HISTORY
=======

Compiz has a somewhat turbulent history that involves forking into Compiz
and Beryl, then merging to Compiz Fusion and Compiz, then being
re-implemented in C++, and now this.

This version is based on the code base as it existed right before it was
re-implemented in C++. For the user, there are few actual differences
between the 0.8-code base (C), and the later 0.9 code base (C++). The main
difference is that one supports Unity (0.9) and the other does not.

ABOUT 0.8.11
============

This 0.8.11-based code-base is undergoing some significant changes. Changes
between the 0.8.9-code(which is almost identical to the released 0.8.8) and
0.8.11:

- bcop now included directly and built/distributed. Plugins don't need the
  bcop-binary, just the xslt. See staticswitcher in plugins/Makefile.am.
- plugins-main imported to contrib/ and some plugins moved from
  contrib/plugins-main to plugins/ (ezoom, mousepoll, staticswitcher). The rest 
  does NOT build automatically. All the plugins will be ported one at a
  time.
- At the moment I am asking people to file bug reports to
  https://github.com/KristianLyng/compiz . I will also accept pull requests
  if they make sense.
- Silent building
- autogen.sh does NOT run configure now. Run it by hand. (Tip:
  ./autogen.sh; mkdir build; cd build; ../configure; make ... Now you have
  out-of-tree building).
- We will probably need to address versioning sooner or later.

TODO
====

See https://github.com/KristianLyng/compiz and 'enhancements'.

SEE ALSO
========

* gtk-window-decorator(1)
* ccsm(1)

COPYRIGHT
=========

This document is licensed under the MIT license, same as most of Compiz. See
LICENSE for details.

* Copyright 2014 Kristian Lyngstol <kristian@bohemians.org>
