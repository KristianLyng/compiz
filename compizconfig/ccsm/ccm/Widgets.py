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

import pygtk
import gtk
import gtk.gdk
import gobject
import cairo, pangocairo
from math import pi, sqrt
import time
import re
import mimetypes
mimetypes.init()

from ccm.Utils import *
from ccm.Constants import *
from ccm.Conflicts import *

import locale
import gettext
locale.setlocale(locale.LC_ALL, "")
gettext.bindtextdomain("ccsm", DataDir + "/locale")
gettext.textdomain("ccsm")
_ = gettext.gettext

#
# Try to use gtk like coding style for consistency
#

# Cell Renderer for MultiList

class CellRendererColor(gtk.GenericCellRenderer):
    __gproperties__ = {
        'text': (gobject.TYPE_STRING,
                'color markup text',
                'The color as markup like this: #rrrrggggbbbbaaaa',
                '#0000000000000000',
                gobject.PARAM_READWRITE)
    }

    _text  = '#0000000000000000'
    _color = [0, 0, 0, 0]
    _surface = None
    _surface_size = (-1, -1)

    def __init__(self):
        gtk.GenericCellRenderer.__init__(self)

    def _parse_color(self):
        color = gtk.gdk.color_parse(self._text[:-4])
        alpha = int("0x%s" % self._text[-4:], base=16)
        self._color = [color.red/65535.0, color.green/65535.0, color.blue/65535.0, alpha/65535.0]

    def do_set_property(self, property, value):
        if property.name == 'text':
            self._text = value
            self._parse_color()

    def do_get_property(self, property):
        if property.name == 'text':
            return self._text

    def on_get_size(self, widget, cell_area):
        return (0, 0, 0, 0) # FIXME

    def redraw(self, width, height):
        # found in gtk-color-button.c
        CHECK_SIZE  = 4
        CHECK_DARK  = 21845 # 65535 / 3
        CHECK_LIGHT = 43690

        width += 10
        height += 10
        self._surface_size = (width, height)
        self._surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        cr = cairo.Context(self._surface)

        x = 0
        y = 0
        colors = [CHECK_DARK, CHECK_LIGHT]
        state = 0
        begin_state = 0
        while y < height:
            while x < width:
                cr.rectangle(x, y, CHECK_SIZE, CHECK_SIZE)
                c = colors[state] / 65535.0
                cr.set_source_rgb(c, c, c)
                cr.fill()
                x += CHECK_SIZE
                state = not state
            state = not begin_state
            begin_state = state
            x = 0
            y += CHECK_SIZE

    def on_render(self, window, widget, background_area, cell_area, expose_area, flags):
        cr = window.cairo_create()

        height, width = (cell_area.height, cell_area.width)
        sheight, swidth = self._surface_size
        if height > sheight or width > swidth:
            self.redraw(width, height)

        cr.rectangle(cell_area.x, cell_area.y, width, height)
        cr.clip()

        cr.set_source_surface(self._surface, cell_area.x, cell_area.y)
        cr.paint()

        r, g, b, a = self._color
        cr.set_source_rgba(r, g, b, a)
        cr.paint()

class PluginView(gtk.TreeView):
    def __init__(self, plugins):
        liststore = gtk.ListStore(str, gtk.gdk.Pixbuf, bool, object)
        self.model = liststore.filter_new()
        gtk.TreeView.__init__(self, self.model)

        self.SelectionHandler = None

        self.Plugins = set(plugins)

        for plugin in sorted(plugins.values(), key=PluginKeyFunc):
            liststore.append([plugin.ShortDesc, Image(plugin.Name, type=ImagePlugin).props.pixbuf, 
                plugin.Enabled, plugin])
        
        column = self.insert_column_with_attributes(0, _('Plugin'), gtk.CellRendererPixbuf(), pixbuf=1, sensitive=2)
        cell = gtk.CellRendererText()
        cell.props.wrap_width = 200
        column.pack_start(cell)
        column.set_attributes(cell, text=0)
        self.model.set_visible_func(self.VisibleFunc)
        self.get_selection().connect('changed', self.SelectionChanged)

    def VisibleFunc(self, model, iter):
        return model[iter][3].Name in self.Plugins

    def Filter(self, plugins):
        self.Plugins = set(plugins)
        self.model.refilter()

    def SelectionChanged(self, selection):
        model, iter = selection.get_selected()
        if iter is None:
            return self.SelectionHandler(None)
        
        return self.SelectionHandler(model[iter][3])

class GroupView(gtk.TreeView):
    def __init__(self, name):
        self.model = gtk.ListStore(str, str)
        gtk.TreeView.__init__(self, self.model)

        self.SelectionHandler = None

        self.Visible = set()
        
        cell = gtk.CellRendererText()
        cell.props.ypad = 5
        cell.props.wrap_width = 200
        column = gtk.TreeViewColumn(name, cell, text=0)
        self.append_column(column)

        self.get_selection().connect('changed', self.SelectionChanged)
        self.hide_all()
        self.props.no_show_all = True

    def Update(self, items):
        self.model.clear()

        self.model.append([_('All'), 'All'])

        length = 0
        for item in items:
            self.model.append([item or _("General"), item])
            if item: # exclude "General" from count
                length += 1

        if length:
            self.show_all()
            self.props.no_show_all = False
        else:
            self.hide_all()
            self.props.no_show_all = True

    def SelectionChanged(self, selection):
        model, iter = selection.get_selected()
        if iter is None:
            return None
        
        return self.SelectionHandler(model[iter][1])

# Selector Buttons
#
class SelectorButtons(gtk.HBox):
    def __init__(self):
        gtk.HBox.__init__(self)
        self.set_border_width(10)
        self.set_spacing(5)
        self.buttons = []
        self.arrows = []

    def clear_buttons(self):
        for widget in (self.arrows + self.buttons):
            widget.destroy()

        self.arrows = []
        self.buttons = []

    def add_button(self, label, callback):
        arrow = gtk.Arrow(gtk.ARROW_RIGHT, gtk.SHADOW_NONE)
        button = gtk.Button(label)
        button.set_relief(gtk.RELIEF_NONE)
        button.connect('clicked', self.on_button_clicked, callback)
        if self.get_children():
            self.pack_start(arrow, False, False)
            self.arrows.append(arrow)
        self.pack_start(button, False, False)
        self.buttons.append(button)
        self.show_all()

    def remove_button(self, pos):
        if pos > len(self.buttons)-1:
            return
        self.buttons[pos].destroy()
        self.buttons.remove(self.buttons[pos])
        if pos > 0:
            self.arrows[pos-1].destroy()
            self.arrows.remove(self.arrows[pos-1])

    def on_button_clicked(self, widget, callback):
        callback(selector=True)

