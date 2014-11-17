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

--bg-image PNG
        Default background image if none is set.

--refresh-rate RATE
        Set the screen refresh rate to RATE. Useful if you are using
        multiple monitors with different refresh rates.

--fast-filter
        Force using a fast filter. This will give a visually jagged, but
        smooth experience. Does not significantly impact performance in most
        cases.

--indirect-rendering
        Force indirect rendering, even when direct rendering is seemingly
        possible.

--no-detection
        Do not attempt to detect screen sizes and refresh rates. Will most
        likely result in a semi-broken desktop until you can configure it
        manually.

--keep-desktop-hints
        Use desktop hints to determine amount of desktops and which one is
        the current one at startup.

--lose-bindings
        Don't use strict binding for textures.

--replace
        If an other window manager is running, try to replace it. This also
        works if compiz is already running and you wish to restart.

--sm-disable
        Disable session management.

--sm-client-id ID
        Session ID.

--only-current-screen
        Only start compiz on the current X Screen. Most setups today only
        use a single X screen, even for multiple monitors. Multiple X
        screens are mostly obsoleted and has the major drawback of not
        allowing you to move windows between one screen and an other.

--use-root-window
        Don't use the compositing overlay window (cow) for the root window.

--debug
        Enable certain debug-features (like forcing sync).

--version
        Print the compiz version.

--help
        Print basic usage.

[PLUGIN]
        One or more plugin to load. You most likely want to load a
        configuration plugin, then do the rest of the configuration through
        that. Example: ``gconf``, ``ccp``, ``ini``. Without some plugins,
        compiz will just sit there and you will not be able to do anything
        like move windows or change viewports. See compiz-plugins(7) for an
        overview.

CONFIGURATION
=============

Compiz has two types of configuration. The command line arguments (see
OPTIONS above) and metadata. Most configuration is done through metadata.

Because Compiz is also plugin-driven, there is no single standard way of
configuring it. There is a number of configuration-plugins, each adapted to
either a storage backend or library (e.g. ``gconf`` and ``ini``).

The recommended plugin is ``ccp``, and configuration can then be done using
the Compiz Config Settings Manager (``ccsm``).

EXAMPLES
========

::

    compiz --replace ccp

Starts compiz with the CompizConfig plugin. Configuration can then be done
through ``ccsm``.

::

    compiz --replace move mousepoll png cube rotate ezoom staticswitcher 
           resize decoration &
    gtk-window-decorator &

Starts compiz with a set of plugins and a GTK window decorator. This will
give you a functional desktop, but no way of changing the configuration of
the plugins from the default values.

NOTES
=====

Configuration schemas are typically stored in ``/usr/share/compiz/foo.xml``
(or the ``/usr/local`` equivalent). These schemas are NOT used by compiz
itself. Changing default values here will not change the default values of
Compiz.

These files may be used by the various configuration plugins. If you are
using a configuration plugin that utilizes them, then changing the default
values in the XML files MIGHT change the actual defaults, but it is not
guaranteed. Bottom line: Do not change the XML in attempt to change
configuration defaults.

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
- plugins-main imported to contrib/ and most plugins moved from
  contrib/plugins-main to plugins/ . Missing colorfilter and animation for
  now.
- Significant work on the build system to reduce cruft
- Silent building
- autogen.sh does NOT run configure now. Run it by hand. (Tip:
  ./autogen.sh; mkdir build; cd build; ../configure; make ... Now you have
  out-of-tree building).
- README.rst which actually has useful information, and is shipped as a
  manual page.
- We will probably need to address versioning sooner or later.

Compizconfig will also be imported, but that has not been done just yet.

BUGS
====

There are a number of well-known issues with Compiz. Please file bugs at
https://github.com/KristianLyng/compiz for now. This page also lists
TODO-items.

SEE ALSO
========

* gtk-window-decorator(1)
* ccsm(1)
* compiz-plugins(7)

COPYRIGHT
=========

This document is licensed under the MIT license, same as most of Compiz. See
LICENSE for details.

* Copyright 2014 Kristian Lyngstol <kristian@bohemians.org>
