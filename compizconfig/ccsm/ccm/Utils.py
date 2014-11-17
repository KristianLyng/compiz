#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# Authors: Quinn Storm (quinn@beryl-project.org)
#          Patrick Niklaus (marex@opencompositing.org)
#          Guillaume Seguin (guillaume@segu.in)
#          Christopher Williams (christopherw@verizon.net)
# Copyright (C) 2007 Quinn Storm

import os

import pygtk
import gtk
import gtk.gdk
import gobject
import pango
import weakref

from ccm.Constants import *
from cgi import escape as protect_pango_markup
import operator
import itertools

import locale
import gettext
locale.setlocale(locale.LC_ALL, "")
gettext.bindtextdomain("ccsm", DataDir + "/locale")
gettext.textdomain("ccsm")
_ = gettext.gettext

IconTheme = gtk.icon_theme_get_default()
if not IconDir in IconTheme.get_search_path():
    IconTheme.prepend_search_path(IconDir)

def gtk_process_events ():
    while gtk.events_pending ():
        gtk.main_iteration ()

def getScreens():
    screens = []
    display = gtk.gdk.display_get_default()
    nScreens = display.get_n_screens()
    for i in range(nScreens):
        screens.append(i)
    return screens

def protect_markup_dict (dict_):
    return dict((k, protect_pango_markup (v)) for (k, v) in dict_.iteritems())

class Image (gtk.Image):

    def __init__ (self, name = None, type = ImageNone, size = 32,
                  useMissingImage = False):
        gtk.Image.__init__ (self)

        if not name:
            return

        if useMissingImage:
            self.set_from_stock (gtk.STOCK_MISSING_IMAGE,
                                 gtk.ICON_SIZE_LARGE_TOOLBAR)
            return

        try:
            if type in  (ImagePlugin, ImageCategory, ImageThemed):
                pixbuf = None
                
                if type == ImagePlugin:
                    name = "plugin-" + name
                    try:
                        pixbuf = IconTheme.load_icon (name, size, 0)
                    except gobject.GError:
                        pixbuf = IconTheme.load_icon ("plugin-unknown", size, 0)
                
                elif type == ImageCategory:
                    name = "plugins-" + name
                    try:
                        pixbuf = IconTheme.load_icon (name, size, 0)
                    except gobject.GError:
                        pixbuf = IconTheme.load_icon ("plugins-unknown", size, 0)
                
                else:
                    pixbuf = IconTheme.load_icon (name, size, 0)

                self.set_from_pixbuf (pixbuf)
            
            elif type == ImageStock:
                self.set_from_stock (name, size)
        except gobject.GError, e:
            self.set_from_stock (gtk.STOCK_MISSING_IMAGE, gtk.ICON_SIZE_BUTTON)

class ActionImage (gtk.Alignment):

    map = {
            "keyboard"  : "input-keyboard",
            "button"    : "input-mouse",
            "edges"     : "video-display",
            "bell"      : "audio-x-generic"
          }

    def __init__ (self, action):
        gtk.Alignment.__init__ (self, 0, 0.5)
        self.set_padding (0, 0, 0, 10)
        if action in self.map: action = self.map[action]
        self.add (Image (name = action, type = ImageThemed, size = 22))

class SizedButton (gtk.Button):

    minWidth = -1
    minHeight = -1

    def __init__ (self, minWidth = -1, minHeight = -1):
        super (SizedButton, self).__init__ ()
        self.minWidth = minWidth
        self.minHeight = minHeight
        self.connect ("size-request", self.adjust_size)

    def adjust_size (self, widget, requisition):
        width, height = requisition.width, requisition.height
        newWidth = max (width, self.minWidth)
        newHeight = max (height, self.minHeight)
        self.set_size_request (newWidth, newHeight)