# Selector Box
#
class SelectorBox(gtk.ScrolledWindow):
    def __init__(self, backgroundColor):
        gtk.ScrolledWindow.__init__(self)
        self.viewport = gtk.Viewport()
        self.viewport.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(backgroundColor))
        self.props.hscrollbar_policy = gtk.POLICY_NEVER
        self.props.vscrollbar_policy = gtk.POLICY_AUTOMATIC
        self.box = gtk.VBox()
        self.box.set_spacing(5)
        self.viewport.add(self.box)
        self.add(self.viewport)

    def close(self):
        self.destroy()
        self.viewport.destroy()
        for button in self.box.get_children():
            button.destroy()
        self.box.destroy()

    def add_item(self, item, callback, markup="%s", image=None, info=None):
        button = gtk.Button()
        label = Label(wrap=170)
        text = protect_pango_markup(item)
        label.set_markup(markup % text or _("General"))
        labelBox = gtk.VBox()
        labelBox.set_spacing(5)
        labelBox.pack_start(label)
        if info:
            infoLabel = Label()
            infoLabel.set_markup("<span size='small'>%s</span>" % info)
            labelBox.pack_start(infoLabel)
        box = gtk.HBox()
        box.set_spacing(5)
        if image:
            box.pack_start(image, False, False)
        box.pack_start(labelBox)
        button.add(box)
        button.connect("clicked", callback, item)
        button.set_relief(gtk.RELIEF_NONE)
        self.box.pack_start(button, False, False)

    def clear_list(self):
        for button in self.box.get_children():
            button.destroy()
    
    def set_item_list(self, list, callback):
        self.clear_list()
        for item in list:
            self.add_item(item)
            
        self.box.show_all()

# Scrolled List
#
class ScrolledList(gtk.ScrolledWindow):
    def __init__(self, name):
        gtk.ScrolledWindow.__init__(self)

        self.props.hscrollbar_policy = gtk.POLICY_NEVER
        self.props.vscrollbar_policy = gtk.POLICY_AUTOMATIC

        self.store = gtk.ListStore(gobject.TYPE_STRING)
    
        self.view = gtk.TreeView(self.store)
        self.view.set_headers_visible(True)
        self.view.insert_column_with_attributes(-1, name, gtk.CellRendererText(), text=0)
        
        self.set_size_request(300, 300)
        
        self.add(self.view)
        
        self.select = self.view.get_selection()
        self.select.set_mode(gtk.SELECTION_SINGLE)

    def get_list(self):
        values = []
        iter = self.store.get_iter_first()
        while iter:
            value = self.store.get(iter, 0)[0]
            if value != "":
                values.append(value)
            iter = self.store.iter_next(iter)    
        return values

    def clear(self):
        self.store.clear()
    
    def append(self, value):
        iter = self.store.append()
        self.store.set(iter, 0, value)

    def set(self, pos, value):
        iter = self.store.get_iter(pos)
        self.store.set(iter, 0, value)

    def delete(self, b):
        selected_rows = self.select.get_selected_rows()[1]
        for path in selected_rows:
            iter = self.store.get_iter(path)
            self.store.remove(iter)
    
    def move_up(self, b):
        selected_rows = self.select.get_selected_rows()[1]
        if len(selected_rows) == 1:
            iter = self.store.get_iter(selected_rows[0])
            prev = self.store.get_iter_first()
            if not self.store.get_path(prev) == self.store.get_path(iter):
                while prev is not None and not self.store.get_path(self.store.iter_next(prev)) == self.store.get_path(iter):
                    prev = self.store.iter_next(prev)
                self.store.swap(iter, prev)

    def move_down(self, b):
        selected_rows = self.select.get_selected_rows()[1]
        if len(selected_rows) == 1:
            iter = self.store.get_iter(selected_rows[0])
            next = self.store.iter_next(iter)
            if next is not None:
                self.store.swap(iter, next)

# Button modifier selection widget
#
class ModifierSelector (gtk.DrawingArea):

    __gsignals__    = {"added" : (gobject.SIGNAL_RUN_FIRST,
                                    gobject.TYPE_NONE, [gobject.TYPE_STRING]),
                       "removed" : (gobject.SIGNAL_RUN_FIRST,
                                    gobject.TYPE_NONE, [gobject.TYPE_STRING])}

    _current = []

    _base_surface   = None
    _surface        = None

    _x0     = 0
    _y0     = 12
    _width  = 100
    _height = 50

    _font   = "Sans 12 Bold"

    def __init__ (self, mods):
        '''Prepare widget'''
        super (ModifierSelector, self).__init__ ()
        self._current = mods.split ("|")
        modifier = "%s/modifier.png" % PixmapDir
        self._base_surface = cairo.ImageSurface.create_from_png (modifier)
        self.add_events (gtk.gdk.BUTTON_PRESS_MASK)
        self.connect ("expose_event", self.expose)
        self.connect ("button_press_event", self.button_press)
        self.set_size_request (200, 120)

        x0, y0, width, height = self._x0, self._y0, self._width, self._height
        self._modifiers = {
            "Shift"     : (x0, y0),
            "Control"   : (x0, y0 + height),
            "Super"     : (x0 + width, y0),
            "Alt"       : (x0 + width, y0 + height)
        }

        self._names = {
            "Control"   : "Ctrl"
        }

    def set_current (self, value):
        self._current = value.split ("|")
        self.redraw (queue = True)

    def get_current (self):
        return "|".join (filter (lambda s: len (s) > 0, self._current))
    current = property (get_current, set_current)

    def draw (self, cr, width, height):
        '''The actual drawing function'''
        for mod in self._modifiers:
            x, y = self._modifiers[mod]
            if mod in self._names: text = self._names[mod]
            else: text = mod
            cr.set_source_surface (self._base_surface, x, y)
            cr.rectangle (x, y, self._width, self._height)
            cr.fill_preserve ()
            if mod in self._current:
                cr.set_source_rgb (0.3, 0.3, 0.3)
                self.write (cr, x + 23, y + 12, text)
                cr.set_source_rgb (0.5, 1, 0)
            else:
                cr.set_source_rgb (0, 0, 0)
            self.write (cr, x + 22, y + 11, text)

    def write (self, cr, x, y, text):
        cr.move_to (x, y)
        markup = '''<span font_desc="%s">%s</span>''' % (self._font, text)
        pcr = pangocairo.CairoContext (cr)
        layout = pcr.create_layout ()
        layout.set_markup (markup)
        pcr.show_layout (layout) 

    def redraw (self, queue = False):
        '''Redraw internal surface'''
        alloc = self.get_allocation ()
        # Prepare drawing surface
        width, height = alloc.width, alloc.height
        self._surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, width, height)
        cr = cairo.Context (self._surface)
        # Clear
        cr.set_operator (cairo.OPERATOR_CLEAR)
        cr.paint ()
        cr.set_operator (cairo.OPERATOR_OVER)
        # Draw
        self.draw (cr, alloc.width, alloc.height)
        # Queue expose event if required
        if queue:
            self.queue_draw ()

    def expose (self, widget, event):
        '''Expose event handler'''
        cr = self.window.cairo_create ()
        if not self._surface:
            self.redraw ()
        cr.set_source_surface (self._surface)
        cr.rectangle (event.area.x, event.area.y,
                      event.area.width, event.area.height)
        cr.clip ()
        cr.paint ()
        return False

    def in_rect (self, x, y, x0, y0, x1, y1):
        return x >= x0 and y >= y0 and x <= x1 and y <= y1
    
    def button_press (self, widget, event):
        x, y = event.x, event.y
        mod = ""

        for modifier in self._modifiers:
            x0, y0 = self._modifiers[modifier]
            if self.in_rect (x, y, x0, y0,
                             x0 + self._width, y0 + self._height):
                mod = modifier
                break

        if not len (mod):
            return
        if mod in self._current:
            self._current.remove (mod)
            self.emit ("removed", mod)
        else:
            self._current.append (mod)
            self.emit ("added", mod)
        self.redraw (queue = True)