class PrettyButton (gtk.Button):

    __gsignals__ = {
        'expose-event'      : 'override',
    }

    _old_toplevel = None

    def __init__ (self):
        super (PrettyButton, self).__init__ ()
        self.states = {
                        "focus"   : False,
                        "pointer" : False
                      }
        self.set_size_request (200, -1)
        self.set_relief (gtk.RELIEF_NONE)
        self.connect ("focus-in-event", self.update_state_in, "focus")
        self.connect ("focus-out-event", self.update_state_out, "focus")
        self.connect ("hierarchy-changed", self.hierarchy_changed)

    def hierarchy_changed (self, widget, old_toplevel):
        if old_toplevel == self._old_toplevel:
            return

        if not old_toplevel and self.state != gtk.STATE_NORMAL:
            self.set_state(gtk.STATE_PRELIGHT)
            self.set_state(gtk.STATE_NORMAL)

        self._old_toplevel = old_toplevel


    def update_state_in (self, *args):
        state = args[-1]
        self.set_state (gtk.STATE_PRELIGHT)
        self.states[state] = True

    def update_state_out (self, *args):
        state = args[-1]
        self.states[state] = False
        if True in self.states.values ():
            self.set_state (gtk.STATE_PRELIGHT)
        else:
            self.set_state (gtk.STATE_NORMAL)

    def do_expose_event (self, event):
        has_focus = self.flags () & gtk.HAS_FOCUS
        if has_focus:
            self.unset_flags (gtk.HAS_FOCUS)

        ret = gtk.Button.do_expose_event (self, event)

        if has_focus:
            self.set_flags (gtk.HAS_FOCUS)

        return ret

class Label(gtk.Label):
    def __init__(self, value = "", wrap = 160):
        gtk.Label.__init__(self, value)
        self.props.xalign = 0
        self.props.wrap_mode = pango.WRAP_WORD
        self.set_line_wrap(True)
        self.set_size_request(wrap, -1)

class NotFoundBox(gtk.Alignment):
    def __init__(self, value=""):
        gtk.Alignment.__init__(self, 0.5, 0.5, 0.0, 0.0)
        
        box = gtk.HBox()
        self.Warning = gtk.Label()
        self.Markup = _("<span size=\"large\"><b>No matches found.</b> </span><span>\n\n Your filter \"<b>%s</b>\" does not match any items.</span>")
        value = protect_pango_markup(value)
        self.Warning.set_markup(self.Markup % value)
        image = Image("face-surprise", ImageThemed, 48)
            
        box.pack_start(image, False, False, 0)
        box.pack_start(self.Warning, True, True, 15)
        self.add(box)

    def update(self, value):
        value = protect_pango_markup(value)
        self.Warning.set_markup(self.Markup % value)

class IdleSettingsParser:
    def __init__(self, context, main):
        def FilterPlugin (p):
            return not p.Initialized and p.Enabled

        self.Context = context
        self.Main = main
        self.PluginList = [p for p in self.Context.Plugins.items() if FilterPlugin(p[1])]
        nCategories = len (main.MainPage.RightWidget._boxes)
        self.CategoryLoadIconsList = range (3, nCategories) # Skip the first 3
        print 'Loading icons...'

        gobject.timeout_add (150, self.Wait)

    def Wait(self):
        if not self.PluginList:
            return False
        
        if len (self.CategoryLoadIconsList) == 0: # If we're done loading icons
            gobject.idle_add (self.ParseSettings)
        else:
            gobject.idle_add (self.LoadCategoryIcons)
        
        return False
    
    def ParseSettings(self):
        name, plugin = self.PluginList[0]

        if not plugin.Initialized:
            plugin.Update ()
            self.Main.RefreshPage(plugin)

        self.PluginList.remove (self.PluginList[0])

        gobject.timeout_add (200, self.Wait)

        return False

    def LoadCategoryIcons(self):
        from ccm.Widgets import PluginButton

        catIndex = self.CategoryLoadIconsList[0]
        pluginWindow = self.Main.MainPage.RightWidget
        categoryBox = pluginWindow._boxes[catIndex]
        for (pluginIndex, plugin) in \
            enumerate (categoryBox.get_unfiltered_plugins()):
            categoryBox._buttons[pluginIndex] = PluginButton (plugin)
        categoryBox.rebuild_table (categoryBox._current_cols, True)
        pluginWindow.connect_buttons (categoryBox)

        self.CategoryLoadIconsList.remove (self.CategoryLoadIconsList[0])

        gobject.timeout_add (150, self.Wait)

        return False

# Updates all registered setting when they where changed through CompizConfig
class Updater:

    def __init__ (self):
        self.VisibleSettings = {}
        self.Plugins = []
        self.Block = 0

    def SetContext (self, context):
        self.Context = context

        gobject.timeout_add (2000, self.Update)

    def Append (self, widget):
        reference = weakref.ref(widget)
        setting = widget.Setting
        self.VisibleSettings.setdefault((setting.Plugin.Name, setting.Name), []).append(reference)

    def AppendPlugin (self, plugin):
        self.Plugins.append (plugin)

    def Remove (self, widget):
        setting = widget.Setting
        l = self.VisibleSettings.get((setting.Plugin.Name, setting.Name))
        if not l:
            return
        for i, ref in enumerate(list(l)):
            if ref() is widget:
                l.remove(ref)
                break

    def UpdatePlugins(self):
        for plugin in self.Plugins:
            plugin.Read()

    def UpdateSetting (self, setting):
        widgets = self.VisibleSettings.get((setting.Plugin.Name, setting.Name))
        if not widgets:
            return
        for reference in widgets:
            widget = reference()
            if widget is not None:
                widget.Read()

    def Update (self):
        if self.Block > 0:
            return True

        if self.Context.ProcessEvents():
            changed = self.Context.ChangedSettings
            if [s for s in changed if s.Plugin.Name == "core" and s.Name == "active_plugins"]:
                self.UpdatePlugins()

            for setting in list(changed):
                widgets = self.VisibleSettings.get((setting.Plugin.Name, setting.Name))
                if widgets: 
                    for reference in widgets:
                        widget = reference()
                        if widget is not None:
                            widget.Read()
                            if widget.List:
                                widget.ListWidget.Read()
                changed.remove(setting)

            self.Context.ChangedSettings = changed

        return True

GlobalUpdater = Updater ()

class PluginSetting:

    def __init__ (self, plugin, widget, handler):
        self.Widget = widget
        self.Plugin = plugin
        self.Handler = handler
        GlobalUpdater.AppendPlugin (self)

    def Read (self):
        widget = self.Widget
        widget.handler_block(self.Handler)
        widget.set_active (self.Plugin.Enabled)
        widget.set_sensitive (self.Plugin.Context.AutoSort)
        widget.handler_unblock(self.Handler)

class PureVirtualError(Exception):
    pass

def SettingKeyFunc(value):
    return value.Plugin.Ranking[value.Name]

def CategoryKeyFunc(category):
    if 'General' == category:
        return ''
    else:
        return category or 'zzzzzzzz'

def GroupIndexKeyFunc(item):
    return item[1][0]

FirstItemKeyFunc = operator.itemgetter(0)

EnumSettingKeyFunc = operator.itemgetter(1)

PluginKeyFunc = operator.attrgetter('ShortDesc')

def HasOnlyType (settings, stype):
    return settings and not [s for s in settings if s.Type != stype]

def GetSettings(group, displayOnly=False, types=None):

    def TypeFilter (settings, types):
         for setting in settings:
            if setting.Type in types:
                yield setting

    if types:
        display = TypeFilter(group.Display.itervalues(), types)
    else:
        display = group.Display.itervalues()

    if displayOnly:
        return display

    if types:
        screen = TypeFilter(group.Screens[CurrentScreenNum].itervalues(), types)
    else:
        screen = group.Screens[CurrentScreenNum].itervalues()

    return itertools.chain(screen, display)

# Support python 2.4
try:
    any
    all
except NameError:
    def any(iterable):
        for element in iterable:
            if element:
                return True
        return False

    def all(iterable):
        for element in iterable:
            if not element:
                return False
        return True