# Edge selection widget
#
class EdgeSelector (gtk.DrawingArea):

    __gsignals__    = {"clicked" : (gobject.SIGNAL_RUN_FIRST,
                                    gobject.TYPE_NONE, (gobject.TYPE_STRING, gobject.TYPE_PYOBJECT,))}

    _base_surface   = None
    _surface        = None
    _radius         = 13
    _cradius        = 20
    _coords         = []

    def __init__ (self):
        '''Prepare widget'''
        super (EdgeSelector, self).__init__ ()
        background = "%s/display.png" % PixmapDir
        self._base_surface = cairo.ImageSurface.create_from_png (background)
        self.add_events (gtk.gdk.BUTTON_PRESS_MASK)
        self.connect ("expose_event", self.expose)
        self.connect ("button_press_event", self.button_press)
        self.set_size_request (196, 196)

        # Useful vars
        x0 = 16
        y0 = 24
        x1 = 181
        y1 = 133
        x2 = x0 + 39
        y2 = y0 + 26
        x3 = x1 - 39
        y3 = y1 - 26
        self._coords = (x0, y0, x1, y1, x2, y2, x3, y3)

    def draw (self, cr, width, height):
        '''The actual drawing function'''
        # Useful vars
        x0, y0, x1, y1, x2, y2, x3, y3 = self._coords
        cradius = self._cradius
        radius  = self._radius

        cr.set_line_width(1.0)

        # Top left edge
        cr.new_path ()
        cr.move_to (x0, y0 + cradius)
        cr.line_to (x0, y0)
        cr.line_to (x0 + cradius, y0)
        cr.arc (x0, y0, cradius, 0, pi / 2)
        cr.close_path ()
        self.set_fill_color (cr, "TopLeft")
        cr.fill_preserve ()
        self.set_stroke_color (cr, "TopLeft")
        cr.stroke ()
        # Top right edge
        cr.new_path ()
        cr.move_to (x1, y0 + cradius)
        cr.line_to (x1, y0)
        cr.line_to (x1 - cradius, y0)
        cr.arc_negative (x1, y0, cradius, pi, pi/2)
        cr.close_path ()
        self.set_fill_color (cr, "TopRight")
        cr.fill_preserve ()
        self.set_stroke_color (cr, "TopRight")
        cr.stroke ()
        # Bottom left edge
        cr.new_path ()
        cr.move_to (x0, y1 - cradius)
        cr.line_to (x0, y1)
        cr.line_to (x0 + cradius, y1)
        cr.arc_negative (x0, y1, cradius, 2 * pi, 3 * pi / 2)
        cr.close_path ()
        self.set_fill_color (cr, "BottomLeft")
        cr.fill_preserve ()
        self.set_stroke_color (cr, "BottomLeft")
        cr.stroke ()
        # Bottom right edge
        cr.new_path ()
        cr.move_to (x1, y1 - cradius)
        cr.line_to (x1, y1)
        cr.line_to (x1 - cradius, y1)
        cr.arc (x1, y1, cradius, pi, 3 * pi / 2)
        cr.close_path ()
        self.set_fill_color (cr, "BottomRight")
        cr.fill_preserve ()
        self.set_stroke_color (cr, "BottomRight")
        cr.stroke ()
        # Top edge
        cr.new_path ()
        cr.move_to (x2 + radius, y0)
        cr.line_to (x3 - radius, y0)
        cr.arc (x3 - radius, y0, radius, 0, pi / 2)
        cr.line_to (x2 + radius, y0 + radius)
        cr.arc (x2 + radius, y0, radius, pi / 2, pi)
        cr.close_path ()
        self.set_fill_color (cr, "Top")
        cr.fill_preserve ()
        self.set_stroke_color (cr, "Top")
        cr.stroke ()
        # Bottom edge
        cr.new_path ()
        cr.move_to (x2 + radius, y1)
        cr.line_to (x3 - radius, y1)
        cr.arc_negative (x3 - radius, y1, radius, 0, - pi / 2)
        cr.line_to (x2 + radius, y1 - radius)
        cr.arc_negative (x2 + radius, y1, radius, - pi / 2, pi)
        cr.close_path ()
        self.set_fill_color (cr, "Bottom")
        cr.fill_preserve ()
        self.set_stroke_color (cr, "Bottom")
        cr.stroke ()
        # Left edge
        cr.new_path ()
        cr.move_to (x0, y2 + radius)
        cr.line_to (x0, y3 - radius)
        cr.arc_negative (x0, y3 - radius, radius, pi / 2, 0)
        cr.line_to (x0 + radius, y2 + radius)
        cr.arc_negative (x0, y2 + radius, radius, 0, 3 * pi / 2)
        cr.close_path ()
        self.set_fill_color (cr, "Left")
        cr.fill_preserve ()
        self.set_stroke_color (cr, "Left")
        cr.stroke ()
        # Right edge
        cr.new_path ()
        cr.move_to (x1, y2 + radius)
        cr.line_to (x1, y3 - radius)
        cr.arc (x1, y3 - radius, radius, pi / 2, pi)
        cr.line_to (x1 - radius, y2 + radius)
        cr.arc (x1, y2 + radius, radius, pi, 3 * pi / 2)
        cr.close_path ()
        self.set_fill_color (cr, "Right")
        cr.fill_preserve ()
        self.set_stroke_color (cr, "Right")
        cr.stroke ()

    def set_fill_color (self, cr, edge):
        '''Set painting color for edge'''
        cr.set_source_rgb (0.9, 0.9, 0.9)

    def set_stroke_color (self, cr, edge):
        '''Set stroke color for edge'''
        cr.set_source_rgb (0.45, 0.45, 0.45)

    def redraw (self, queue = False):
        '''Redraw internal surface'''
        alloc = self.get_allocation ()
        # Prepare drawing surface
        width, height = alloc.width, alloc.height
        self._surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, width, height)
        cr = cairo.Context (self._surface)
        # Draw background
        cr.set_source_surface (self._base_surface)
        cr.paint ()
        # Draw
        self.draw (cr, alloc.width, alloc.height)
        # Queue expose event if required
        if queue:
            self.queue_draw ()

    def expose (self, widget, event):
        '''Expose event handler'''
        cr = self.window.cairo_create ()
        if not self._surface:
            self.redraw ()
        cr.set_source_surface (self._surface)
        cr.rectangle (event.area.x, event.area.y,
                      event.area.width, event.area.height)
        cr.clip ()
        cr.paint ()
        return False

    def in_circle_quarter (self, x, y, x0, y0, x1, y1, x2, y2, radius):
        '''Args:
            x, y = point coordinates
            x0, y0 = center coordinates
            x1, y1 = circle square top left coordinates
            x2, y2 = circle square bottom right coordinates
            radius = circle radius'''
        if not self.in_rect (x, y, x1, y1, x2, y2):
            return False
        return self.dist (x, y, x0, y0) <= radius

    def dist (self, x1, y1, x2, y2):
        return sqrt ((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def in_rect (self, x, y, x0, y0, x1, y1):
        return x >= x0 and y >= y0 and x <= x1 and y <= y1

    def button_press (self, widget, event):
        x, y = event.x, event.y
        edge = ""

        # Useful vars
        x0, y0, x1, y1, x2, y2, x3, y3 = self._coords
        cradius = self._cradius
        radius  = self._radius

        if self.in_circle_quarter (x, y, x0, y0, x0, y0,
                                   x0 + cradius, y0 + cradius,
                                   cradius):
            edge = "TopLeft"
        elif self.in_circle_quarter (x, y, x1, y0, x1 - cradius, y0,
                                     x1, y0 + cradius, cradius):
            edge = "TopRight"
        elif self.in_circle_quarter (x, y, x0, y1, x0, y1 - cradius,
                                     x0 + cradius, y1, cradius):
            edge = "BottomLeft"
        elif self.in_circle_quarter (x, y, x1, y1, x1 - cradius, y1 - cradius,
                                     x1, y1, cradius):
            edge = "BottomRight"
        elif self.in_rect (x, y, x2 + radius, y0, x3 - radius, y0 + radius) \
             or self.in_circle_quarter (x, y, x2 + radius, y0, x2, y0,
                                        x2 + radius, y0 + radius, radius) \
             or self.in_circle_quarter (x, y, x3 - radius, y0, x3 - radius, y0,
                                        x3, y0 + radius, radius):
            edge = "Top"
        elif self.in_rect (x, y, x2 + radius, y1 - radius, x3 - radius, y1) \
             or self.in_circle_quarter (x, y, x2 + radius, y1, x2, y1 - radius,
                                        x2 + radius, y1, radius) \
             or self.in_circle_quarter (x, y, x3 - radius, y1,
                                        x3 - radius, y1 - radius,
                                        x3, y1, radius):
            edge = "Bottom"
        elif self.in_rect (x, y, x0, y2 + radius, x0 + radius, y3 - radius) \
             or self.in_circle_quarter (x, y, x0, y2 + radius, x0, y2,
                                        x0 + radius, y2 + radius, radius) \
             or self.in_circle_quarter (x, y, x0, y3 - radius,
                                        x0, y3 - radius,
                                        x0 + radius, y3, radius):
            edge = "Left"
        elif self.in_rect (x, y, x1 - radius, y2 + radius, x1, y3 - radius) \
             or self.in_circle_quarter (x, y, x1, y2 + radius, x1 - radius, y2,
                                        x1, y2 + radius, radius) \
             or self.in_circle_quarter (x, y, x1, y3 - radius,
                                        x1 - radius, y3 - radius,
                                        x1, y3, radius):
            edge = "Right"

        if edge:
            self.emit ("clicked", edge, event)

# Edge selection widget
#
class SingleEdgeSelector (EdgeSelector):

    _current = []

    def __init__ (self, edge):
        '''Prepare widget'''
        EdgeSelector.__init__ (self)
        self._current = edge.split ("|")
        self.connect ('clicked', self.edge_clicked)

    def set_current (self, value):
        self._current = value.split ("|")
        self.redraw (queue = True)

    def get_current (self):
        return "|".join (filter (lambda s: len (s) > 0, self._current))
    current = property (get_current, set_current)

    def set_fill_color (self, cr, edge):
        '''Set painting color for edge'''
        if edge in self._current:
            cr.set_source_rgb (0.64, 1.0, 0.09)
        else:
            cr.set_source_rgb (0.80, 0.00, 0.00)

    def set_stroke_color (self, cr, edge):
        '''Set stroke color for edge'''
        if edge in self._current:
            cr.set_source_rgb (0.31, 0.60, 0.02)
        else:
            cr.set_source_rgb (0.64, 0.00, 0.00)

    def edge_clicked (self, widget, edge, event):
        if not len (edge):
            return
        if edge in self._current:
            self._current.remove (edge)
        else:
            self._current.append (edge)

        self.redraw (queue = True)

# Global Edge Selector
#
class GlobalEdgeSelector(EdgeSelector):

    _settings = []
    _edges = {}
    _text  = {}
    _context = None

    def __init__ (self, context, settings=[]):
        EdgeSelector.__init__ (self)

        self._context = context
        self._settings = settings

        self.connect ("clicked", self.show_popup)

        if len (settings) <= 0:
            self.generate_setting_list ()

    def set_fill_color (self, cr, edge):
        '''Set painting color for edge'''
        if edge in self._edges:
            cr.set_source_rgb (0.64, 1.0, 0.09)
        else:
            cr.set_source_rgb (0.80, 0.00, 0.00)

    def set_stroke_color (self, cr, edge):
        '''Set stroke color for edge'''
        if edge in self._edges:
            cr.set_source_rgb (0.31, 0.60, 0.02)
        else:
            cr.set_source_rgb (0.64, 0.00, 0.00)

    def set_settings (self, value):
        self._settings = value

    def get_settings (self):
        return self._settings
    settings = property (get_settings, set_settings)

    def generate_setting_list (self):
        self._settings = []

        def filter_settings(plugin):
            if plugin.Enabled:
                settings = sorted (GetSettings(plugin), key=SettingKeyFunc)
                settings = filter (lambda s: s.Type == 'Edge', settings)
                return settings
            return []

        for plugin in self._context.Plugins.values ():
            self._settings += filter_settings (plugin)

        for setting in self._settings:
            edges = setting.Value.split ("|")
            for edge in edges:
                self._edges[edge] = setting

    def set_edge_setting (self, setting, edge):
        if not setting:
            if edge in self._edges:
                self._edges.pop(edge)
            for setting in self._settings:
              value = setting.Value.split ("|")
              if edge in value:
                value.remove(edge)
                value = "|".join (filter (lambda s: len (s) > 0, value))
                setting.Value = value
        else:
            value = setting.Value.split ("|")
            if not edge in value:
                value.append (edge)
            value = "|".join (filter (lambda s: len (s) > 0, value))

            conflict = EdgeConflict (setting, value, settings = self._settings, autoResolve = True)
            if conflict.Resolve (GlobalUpdater):
                setting.Value = value
                self._edges[edge] = setting

        self._context.Write()
        self.redraw (queue = True)

    def show_popup (self, widget, edge, event):
        self._text = {}
        comboBox = gtk.combo_box_new_text ()

        comboBox.append_text (_("None"))
        comboBox.set_active (0)
        i = 1
        for setting in self._settings:
            text = "%s: %s" % (setting.Plugin.ShortDesc, setting.ShortDesc)
            comboBox.append_text (text)
            self._text[text] = setting

            if edge in setting.Value.split ("|"):
                comboBox.set_active (i)
            i += 1

        comboBox.set_size_request (200, -1)
        comboBox.connect ('changed', self.combo_changed, edge)

        popup = Popup (self, child=comboBox, decorated=False, mouse=True, modal=False)
        popup.show_all()
        popup.connect ('focus-out-event', self.focus_out)

    def focus_out (self, widget, event):
        combo = widget.get_child ()
        if combo.props.popup_shown:
            return
        gtk_process_events ()
        widget.destroy ()

    def combo_changed (self, widget, edge):
        text = widget.get_active_text ()
        setting = None
        if text != _("None"):
            setting = self._text[text]
        self.set_edge_setting (setting, edge)
        popup = widget.get_parent ()
        popup.destroy ()

# Popup
#
class Popup (gtk.Window):

    def __init__ (self, parent=None, text=None, child=None, decorated=True, mouse=False, modal=True):
        gtk.Window.__init__ (self, gtk.WINDOW_TOPLEVEL)
        self.set_type_hint (gtk.gdk.WINDOW_TYPE_HINT_UTILITY)
        self.set_position (mouse and gtk.WIN_POS_MOUSE or gtk.WIN_POS_CENTER_ALWAYS)
        if parent:
            self.set_transient_for (parent.get_toplevel ())
        self.set_modal (modal)
        self.set_decorated (decorated)
        self.set_property("skip-taskbar-hint", True)
        if text:
            label = gtk.Label (text)
            align = gtk.Alignment ()
            align.set_padding (20, 20, 20, 20)
            align.add (label)
            self.add (align)
        elif child:
            self.add (child)
        gtk_process_events ()

    def destroy (self):
        gtk.Window.destroy (self)
        gtk_process_events ()

# Key Grabber
#
class KeyGrabber (gtk.Button):

    __gsignals__    = {"changed" : (gobject.SIGNAL_RUN_FIRST,
                                    gobject.TYPE_NONE,
                                    [gobject.TYPE_INT, gobject.TYPE_INT]),
                       "current-changed" : (gobject.SIGNAL_RUN_FIRST,
                                    gobject.TYPE_NONE,
                                    [gobject.TYPE_INT, gobject.TYPE_INT])}

    key     = 0
    mods    = 0
    handler = None
    popup   = None

    label   = None

    def __init__ (self, key = 0, mods = 0, label = None):
        '''Prepare widget'''
        super (KeyGrabber, self).__init__ ()

        self.key = key
        self.mods = mods

        self.label = label

        self.connect ("clicked", self.begin_key_grab)
        self.set_label ()

    def begin_key_grab (self, widget):
        self.add_events (gtk.gdk.KEY_PRESS_MASK)
        self.popup = Popup (self, _("Please press the new key combination"))
        self.popup.show_all()
        self.handler = self.popup.connect ("key-press-event",
                                           self.on_key_press_event)
        while gtk.gdk.keyboard_grab (self.popup.window) != gtk.gdk.GRAB_SUCCESS:
            time.sleep (0.1)

    def end_key_grab (self):
        gtk.gdk.keyboard_ungrab (gtk.get_current_event_time ())
        self.popup.disconnect (self.handler)
        self.popup.destroy ()

    def on_key_press_event (self, widget, event):
        mods = event.state & gtk.accelerator_get_default_mod_mask ()

        if event.keyval in (gtk.keysyms.Escape, gtk.keysyms.Return) \
            and not mods:
            if event.keyval == gtk.keysyms.Escape:
                self.emit ("changed", self.key, self.mods)
            self.end_key_grab ()
            self.set_label ()
            return

        key = gtk.gdk.keyval_to_lower (event.keyval)
        if (key == gtk.keysyms.ISO_Left_Tab):
            key = gtk.keysyms.Tab

        if gtk.accelerator_valid (key, mods) \
           or (key == gtk.keysyms.Tab and mods):
            self.set_label (key, mods)
            self.end_key_grab ()
            self.key = key
            self.mods = mods
            self.emit ("changed", self.key, self.mods)
            return

        self.set_label (key, mods)

    def set_label (self, key = None, mods = None):
        if self.label:
            if key != None and mods != None:
                self.emit ("current-changed", key, mods)
            gtk.Button.set_label (self, self.label)
            return
        if key == None and mods == None:
            key = self.key
            mods = self.mods
        label = gtk.accelerator_name (key, mods)
        if not len (label):
            label = _("Disabled")
        gtk.Button.set_label (self, label)

# Match Button
#
class MatchButton(gtk.Button):

    __gsignals__    = {"changed" : (gobject.SIGNAL_RUN_FIRST,
                                    gobject.TYPE_NONE,
                                    [gobject.TYPE_STRING])}

    prefix = {\
            _("Window Title"): 'title',
            _("Window Role"): 'role',
            _("Window Name"): 'name',
            _("Window Class"): 'class',
            _("Window Type"): 'type',
            _("Window ID"): 'xid',
    }

    symbols = {\
            _("And"): '&',
            _("Or"): '|'
    }

    match   = None

    def __init__ (self, entry = None):
        '''Prepare widget'''
        super (MatchButton, self).__init__ ()

        self.entry = entry
        self.match = entry.get_text()

        self.add (Image (name = gtk.STOCK_ADD, type = ImageStock,
                         size = gtk.ICON_SIZE_BUTTON))
        self.connect ("clicked", self.run_edit_dialog)

    def set_match (self, value):
        self.match = value
        self.entry.set_text(value)
        self.entry.activate()

    def get_xprop (self, regexp, proc = "xprop"):
        proc = os.popen (proc)
        output = proc.readlines ()
        rex = re.compile (regexp)
        value = ""
        for line in output:
            if rex.search (line):
                m = rex.match (line)
                value = m.groups () [-1]
                break

        return value

    # Regular Expressions taken from beryl-settings
    def grab_value (self, widget, value_widget, type_widget):
        value = ""
        prefix = self.prefix[type_widget.get_active_text()]

        if prefix == "type":
            value = self.get_xprop("^_NET_WM_WINDOW_TYPE\(ATOM\) = _NET_WM_WINDOW_TYPE_(\w+)")
            value = value.lower().capitalize()
        elif prefix == "role":
            value = self.get_xprop("^WM_WINDOW_ROLE\(STRING\) = \"([^\"]+)\"")
        elif prefix == "name":
            value = self.get_xprop("^WM_CLASS\(STRING\) = \"([^\"]+)\"")
        elif prefix == "class":
            value = self.get_xprop("^WM_CLASS\(STRING\) = \"([^\"]+)\", \"([^\"]+)\"")
        elif prefix == "title":
            value = self.get_xprop("^_NET_WM_NAME\(UTF8_STRING\) = ([^\n]+)")
            if value:
                list = value.split(", ")
                value = ""
                for hex in list:
                    value += "%c" % int(hex, 16)
            else:
                value = self.get_xprop("^WM_NAME\(STRING\) = \"([^\"]+)\"")
        elif prefix == "id":
            value = self.get_xprop("^xwininfo: Window id: ([^\s]+)", "xwininfo")

        value_widget.set_text(value)

    def generate_match (self, type, value, relation, invert):
        match = ""
        text = self.match

        prefix = self.prefix[type]
        symbol = self.symbols[relation]

        # check if the current match needs some brackets
        if len(text) > 0 and text[-1] != ')' and text[0] != '(':
            match = "(%s)" % text
        else:
            match = text

        if invert:
            match = "%s %s !(%s=%s)" % (match, symbol, prefix, value)
        elif len(match) > 0:
            match = "%s %s %s=%s" % (match, symbol, prefix, value)
        else:
            match = "%s=%s" % (prefix, value)

        self.set_match (match)

    def _check_entry_value (self, entry, dialog):
        is_valid = False
        value = entry.get_text()
        if value != "":
            is_valid = True
        dialog.set_response_sensitive(gtk.RESPONSE_OK, is_valid)

    def run_edit_dialog (self, widget):
        '''Run dialog to generate a match'''

        self.match = self.entry.get_text ()

        dlg = gtk.Dialog (_("Edit match"))
        dlg.set_position (gtk.WIN_POS_CENTER_ON_PARENT)
        dlg.set_transient_for (self.get_parent ().get_toplevel ())
        dlg.add_button (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        dlg.add_button (gtk.STOCK_ADD, gtk.RESPONSE_OK).grab_default ()
        dlg.set_response_sensitive(gtk.RESPONSE_OK, False)
        dlg.set_default_response (gtk.RESPONSE_OK)

        table = gtk.Table ()

        rows = []

        # Type
        label = Label (_("Type"))
        type_chooser = gtk.combo_box_new_text ()
        for type in self.prefix.keys ():
            type_chooser.append_text (type)
        type_chooser.set_active (0)
        rows.append ((label, type_chooser))

        # Value
        label = Label (_("Value"))
        box = gtk.HBox ()
        box.set_spacing (5)
        entry = gtk.Entry ()
        entry.connect ('changed', self._check_entry_value, dlg)
        button = gtk.Button (_("Grab"))
        button.connect ('clicked', self.grab_value, entry, type_chooser)
        box.pack_start (entry, True, True)
        box.pack_start (button, False, False)
        rows.append ((label, box))

        # Relation
        label = Label (_("Relation"))
        relation_chooser = gtk.combo_box_new_text ()
        for relation in self.symbols.keys ():
            relation_chooser.append_text (relation)
        relation_chooser.set_active (0)
        rows.append ((label, relation_chooser))

        # Invert
        label = Label (_("Invert"))
        check = gtk.CheckButton ()
        rows.append ((label, check))

        row = 0
        for label, widget in rows:
            table.attach(label, 0, 1, row, row+1, yoptions=0, xpadding=TableX, ypadding=TableY)
            table.attach(widget, 1, 2, row, row+1, yoptions=0, xpadding=TableX, ypadding=TableY)
            row += 1

        dlg.vbox.pack_start (table)
        dlg.vbox.set_spacing (5)
        dlg.show_all ()

        response = dlg.run ()
        dlg.hide ()
        if response == gtk.RESPONSE_OK:
            type     = type_chooser.get_active_text ()
            value    = entry.get_text ()
            relation = relation_chooser.get_active_text ()
            invert   = check.get_active ()
            self.generate_match (type, value, relation, invert)

        dlg.destroy ()

class FileButton (gtk.Button):
    __gsignals__    = {"changed" : (gobject.SIGNAL_RUN_FIRST,
                                    gobject.TYPE_NONE,
                                    [gobject.TYPE_STRING])}
    _directory = False
    _context   = None
    _image     = False
    _path      = ""

    def __init__ (self, context, entry, directory=False, image=False, path=""):
        gtk.Button.__init__ (self)

        self._entry = entry
        self._directory = directory
        self._context = context
        self._image = image
        self._path = path

        self.set_tooltip_text(_("Browse..."))
        self.set_image(gtk.image_new_from_stock(
            gtk.STOCK_OPEN, gtk.ICON_SIZE_BUTTON))
        self.connect('clicked', self.open_dialog)

    def set_path (self, value):
        self._path = value
        self._entry.set_text (value)
        self._entry.activate ()

    def create_filter(self):
        filter = gtk.FileFilter ()
        if self._image:
            filter.set_name (_("Images"))
            filter.add_pattern ("*.png")
            filter.add_pattern ("*.jpg")
            filter.add_pattern ("*.jpeg")
            filter.add_pattern ("*.svg")
        else:
            filter.add_pattern ("*")
            filter.set_name (_("File"))

        return filter

    def check_type (self, filename):
        if filename.find (".") == -1:
            return True
        ext = filename.split (".") [-1]

        try:
            mime = mimetypes.types_map [".%s" %ext]
        except KeyError:
            return True

        if self._image:
            require = FeatureRequirement (self._context, 'imagemime:' + mime)
            return require.Resolve ()

        return True

    def update_preview (self, widget):
        path = widget.get_preview_filename ()
        if path is None or os.path.isdir (path):
            widget.get_preview_widget ().set_from_file (None)
            return
        try:
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size (path, 128, 128)
        except gobject.GError:
            return
        widget.get_preview_widget ().set_from_pixbuf (pixbuf)

    def open_dialog (self, widget):
        b = (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK)
        if self._directory:
            title = _("Open directory...")
        else:
            title = _("Open file...")

        chooser = gtk.FileChooserDialog (title = title, buttons = b)
        if self._directory:
            chooser.set_action (gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        else:
            chooser.set_filter (self.create_filter ())

        if self._path and os.path.exists (self._path):
            chooser.set_filename (self._path)
        else:
            chooser.set_current_folder (os.environ.get("HOME"))

        if self._image:
            chooser.set_use_preview_label (False)
            chooser.set_preview_widget (gtk.Image ())
            chooser.connect ("selection-changed", self.update_preview)

        ret = chooser.run ()

        filename = chooser.get_filename ()
        chooser.destroy ()
        if ret == gtk.RESPONSE_OK:
            if self._directory or self.check_type (filename):
                self.set_path (filename)

# About Dialog
#
class AboutDialog (gtk.AboutDialog):
    def __init__ (self, parent):
        gtk.AboutDialog.__init__ (self)
        self.set_transient_for (parent)

        self.set_name (_("CompizConfig Settings Manager"))
        self.set_version (Version)
        self.set_comments (_("This is a settings manager for the CompizConfig configuration system."))
        self.set_copyright ("Copyright \xC2\xA9 2007-2008 Patrick Niklaus/Christopher Williams/Guillaume Seguin/Quinn Storm")
        self.set_translator_credits (_("translator-credits"))
        self.set_authors (["Patrick Niklaus <marex@opencompositing.org>",
                           "Christopher Williams <christopherw@verizon.net>",
                           "Guillaume Seguin <guillaume@segu.in>",
                           "Quinn Storm <quinn@beryl-project.org>"])
        self.set_artists (["Andrew Wedderburn <andrew.wedderburn@gmail.com>",
                           "Patrick Niklaus <marex@opencompositing.org>",
                           "Gnome Icon Theme Team"])
        if IconTheme.lookup_icon("ccsm", 64, 0):
            icon = IconTheme.load_icon("ccsm", 64, 0)
            self.set_logo (icon)
        self.set_website ("http://www.compiz-fusion.org")

# Error dialog
#
class ErrorDialog (gtk.MessageDialog):
    '''Display an error dialog'''

    def __init__ (self, parent, message):
        gtk.MessageDialog.__init__ (self, parent,
                                    gtk.DIALOG_DESTROY_WITH_PARENT,
                                    gtk.MESSAGE_ERROR,
                                    gtk.BUTTONS_CLOSE)
        self.set_position (gtk.WIN_POS_CENTER)
        self.set_markup (message)
        self.set_title (_("An error has occured"))
        self.set_transient_for (parent)
        self.set_modal (True)
        self.show_all ()
        self.connect ("response", lambda *args: self.destroy ())

# Warning dialog
#
class WarningDialog (gtk.MessageDialog):
    '''Display a warning dialog'''

    def __init__ (self, parent, message):
        gtk.MessageDialog.__init__ (self, parent,
                                    gtk.DIALOG_DESTROY_WITH_PARENT,
                                    gtk.MESSAGE_WARNING,
                                    gtk.BUTTONS_YES_NO)
        self.set_position (gtk.WIN_POS_CENTER)
        self.set_markup (message)
        self.set_title (_("Warning"))
        self.set_transient_for (parent)
        self.connect_after ("response", lambda *args: self.destroy ())

# Plugin Button
#
class PluginButton (gtk.HBox):

    __gsignals__    = {"clicked"   : (gobject.SIGNAL_RUN_FIRST,
                                      gobject.TYPE_NONE,
                                      []),
                       "activated" : (gobject.SIGNAL_RUN_FIRST,
                                      gobject.TYPE_NONE,
                                      [])}

    _plugin = None

    def __init__ (self, plugin, useMissingImage = False):
        gtk.HBox.__init__(self)
        self._plugin = plugin

        image = Image (plugin.Name, ImagePlugin, 32, useMissingImage)
        label = Label (plugin.ShortDesc, 120)
        label.connect ('style-set', self.style_set)
        box = gtk.HBox ()
        box.set_spacing (5)
        box.pack_start (image, False, False)
        box.pack_start (label)

        button = PrettyButton ()
        button.connect ('clicked', self.show_plugin_page)
        button.set_tooltip_text (plugin.LongDesc)
        button.add (box)

        if plugin.Name != 'core':
            enable = gtk.CheckButton ()
            enable.set_tooltip_text(_("Enable %s") % plugin.ShortDesc)
            enable.set_active (plugin.Enabled)
            enable.set_sensitive (plugin.Context.AutoSort)
            self._toggled_handler = enable.connect ("toggled", self.enable_plugin)
            PluginSetting (plugin, enable, self._toggled_handler)
            self.pack_start (enable, False, False)
        self.pack_start (button, False, False)

        self.set_size_request (220, -1)

    StyleBlock = 0

    def style_set (self, widget, previous):
        if self.StyleBlock > 0:
            return
        self.StyleBlock += 1
        widget.modify_fg(gtk.STATE_NORMAL, widget.style.text[gtk.STATE_NORMAL])
        self.StyleBlock -= 1

    def enable_plugin (self, widget):

        plugin = self._plugin
        conflicts = plugin.Enabled and plugin.DisableConflicts or plugin.EnableConflicts

        conflict = PluginConflict (plugin, conflicts)

        if conflict.Resolve ():
            plugin.Enabled = widget.get_active ()
        else:
            widget.handler_block(self._toggled_handler)
            widget.set_active (plugin.Enabled)
            widget.handler_unblock(self._toggled_handler)

        plugin.Context.Write ()
        GlobalUpdater.UpdatePlugins()
        plugin.Context.UpdateExtensiblePlugins ()
        self.emit ('activated')

    def show_plugin_page (self, widget):
        self.emit ('clicked')

    def filter (self, text, level=FilterAll):
        found = False
        if level & FilterName:
            if (text in self._plugin.Name.lower ()
            or text in self._plugin.ShortDesc.lower ()):
                found = True
        if not found and level & FilterLongDesc:
            if text in self._plugin.LongDesc.lower():
                found = True
        if not found and level & FilterCategory:
            if text == None \
            or (text == "" and self._plugin.Category.lower() == "") \
            or (text != "" and text in self._plugin.Category.lower()):
                found = True

        return found

    def get_plugin (self):
        return self._plugin

# Category Box
#
class CategoryBox(gtk.VBox):

    _plugins = None
    _unfiltered_plugins = None
    _buttons = None
    _context = None
    _name    = ""
    _tabel   = None
    _alignment = None
    _current_cols = 0
    _current_plugins = 0

    def __init__ (self, context, name, plugins=None, categoryIndex=0):
        gtk.VBox.__init__ (self)

        self.set_spacing (5)

        self._context = context
        if plugins is not None:
            self._plugins = plugins
        else:
            self._plugins = []

        if not plugins:
            for plugin in context.Plugins.values ():
                if plugin.Category == name:
                    self._plugins.append (plugin)

        self._plugins.sort(key=PluginKeyFunc)
        self._name = name
        text = name or 'Uncategorized'

        # Keep unfiltered list of plugins for correct background icon loading
        self._unfiltered_plugins = self._plugins

        header = gtk.HBox ()
        header.set_border_width (5)
        header.set_spacing (10)
        label = Label ('', -1)
        label.set_markup ("<span color='#aaa' size='x-large' weight='800'>%s</span>" % _(text))

        icon = text.lower ().replace (" ", "_")
        image = Image (icon, ImageCategory)
        header.pack_start (image, False, False)
        header.pack_start (label, False, False)

        self._table = gtk.Table ()
        self._table.set_border_width (10)

        # load icons now only for the first 3 categories
        dontLoadIcons = (categoryIndex >= 3);

        self._buttons = []
        for plugin in self._plugins:
            button = PluginButton(plugin, dontLoadIcons)
            self._buttons.append(button)

        self._alignment = gtk.Alignment (0, 0, 1, 1)
        self._alignment.set_padding (0, 20, 0, 0)
        self._alignment.add (gtk.HSeparator ())

        self.pack_start (header, False, False)
        self.pack_start (self._table, False, False)
        self.pack_start (self._alignment)

    def show_separator (self, show):
        children = self.get_children ()
        if show:
            if self._alignment not in children:
                self.pack_start (self._alignment)
        else:
            if self._alignment in children:
                self.remove(self._alignment)

    def filter_buttons (self, text, level=FilterAll):
        self._plugins = []
        for button in self._buttons:
            if button.filter (text, level=level):
                self._plugins.append (button.get_plugin())

        return bool(self._plugins)

    def rebuild_table (self, ncols, force = False):
        if (not force and ncols == self._current_cols
        and len (self._plugins) == self._current_plugins):
            return
        self._current_cols = ncols
        self._current_plugins = len (self._plugins)

        children = self._table.get_children ()
        if children:
            for child in children:
                self._table.remove(child)

        row = 0
        col = 0
        for button in self._buttons:
            if button.get_plugin () in self._plugins:
                self._table.attach (button, col, col+1, row, row+1, 0, xpadding=TableX, ypadding=TableY)
                col += 1
                if col == ncols:
                    col = 0
                    row += 1
        self.show_all ()

    def get_buttons (self):
        return self._buttons

    def get_plugins (self):
        return self._plugins

    def get_unfiltered_plugins (self):
        return self._unfiltered_plugins

# Plugin Window
#
class PluginWindow(gtk.ScrolledWindow):
    __gsignals__    = {"show-plugin" : (gobject.SIGNAL_RUN_FIRST,
                                        gobject.TYPE_NONE,
                                        [gobject.TYPE_PYOBJECT])}

    _not_found_box = None
    _style_block   = 0
    _context       = None
    _categories    = None
    _viewport      = None
    _boxes         = None
    _box           = None

    def __init__ (self, context, categories=[], plugins=[]):
        gtk.ScrolledWindow.__init__ (self)

        self._categories = {}
        self._boxes = []
        self._context = context
        pool = plugins or self._context.Plugins.values()
        if len (categories):
            for plugin in pool:
                category = plugin.Category
                if category in categories:
                    if not category in self._categories:
                        self._categories[category] = []
                    self._categories[category].append(plugin)
        else:
            for plugin in pool:
                category = plugin.Category
                if not category in self._categories:
                    self._categories[category] = []
                self._categories[category].append(plugin)

        self.props.hscrollbar_policy = gtk.POLICY_NEVER
        self.props.vscrollbar_policy = gtk.POLICY_AUTOMATIC
        self.connect ('size-allocate', self.rebuild_boxes)

        self._box = gtk.VBox ()
        self._box.set_spacing (5)

        self._not_found_box = NotFoundBox ()

        categories = sorted(self._categories, key=CategoryKeyFunc)
        for (i, category) in enumerate(categories):
            plugins = self._categories[category]
            category_box = CategoryBox(context, category, plugins, i)
            self.connect_buttons (category_box)
            self._boxes.append (category_box)
            self._box.pack_start (category_box, False, False)

        viewport = gtk.Viewport ()
        viewport.connect("style-set", self.set_viewport_style)
        viewport.set_focus_vadjustment (self.get_vadjustment ())
        viewport.add (self._box)
        self.add (viewport)

    def connect_buttons (self, category_box):
        buttons = category_box.get_buttons ()
        for button in buttons:
            button.connect('clicked', self.show_plugin_page)

    def set_viewport_style (self, widget, previous):
        if self._style_block > 0:
            return
        self._style_block += 1
        widget.modify_bg(gtk.STATE_NORMAL, widget.style.base[gtk.STATE_NORMAL])
        self._style_block -= 1

    def filter_boxes (self, text, level=FilterAll):
        found = False

        for box in self._boxes:
            found |= box.filter_buttons (text, level)

        viewport = self.get_child ()
        child    = viewport.get_child ()

        if not found:
            if child is not self._not_found_box:
                viewport.remove (self._box)
                viewport.add (self._not_found_box)
            self._not_found_box.update (text)
        else:
            if child is self._not_found_box:
                viewport.remove (self._not_found_box)
                viewport.add (self._box)

        self.queue_resize()
        self.show_all()

    def rebuild_boxes (self, widget, request):
        ncols = request.width / 220
        width = ncols * (220 + 2 * TableX) + 40
        if width > request.width:
            ncols -= 1

        pos = 0
        last_box = None
        children = self._box.get_children ()
        for box in self._boxes:
            plugins = box.get_plugins ()
            if len (plugins) == 0:
                if box in children:
                    self._box.remove(box)
            else:
                if last_box:
                    last_box.show_separator (True)

                if box not in children:
                    self._box.pack_start (box, False, False)
                    self._box.reorder_child (box, pos)
                box.rebuild_table (ncols)
                box.show_separator (False)
                pos += 1

                last_box = box

    def get_categories (self):
        return self._categories.keys ()

    def show_plugin_page (self, widget):
        plugin = widget.get_plugin ()
        self.emit ('show-plugin', plugin)

