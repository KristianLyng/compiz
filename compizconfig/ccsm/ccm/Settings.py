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
import gobject
import os

from ccm.Constants import *
from ccm.Conflicts import *
from ccm.Widgets import *
from ccm.Utils import *
from ccm.Pages import *

import locale
import gettext
locale.setlocale(locale.LC_ALL, "")
gettext.bindtextdomain("ccsm", DataDir + "/locale")
gettext.textdomain("ccsm")
_ = gettext.gettext

NAItemText = _("N/A")

class Setting(object):

    NoneValue = ''

    def __init__(self, Setting=None, Settings=None, List=False):
        self.Setting = Setting
        self.Settings = Settings # for multi-list settings
        self.List = List
        if List:
            self.CurrentRow = None

        self.Blocked = 0
        self.EBox = gtk.EventBox()
        self.Box = gtk.HBox()
        self.EBox.set_visible_window(False)
        if Setting:
            self.EBox.set_sensitive(not Setting.ReadOnly)
        self.Box.set_spacing(5)
        self.EBox.add(self.Box)
        self.Reset = gtk.Button()
        if not Settings:
            self.MakeLabel()
            markup = "%s\n<small><i>%s</i></small>" % (self.Setting.LongDesc, self.Setting.Name)
            self.EBox.set_tooltip_markup(markup)
            self.Reset.set_tooltip_text(_("Reset setting to the default value"))
        self.Reset.set_image (Image (name = gtk.STOCK_CLEAR, type = ImageStock,
                                     size = gtk.ICON_SIZE_BUTTON))
        self.Reset.connect('clicked', self.DoReset)
        self._Init()

        self.EBox.connect("destroy", self.OnDestroy)

        self.AddUpdater()

    def AddUpdater(self):
        GlobalUpdater.Append(self)

    def RemoveUpdater(self):
        GlobalUpdater.Remove(self)

    def OnDestroy(self, widget):
        self.RemoveUpdater()

    def GetColumn(self, num):
        return (str, gtk.TreeViewColumn(self.Setting.ShortDesc, gtk.CellRendererText(), text=num))

    def PureVirtual (self, func):
        message = "Missing %(function)s function for %(name)s setting (%(class)s)"

        msg_dict = {'function': func,
                    'name': self.Setting.Name,
                    'class': self}

        value = message % msg_dict
        raise PureVirtualError, value

    def _Init(self):
        self.PureVirtual('_Init')
    
    def DoReset(self, foo):
        self.Setting.Reset()
        self.Setting.Plugin.Context.Write()
        self.Read()

    def MakeLabel(self):

        if not self.Setting:
            return

        label = gtk.Label()
        desc = protect_pango_markup (self.Setting.ShortDesc)
        style = "%s"
        if self.Setting.Integrated:
            style = "<i>%s</i>"
        label.set_markup(style % desc)
        label.props.xalign = 0
        label.set_size_request(160, -1)
        label.props.wrap_mode = pango.WRAP_WORD
        label.set_line_wrap(True)
        self.Label = label

    def Block(self):
        self.Blocked += 1
    
    def UnBlock(self):
        self.Blocked -= 1

    def Read(self):
        self.Block()
        self._Read()
        self.UnBlock()

    def _Read(self):
        self.PureVirtual('_Read')

    def Changed(self, *args, **kwargs):
        if self.Blocked <= 0:
            self._Changed()
            self.Setting.Plugin.Context.Write()

    def _Changed(self):
        self.PureVirtual('_Changed')

    def Get(self):
        if self.List:
            if self.CurrentRow is not None:
                return self.Setting.Value[self.CurrentRow]
            else:
                return self.NoneValue
        else:
            return self.Setting.Value
    
    def GetForRenderer(self):
        return self.Setting.Value

    def Set(self, value):
        if self.List:
            if self.CurrentRow is not None:
                vlist = self.Setting.Value
                vlist[self.CurrentRow] = value
                self.Setting.Value = vlist
        else:
            self.Setting.Value = value

    def Swap(self, a, b):
        vlist = self.Setting.Value
        vlist.insert(b, vlist.pop(a))
        self.Setting.Value = vlist

    def _SetHidden(self, visible):

        self.EBox.props.no_show_all = not visible

        if visible:
            self.EBox.show()
        else:
            self.EBox.hide()

    def _Filter(self, text, level):
        visible = False
        if text is not None:
            if level & FilterName:
                visible = (text in self.Setting.Name.lower()
                    or text in self.Setting.ShortDesc.lower())
            if not visible and level & FilterLongDesc:
                visible = text in self.Setting.LongDesc.lower()
            if not visible and level & FilterValue:
                visible = text in str(self.Setting.Value).lower()
        else:
            visible = True
        return visible

    def Filter(self, text, level=FilterAll):
        visible = self._Filter(text, level=level)
        self._SetHidden(visible)
        return visible

    def __hash__(self):
        if self.Setting is not None:
            return hash(self.Setting)
        else:
            raise TypeError

class StockSetting(Setting):

    def _Init(self):
        self.Box.pack_start(self.Label, False, False)
        self.Box.pack_end(self.Reset, False, False)

class StringSetting(StockSetting):
    def _Init(self):
        StockSetting._Init(self)
        self.Entry = gtk.Entry()
        self.Entry.connect('activate', self.Changed)
        self.Entry.connect('focus-out-event', self.Changed)
        self.Widget = self.Entry
        self.Box.pack_start(self.Widget, True, True)

    def _Read(self):
        self.Entry.set_text(self.Get())

    def _Changed(self):
        self.Set(self.Entry.get_text())

class MatchSetting(StringSetting):
    def _Init(self):
        StringSetting._Init(self)
        self.MatchButton = MatchButton(self.Entry)
        self.Box.pack_start(self.MatchButton, False, False)

class FileStringSetting(StringSetting):

    def __init__(self, setting, List=False, isImage=False, isDirectory=False):
        self.isImage = isImage
        self.isDirectory = isDirectory
        StringSetting.__init__(self, setting, List=List)

    def _Init(self):
        StringSetting._Init(self)
        self.FileButton = FileButton(self.Setting.Plugin.Context, self.Entry,
            self.isDirectory, self.isImage)
        self.Box.pack_start(self.FileButton, False, False)

class EnumSetting(StockSetting):

    NoneValue = 0

    def _Init(self):
        StockSetting._Init(self)
        self.Combo = gtk.combo_box_new_text()
        if self.List:
            self.Info = self.Setting.Info[1][2]
        else:
            self.Info = self.Setting.Info[2]
        self.SortedItems = sorted(self.Info.items(), key=EnumSettingKeyFunc)
        for name, value in self.SortedItems:
            self.Combo.append_text(name)
        self.Combo.connect('changed', self.Changed)

        self.Widget = self.Combo
        self.Box.pack_start(self.Combo, True, True)

    def _CellEdited(self, cell, path, new_text):
        self.CurrentRow = int(path[0])
        value = self.Info[new_text]
        self.Store[path][self.Num] = new_text
        self.Set(value)
        self.Setting.Plugin.Context.Write()

    def GetColumn(self, num):
        self.Num = num
        cell = gtk.CellRendererCombo()
        column = gtk.TreeViewColumn(self.Setting.ShortDesc, cell, text=num)
        model = gtk.ListStore(str)
        for property, value in [("model", model), ("text_column", 0),
                                ("editable", False), ("has_entry", False)]:
            cell.set_property (property, value)
        cell.connect("edited", self._CellEdited)
        for item, i in self.SortedItems:
            model.append([item])

        return (str, column)

    def GetForRenderer(self):
        return [self.SortedItems[pos][0] for pos in self.Setting.Value]

    def _Read(self):
        self.Combo.set_active(self.Get())

    def _Changed(self):
        active = self.Combo.get_active_text()
        
        self.Set(self.Info[active])

    def _Filter(self, text, level):
        visible = Setting._Filter(self, text, level=level)
        if text is not None and not visible and level & FilterValue:
            visible = any(text in s.lower() for s in self.Info)
        return visible

class RestrictedStringSetting(StockSetting):

    NoneValue = ''

    def _Init(self):
        StockSetting._Init(self)
        self.Combo = gtk.combo_box_new_text()
        if self.List:
            info = self.Setting.Info[1]
        else:
            info = self.Setting.Info

        self.ItemsByName = info[0]
        self.ItemsByValue = info[1]
        self.SortedItems = info[2]

        # Use the first item in the list as the default value
        self.NoneValue = self.ItemsByName[self.SortedItems[0][0]]

        for (i, (name, value)) in enumerate(self.SortedItems):
            self.Combo.append_text(name)
        self.Combo.connect('changed', self.Changed)

        self.Widget = self.Combo
        self.Box.pack_start(self.Combo, True, True)

        self.OriginalValue = None
        self.NAItemShift = 0

    def _CellEdited(self, cell, path, new_text):
        self.CurrentRow = int(path[0])
        value = self.ItemsByName[new_text]
        self.Store[path][self.Num] = new_text
        self.Set(value)
        self.Setting.Plugin.Context.Write()

    def GetColumn(self, num):
        self.Num = num
        cell = gtk.CellRendererCombo()
        column = gtk.TreeViewColumn(self.Setting.ShortDesc, cell, text=num)
        model = gtk.ListStore(str)
        for property, value in [("model", model), ("text_column", 0),
                                ("editable", False), ("has_entry", False)]:
            cell.set_property (property, value)
        cell.connect("edited", self._CellEdited)
        for item, i in self.SortedItems:
            model.append([item])

        return (str, column)

    def GetItemText (self, val):
        text = self.ItemsByValue.get(val)
        if text is None:
            return NAItemText
        return self.SortedItems[text[1]][0]

    def GetForRenderer(self):
        return [self.GetItemText(val) for val in self.Setting.Value]

    def _Read(self):
        value = self.Get()

        if not self.OriginalValue:
            self.OriginalValue = value

            # if current value is not provided by any restricted string extension,
            # insert an N/A item at the beginning
            if not self.ItemsByValue.has_key(self.OriginalValue):
                self.NAItemShift = 1
                self.Combo.insert_text(0, NAItemText)

        if self.ItemsByValue.has_key(value):
            self.Combo.set_active(self.ItemsByValue[self.Get()][1] + \
                                  self.NAItemShift)
        else:
            self.Combo.set_active(0)

    def _Changed(self):
        active = self.Combo.get_active_text()
        
        if active == NAItemText:
            activeValue = self.OriginalValue
        else:
            activeValue = self.ItemsByName[active]
        self.Set(activeValue)

    def _Filter(self, text, level):
        visible = Setting._Filter(self, text, level=level)
        if text is not None and not visible and level & FilterValue:
            visible = any(text in s.lower() for s in self.ItemsByName)
        return visible

class BoolSetting (StockSetting):

    NoneValue = False

    def _Init (self):
        StockSetting._Init(self)
        self.Label.set_size_request(-1, -1)
        self.CheckButton = gtk.CheckButton ()
        align = gtk.Alignment(yalign=0.5)
        align.add(self.CheckButton)
        self.Box.pack_end(align, False, False)
        self.CheckButton.connect ('toggled', self.Changed)

    def _Read (self):
        self.CheckButton.set_active (self.Get())

    def _Changed (self):
        self.Set(self.CheckButton.get_active ())

    def CellToggled (self, cell, path):
        self.CurrentRow = int(path)
        self.Set(not cell.props.active)
        self.Store[path][self.Num] = self.Get()
        self.Setting.Plugin.Context.Write()

    def GetColumn (self, num):
        self.Num = num
        cell = gtk.CellRendererToggle()
        cell.set_property("activatable", True)
        cell.connect('toggled', self.CellToggled)
        return (bool, gtk.TreeViewColumn(self.Setting.ShortDesc, cell, active=num))

class NumberSetting(StockSetting):

    NoneValue = 0

    def _Init(self):
        StockSetting._Init(self)
        if self.List:
            self.Info = info = self.Setting.Info[1]
        else:
            self.Info = info = self.Setting.Info

        if self.Inc is None:
            self.Inc = info[2]
        inc = self.Inc
        self.NoneValue = info[0]
        self.Adj = gtk.Adjustment(self.Get(), info[0], info[1], inc, inc*10)
        self.Spin = gtk.SpinButton(self.Adj)

        self.Scale = gtk.HScale(self.Adj)

        self.Scale.set_update_policy(gtk.UPDATE_DISCONTINUOUS)
        self.Scale.connect("value-changed", self.Changed)
        self.Spin.connect("value-changed", self.Changed)
        self.Widget = self.Scale

        self.Box.pack_start(self.Scale, True, True)
        self.Box.pack_start(self.Spin, False, False)

    def _Read(self):
        self.Adj.set_value(self.Get())

    def _Changed(self):
        self.Set(self.Adj.get_value())

class IntSetting(NumberSetting):

    def _Init(self):
        self.Inc = 1
        NumberSetting._Init(self)
        self.Spin.set_digits(0)
        self.Scale.set_digits(0)

class FloatSetting(NumberSetting):

    NoneValue = 0.0

    def _Init(self):
        self.Inc = None
        NumberSetting._Init(self)
        self.Spin.set_digits(4)
        self.Scale.set_digits(4)


class ColorSetting(StockSetting):

    NoneValue = (0, 0, 0, 65535) # opaque black

    def _Init(self):
        StockSetting._Init(self)
        self.Button = gtk.ColorButton()
        self.Button.set_size_request (100, -1)
        self.Button.set_use_alpha(True)
        self.Button.connect('color-set', self.Changed)

        self.Widget = gtk.Alignment (1, 0.5)
        self.Widget.add (self.Button)
        self.Box.pack_start(self.Widget, True, True)

    def GetForRenderer(self):
        return ["#%.4x%.4x%.4x%.4x" %tuple(seq) for seq in self.Setting.Value]

    def GetColumn(self, num):
        return (str, gtk.TreeViewColumn(self.Setting.ShortDesc, CellRendererColor(), text=num))

    def _Read(self):
        col = gtk.gdk.Color()
        value = self.Get()
        col.red, col.green, col.blue = value[:3]
        self.Button.set_color(col)
        self.Button.set_alpha(value[3])

    def _Changed(self):
        col = self.Button.get_color()
        alpha = self.Button.get_alpha()
        self.Set([col.red, col.green, col.blue, alpha])

class BaseListSetting(Setting):
    def _Init(self):
        self.Widget = gtk.VBox()
        self.EditDialog = None        
        self.EditDialogOpen = False
        self.PageToBeRefreshed = None

        self.Widgets = []
        for i, setting in enumerate(self.Settings):
            self.Widgets.append(MakeSetting(setting, List=True))

        types, cols = self.ListInfo()
        self.Types = types
        self.Store = gtk.ListStore(*types)
        self.View = gtk.TreeView(self.Store)
        self.View.set_headers_visible(True)

        for widget in self.Widgets:
            widget.Store = self.Store
            widget.Box.remove(widget.Reset)
            widget.ListWidget = self
        for col in cols:
            self.View.append_column(col)

        self.View.connect('row-activated', self.Activated)
        self.View.connect('button-press-event', self.ButtonPressEvent)
        self.View.connect('key-press-event', self.KeyPressEvent)
        self.Select = self.View.get_selection()
        self.Select.set_mode(gtk.SELECTION_SINGLE)
        self.Select.connect('changed', self.SelectionChanged)
        self.Widget.set_spacing(5)
        self.Scroll = gtk.ScrolledWindow()
        self.Scroll.props.hscrollbar_policy = gtk.POLICY_AUTOMATIC
        self.Scroll.props.vscrollbar_policy = gtk.POLICY_NEVER
        self.Scroll.add(self.View)
        self.Widget.pack_start(self.Scroll, True, True)
        self.Widget.set_child_packing(self.Scroll, True, True, 0, gtk.PACK_START)
        buttonBox = gtk.HBox(False)
        buttonBox.set_spacing(5)
        buttonBox.set_border_width(5)
        self.Widget.pack_start(buttonBox, False, False)
        buttonTypes = ((gtk.STOCK_NEW, self.Add, None, True),
                 (gtk.STOCK_DELETE, self.Delete, None, False), 
                 (gtk.STOCK_EDIT, self.Edit, None, False),
                 (gtk.STOCK_GO_UP, self.Move, 'up', False), 
                 (gtk.STOCK_GO_DOWN, self.Move, 'down', False),)
        self.Buttons = {}
        for stock, callback, data, sensitive in buttonTypes:
            b = gtk.Button(stock)
            b.set_use_stock(True)
            buttonBox.pack_start(b, False, False)
            if data is not None:
                b.connect('clicked', callback, data)
            else:
                b.connect('clicked', callback)
            b.set_sensitive(sensitive)
            self.Buttons[stock] = b

        self.Popup = gtk.Menu()
        self.PopupItems = {}
        edit = gtk.ImageMenuItem(stock_id=gtk.STOCK_EDIT)
        edit.connect('activate', self.Edit)
        edit.set_sensitive(False)
        self.Popup.append(edit)
        self.PopupItems[gtk.STOCK_EDIT] = edit
        delete = gtk.ImageMenuItem(stock_id=gtk.STOCK_DELETE)
        delete.connect('activate', self.Delete)
        delete.set_sensitive(False)
        self.Popup.append(delete)
        self.PopupItems[gtk.STOCK_DELETE] = delete
        self.Popup.show_all()

        buttonBox.pack_end(self.Reset, False, False)

        self.Box.pack_start(self.Widget)

    def AddUpdater(self):
        pass

    def RemoveUpdater(self):
        if self.Settings:
            for widget in self.Widgets:
                widget.EBox.destroy()

    def DoReset(self, widget):
        for setting in self.Settings:
            setting.Reset()
        self.Settings[0].Plugin.Context.Write()
        self.Read()

    def MakeLabel(self):
        pass
    
    def Add(self, *args):
        for widget, setting in zip(self.Widgets, self.Settings):
            vlist = setting.Value
            vlist.append(widget.NoneValue)
            setting.Value = vlist
        self.Settings[0].Plugin.Context.Write()
        self.Read()
        self._Edit(len(self.Store)-1)

    def _Delete(self, row):

        for setting in self.Settings:
            vlist = setting.Value
            del vlist[row]
            setting.Value = vlist
        self.Settings[0].Plugin.Context.Write()        

    def Delete(self, *args):
        model, iter = self.Select.get_selected()
        if iter is not None:
            path = model.get_path(iter)
            if path is not None:
                row = path[0]
            else:
                return

            model.remove(iter)

            self._Delete(row)

    def _MakeEditDialog(self):
        dlg = gtk.Dialog(_("Edit"))
        vbox = gtk.VBox(spacing=TableX)
        vbox.props.border_width = 6
        dlg.vbox.pack_start(vbox, True, True)
        dlg.set_default_size(500, -1)
        dlg.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
        dlg.set_default_response(gtk.RESPONSE_CLOSE)

        group = gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)
        for widget in self.Widgets:
            vbox.pack_start(widget.EBox, False, False)
            group.add_widget(widget.Label)
        return dlg

    def Edit(self, widget):
        model, iter = self.Select.get_selected()
        if iter:
            path = model.get_path(iter)
            if path is not None:
                row = path[0]
            else:
                return

            self._Edit(row)

    def _Edit(self, row):
        if not self.EditDialog:
            self.EditDialog = self._MakeEditDialog()

        for widget in self.Widgets:
            widget.CurrentRow = row
            widget.Read()

        self.EditDialogOpen = True
        self.EditDialog.show_all()
        response = self.EditDialog.run()
        self.EditDialog.hide_all()
        self.EditDialogOpen = False

        if self.PageToBeRefreshed:
            self.PageToBeRefreshed[0].RefreshPage(self.PageToBeRefreshed[1],
                                                  self.PageToBeRefreshed[2])
            self.PageToBeRefreshed = None

        self.Read()

    def Move(self, widget, direction):
        model, iter = self.Select.get_selected()
        if iter is not None:
            path = model.get_path(iter)
            if path is not None:
                row = path[0]
            else:
                return
            if direction == 'up':
                dest = row - 1
            elif direction == 'down':
                dest = row + 1
            for widget in self.Widgets:
                widget.Swap(row, dest)

            self.Settings[0].Plugin.Context.Write()

            order = range(len(model))
            order.insert(dest, order.pop(row))
            model.reorder(order)

            self.SelectionChanged(self.Select)

    def SelectionChanged(self, selection):

        model, iter = selection.get_selected()
        for widget in (self.Buttons[gtk.STOCK_EDIT], self.Buttons[gtk.STOCK_DELETE],
                       self.PopupItems[gtk.STOCK_EDIT], self.PopupItems[gtk.STOCK_DELETE]):
            widget.set_sensitive(iter is not None)
            
        if iter is not None:
            path = model.get_path(iter)
            if path is not None:
                row = path[0]
                self.Buttons[gtk.STOCK_GO_UP].set_sensitive(row > 0)
                self.Buttons[gtk.STOCK_GO_DOWN].set_sensitive(row < (len(model) - 1))
        else:
            self.Buttons[gtk.STOCK_GO_UP].set_sensitive(False)
            self.Buttons[gtk.STOCK_GO_DOWN].set_sensitive(False)

    def ButtonPressEvent(self, treeview, event):
        if event.button == 3:
            pthinfo = treeview.get_path_at_pos(int(event.x), int(event.y))
            if pthinfo is not None:
                path, col, cellx, celly = pthinfo
                treeview.grab_focus()
                treeview.set_cursor(path, col, 0)
                self.Popup.popup(None, None, None, event.button, event.time)
            return True

    def KeyPressEvent(self, treeview, event):
        if gtk.gdk.keyval_name(event.keyval) == "Delete":
            model, iter = treeview.get_selection().get_selected()
            if iter is not None:
                path = model.get_path(iter)
                if path is not None:
                    row = path[0]
                    model.remove(iter)
                    self._Delete(row)
                    return True

    def ListInfo(self):
        types = []
        cols = []
        for i, (setting, widget) in enumerate(zip(self.Settings, self.Widgets)):   
            type, col = widget.GetColumn(i)
            types.append(type)
            cols.append(col)
        return types, cols

    def Activated(self, object, path, col):
        self._Edit(path[0])

    def _Read(self):        
        self.Store.clear()
        for values in zip(*[w.GetForRenderer() for w in self.Widgets]):
            self.Store.append(values)

    def OnDestroy(self, widget):
        for w in self.Widgets:
            w.EBox.destroy()

class ListSetting(BaseListSetting):

    def _Init(self):
        self.Settings = [self.Setting]
        BaseListSetting._Init(self)

class MultiListSetting(BaseListSetting):

    def _Init(self):
        self.EBox.set_tooltip_text(_("Multi-list settings. You can double-click a row to edit the values."))
        BaseListSetting._Init(self)

    def Filter(self, text, level=FilterAll):
        visible = False
        for setting in self.Widgets:
            if setting._Filter(text, level=level):
                visible = True
        self._SetHidden(visible)
        return visible

class EnumFlagsSetting(Setting):

    def _Init(self):
        frame = gtk.Frame(self.Setting.ShortDesc)
        table = gtk.Table()
        
        row = col = 0
        self.Checks = []
        sortedItems = sorted(self.Setting.Info[1][2].items(), key=EnumSettingKeyFunc)
        self.minVal = sortedItems[0][1]
        for key, value in sortedItems:
            box = gtk.CheckButton(key)
            self.Checks.append((key, box))
            table.attach(box, col, col+1, row, row+1, TableDef, TableDef, TableX, TableX)
            box.connect('toggled', self.Changed)
            col = col+1
            if col >= 3:
                col = 0
                row += 1

        vbox = gtk.VBox()
        vbox.pack_start(self.Reset, False, False)

        hbox = gtk.HBox()
        hbox.pack_start(table, True, True)
        hbox.pack_start(vbox, False, False)

        frame.add(hbox)
        self.Box.pack_start(frame, True, True)

    def _Read(self):
        for key, box in self.Checks:
            box.set_active(False)
        for setVal in self.Setting.Value:
            self.Checks[setVal-self.minVal][1].set_active(True)

    def _Changed(self):
        values = []
        for key, box in self.Checks:
            if box.get_active():
                values.append(self.Setting.Info[1][2][key])
        self.Setting.Value = values

    def _Filter(self, text, level=FilterAll):
        visible = Setting._Filter(self, text, level=level)
        if text is not None and not visible and level & FilterValue:
            visible = any(text in s.lower() for s in self.Setting.Info[1][2])
        return visible

class RestrictedStringFlagsSetting(Setting):

    def _Init(self):
        frame = gtk.Frame(self.Setting.ShortDesc)
        table = gtk.Table()
        
        row = col = 0
        self.Checks = []
        info = self.Setting.Info[1]
        self.ItemsByName = info[0]
        self.ItemsByValue = info[1]
        sortedItems = info[2]
        for key, value in sortedItems:
            box = gtk.CheckButton(key)
            self.Checks.append((key, box))
            table.attach(box, col, col+1, row, row+1, TableDef, TableDef, TableX, TableX)
            box.connect('toggled', self.Changed)
            col = col+1
            if col >= 3:
                col = 0
                row += 1

        vbox = gtk.VBox()
        vbox.pack_start(self.Reset, False, False)

        hbox = gtk.HBox()
        hbox.pack_start(table, True, True)
        hbox.pack_start(vbox, False, False)

        frame.add(hbox)
        self.Box.pack_start(frame, True, True)

    def _Read(self):
        for key, box in self.Checks:
            box.set_active(False)
        for setVal in self.Setting.Value:
            if self.ItemsByValue.has_key(setVal):
                self.Checks[self.ItemsByValue[setVal][1]][1].set_active(True)

    def _Changed(self):
        values = []
        for key, box in self.Checks:
            if box.get_active():
                values.append(self.ItemsByName[key])
        self.Setting.Value = values

    def _Filter(self, text, level=FilterAll):
        visible = Setting._Filter(self, text, level=level)
        if text is not None and not visible and level & FilterValue:
            visible = any(text in s.lower() for s in self.ItemsByName)
        return visible

class EditableActionSetting (StockSetting):

    def _Init (self, widget, action):
        StockSetting._Init(self)
        alignment = gtk.Alignment (0, 0.5)
        alignment.add (widget)

        self.Label.set_size_request(-1, -1)

        editButton = gtk.Button ()
        editButton.add (Image (name = gtk.STOCK_EDIT, type = ImageStock,
                               size = gtk.ICON_SIZE_BUTTON))
        editButton.set_tooltip_text(_("Edit %s" % self.Setting.ShortDesc))
        editButton.connect ("clicked", self.RunEditDialog)

        action = ActionImage (action)
        self.Box.pack_start (action, False, False)
        self.Box.reorder_child (action, 0)
        self.Box.pack_end (editButton, False, False)
        self.Box.pack_end(alignment, False, False)
        self.Widget = widget


    def RunEditDialog (self, widget):
        dlg = gtk.Dialog (_("Edit %s") % self.Setting.ShortDesc)
        dlg.set_position (gtk.WIN_POS_CENTER_ON_PARENT)
        dlg.set_transient_for (self.Widget.get_toplevel ())
        dlg.add_button (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        dlg.add_button (gtk.STOCK_OK, gtk.RESPONSE_OK).grab_default()
        dlg.set_default_response (gtk.RESPONSE_OK)
        
        entry = gtk.Entry (max = 200)
        entry.set_text (self.GetDialogText ())
        entry.connect ("activate", lambda *a: dlg.response (gtk.RESPONSE_OK))
        alignment = gtk.Alignment (0.5, 0.5, 1, 1)
        alignment.set_padding (10, 10, 10, 10)
        alignment.add (entry)

        entry.set_tooltip_text(self.Setting.LongDesc)
        dlg.vbox.pack_start (alignment)
        
        dlg.vbox.show_all ()
        ret = dlg.run ()
        dlg.destroy ()

        if ret != gtk.RESPONSE_OK:
            return

        self.HandleDialogText (entry.get_text ().strip ())

    def GetDialogText (self):
        self.PureVirtual ('GetDialogText')

    def HandleDialogText (self, text):
        self.PureVirtual ('HandleDialogText')

class KeySetting (EditableActionSetting):

    current = ""

    def _Init (self):

        self.Button = SizedButton (minWidth = 100)
        self.Button.connect ("clicked", self.RunKeySelector)
        self.SetButtonLabel ()
        
        EditableActionSetting._Init (self, self.Button, "keyboard")

    def DoReset (self, widget):
        conflict = KeyConflict (self.Setting, self.Setting.DefaultValue)
        if conflict.Resolve (GlobalUpdater):
            self.Setting.Reset ()
            self.Setting.Plugin.Context.Write ()
            self.Read ()

    def ReorderKeyString (self, accel):
        key, mods = gtk.accelerator_parse (accel)
        return gtk.accelerator_name (key, mods)

    def GetDialogText (self):
        return self.current

    def HandleDialogText (self, accel):
        name = self.ReorderKeyString (accel)
        if len (accel) != len (name):
            accel = protect_pango_markup (accel)
            ErrorDialog (self.Widget.get_toplevel (),
                         _("\"%s\" is not a valid shortcut") % accel)
            return
        self.BindingEdited (accel)

    def GetLabelText (self, text):
        if not len (text) or text.lower() == "disabled":
            text = _("Disabled")
        return text

    def SetButtonLabel (self):
        self.Button.set_label (self.GetLabelText (self.current))

    def RunKeySelector (self, widget):

        def ShowHideBox (button, box, dialog):
            if button.get_active ():
                box.show ()
            else:
                box.hide ()
                dialog.resize (1, 1)

        def HandleGrabberChanged (grabber, key, mods, label, selector):
            new = gtk.accelerator_name (key, mods)
            mods = ""
            for mod in KeyModifier:
                if "%s_L" % mod in new:
                    new = new.replace ("%s_L" % mod, "<%s>" % mod)
                if "%s_R" % mod in new:
                    new = new.replace ("%s_R" % mod, "<%s>" % mod)
                if "<%s>" % mod in new:
                    mods += "%s|" % mod
            mods.rstrip ("|")
            label.set_text (self.GetLabelText (new))
            selector.current = mods

        def HandleModifierAdded (selector, modifier, label):
            current = label.get_text ()
            if current == _("Disabled"):
                current = "<%s>" % modifier
            else:
                current = ("<%s>" % modifier) + current
            label.set_text (self.ReorderKeyString (current))

        def HandleModifierRemoved (selector, modifier, label):
            current = label.get_text ()
            if "<%s>" % modifier in current:
                new = current.replace ("<%s>" % modifier, "")
            elif "%s_L" % modifier in current:
                new = current.replace ("%s_L" % modifier, "")
            elif "%s_R" % modifier in current:
                new = current.replace ("%s_R" % modifier, "")
            label.set_text (self.GetLabelText (new))

        dlg = gtk.Dialog (_("Edit %s") % self.Setting.ShortDesc)
        dlg.set_position (gtk.WIN_POS_CENTER_ALWAYS)
        dlg.set_transient_for (self.Widget.get_toplevel ())
        dlg.set_icon (self.Widget.get_toplevel ().get_icon ())
        dlg.set_modal (True)
        dlg.add_button (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        dlg.add_button (gtk.STOCK_OK, gtk.RESPONSE_OK).grab_default ()
        dlg.set_default_response (gtk.RESPONSE_OK)

        mainBox = gtk.VBox ()
        alignment = gtk.Alignment ()
        alignment.set_padding (10, 10, 10, 10)
        alignment.add (mainBox)
        dlg.vbox.pack_start (alignment)

        checkButton = gtk.CheckButton (_("Enabled"))
        active = len (self.current) \
                 and self.current.lower () not in ("disabled", "none")
        checkButton.set_active (active)
        checkButton.set_tooltip_text(self.Setting.LongDesc)
        mainBox.pack_start (checkButton)

        box = gtk.VBox ()
        checkButton.connect ("toggled", ShowHideBox, box, dlg)
        mainBox.pack_start (box)

        currentMods = ""
        for mod in KeyModifier:
            if "<%s>" % mod in self.current:
                currentMods += "%s|" % mod
        currentMods.rstrip ("|")
        modifierSelector = ModifierSelector (currentMods)
        modifierSelector.set_tooltip_text (self.Setting.LongDesc)
        alignment = gtk.Alignment (0.5)
        alignment.add (modifierSelector)
        box.pack_start (alignment)

        key, mods = gtk.accelerator_parse (self.current)
        grabber = KeyGrabber (key = key, mods = mods,
                              label = _("Grab key combination"))
        grabber.set_tooltip_text (self.Setting.LongDesc)
        box.pack_start (grabber)

        label = gtk.Label (self.current)
        label.set_tooltip_text (self.Setting.LongDesc)
        alignment = gtk.Alignment (0.5, 0.5)
        alignment.set_padding (15, 0, 0, 0)
        alignment.add (label)
        box.pack_start (alignment)

        modifierSelector.connect ("added", HandleModifierAdded, label)
        modifierSelector.connect ("removed", HandleModifierRemoved, label)
        grabber.connect ("changed", HandleGrabberChanged, label,
                         modifierSelector)
        grabber.connect ("current-changed", HandleGrabberChanged, label,
                         modifierSelector)

        dlg.vbox.show_all ()
        ShowHideBox (checkButton, box, dlg)
        ret = dlg.run ()
        dlg.destroy ()

        if ret != gtk.RESPONSE_OK:
            return

        if not checkButton.get_active ():
            self.BindingEdited ("Disabled")
            return

        new = label.get_text ()

        new = self.ReorderKeyString (new)

        self.BindingEdited (new)

    def BindingEdited (self, accel):
        '''Binding edited callback'''
        # Update & save binding
        conflict = KeyConflict (self.Setting, accel)
        if conflict.Resolve (GlobalUpdater):
            self.current = accel
            self.Changed ()
        self.SetButtonLabel ()

    def _Read (self):
        self.current = self.Get()
        self.SetButtonLabel ()

    def _Changed (self):
        self.Set(self.current)

class ButtonSetting (EditableActionSetting):

    current = ""

    def _Init (self):

        self.Button = SizedButton (minWidth = 100)
        self.Button.connect ("clicked", self.RunButtonSelector)
        self.Button.set_tooltip_text(self.Setting.LongDesc)
        self.SetButtonLabel ()
        
        EditableActionSetting._Init (self, self.Button, "button")

    def DoReset (self, widget):
        conflict = ButtonConflict (self.Setting, self.Setting.DefaultValue)
        if conflict.Resolve (GlobalUpdater):
            self.Setting.Reset ()
            self.Setting.Plugin.Context.Write ()
            self.Read ()

    def ReorderButtonString (self, old):
        new = ""
        edges = map (lambda e: "%sEdge" % e, Edges)
        for s in edges + KeyModifier:
            if "<%s>" % s in old:
                new += "<%s>" % s
        for i in range (99, 0, -1):
            if "Button%d" % i in old:
                new += "Button%d" % i
                break
        return new

    def GetDialogText (self):
        return self.current

    def HandleDialogText (self, button):
        def ShowErrorDialog (button):
            button = protect_pango_markup (button)
            ErrorDialog (self.Widget.get_toplevel (),
                         _("\"%s\" is not a valid button") % button)
        if button.lower ().strip () in ("", "disabled", "none"):
            self.ButtonEdited ("Disabled")
            return
        new = self.ReorderButtonString (button)
        if len (button) != len (new):
            ShowErrorDialog (button)
            return
        self.ButtonEdited (new)

    def SetButtonLabel (self):
        label = self.current
        if not len (self.current) or self.current.lower() == "disabled":
            label = _("Disabled")
        self.Button.set_label (label)

    def RunButtonSelector (self, widget):
        def ShowHideBox (button, box, dialog):
            if button.get_active ():
                box.show ()
            else:
                box.hide ()
                dialog.resize (1, 1)
        dlg = gtk.Dialog (_("Edit %s") % self.Setting.ShortDesc)
        dlg.set_position (gtk.WIN_POS_CENTER_ALWAYS)
        dlg.set_transient_for (self.Widget.get_toplevel ())
        dlg.set_modal (True)
        dlg.add_button (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        dlg.add_button (gtk.STOCK_OK, gtk.RESPONSE_OK).grab_default ()
        dlg.set_default_response (gtk.RESPONSE_OK)

        mainBox = gtk.VBox ()
        alignment = gtk.Alignment ()
        alignment.set_padding (10, 10, 10, 10)
        alignment.add (mainBox)
        dlg.vbox.pack_start (alignment)

        checkButton = gtk.CheckButton (_("Enabled"))
        active = len (self.current) \
                 and self.current.lower () not in ("disabled", "none")
        checkButton.set_active (active)
        checkButton.set_tooltip_text (self.Setting.LongDesc)
        mainBox.pack_start (checkButton)

        box = gtk.VBox ()
        checkButton.connect ("toggled", ShowHideBox, box, dlg)
        mainBox.pack_start (box)

        currentEdges = ""
        for edge in Edges:
            if "<%sEdge>" % edge in self.current:
                currentEdges += "%s|" % edge
        currentEdges.rstrip ("|")
        edgeSelector = SingleEdgeSelector (currentEdges)
        edgeSelector.set_tooltip_text(self.Setting.LongDesc)
        box.pack_start (edgeSelector)

        currentMods = ""
        for mod in KeyModifier:
            if "<%s>" % mod in self.current:
                currentMods += "%s|" % mod
        currentMods.rstrip ("|")
        modifierSelector = ModifierSelector (currentMods)
        modifierSelector.set_tooltip_text(self.Setting.LongDesc)
        box.pack_start (modifierSelector)

        buttonCombo = gtk.combo_box_new_text ()
        currentButton = 1
        for i in range (99, 0, -1):
            if "Button%d" % i in self.current:
                currentButton = i
                break
        maxButton = 9
        for i in range (1, maxButton + 1):
            button = "Button%d" % i
            buttonCombo.append_text (button)
        if currentButton > maxButton:
            buttonCombo.append_text ("Button%d" % currentButton)
            buttonCombo.set_active (maxButton)
        else:
            buttonCombo.set_active (currentButton - 1)
        buttonCombo.set_tooltip_text(self.Setting.LongDesc)
        box.pack_start (buttonCombo)

        dlg.vbox.show_all ()
        ShowHideBox (checkButton, box, dlg)
        ret = dlg.run ()
        dlg.destroy ()

        if ret != gtk.RESPONSE_OK:
            return

        if not checkButton.get_active ():
            self.ButtonEdited ("Disabled")
            return

        edges = edgeSelector.current
        modifiers = modifierSelector.current
        button = buttonCombo.get_active_text ()

        edges = edges.split ("|")
        if len (edges):
            edges = "<%sEdge>" % "Edge><".join (edges)
        else: edges = ""

        modifiers = modifiers.split ("|")
        if len (modifiers):
            modifiers = "<%s>" % "><".join (modifiers)
        else: modifiers = ""

        button = "%s%s%s" % (edges, modifiers, button)
        button = self.ReorderButtonString (button)

        self.ButtonEdited (button)

    def ButtonEdited (self, button):
        '''Button edited callback'''
        if button == "Button1":
            warning = WarningDialog (self.Widget.get_toplevel (),
                                     _("Using Button1 without modifiers can \
prevent any left click and thus break your configuration. Do you really want \
to set \"%s\" button to Button1 ?") % self.Setting.ShortDesc)
            response = warning.run ()
            if response != gtk.RESPONSE_YES:
                return
        conflict = ButtonConflict (self.Setting, button)
        if conflict.Resolve (GlobalUpdater):
            self.current = button
            self.Changed ()
        self.SetButtonLabel ()

    def _Read (self):
        self.current = self.Get()
        self.SetButtonLabel ()

    def _Changed (self):
        self.Set(self.current)

class EdgeSetting (EditableActionSetting):

    current = ""

    def _Init (self):

        self.Button = SizedButton (minWidth = 100)
        self.Button.connect ("clicked", self.RunEdgeSelector)
        self.Button.set_tooltip_text(self.Setting.LongDesc)
        self.SetButtonLabel ()

        EditableActionSetting._Init (self, self.Button, "edges")

    def DoReset (self, widget):
        conflict = EdgeConflict (self.Setting, self.Setting.DefaultValue)
        if conflict.Resolve (GlobalUpdater):
            self.Setting.Reset ()
            self.Setting.Plugin.Context.Write ()
            self.Read ()

    def GetDialogText (self):
        return self.current

    def HandleDialogText (self, mask):
        edges = mask.split ("|")
        valid = True
        for edge in edges:
            if edge not in Edges:
                valid = False
                break
        if not valid:
            mask = protect_pango_markup (mask)
            ErrorDialog (self.Widget.get_toplevel (),
                         _("\"%s\" is not a valid edge mask") % mask)
            return
        self.EdgeEdited ("|".join (edges))

    def SetButtonLabel (self):
        label = self.current
        if len (self.current):
            edges = self.current.split ("|")
            edges = map (lambda s: _(s), edges)
            label = ", ".join (edges)
        else:
            label = _("None")
        self.Button.set_label (label)

    def RunEdgeSelector (self, widget):
        dlg = gtk.Dialog (_("Edit %s") % self.Setting.ShortDesc)
        dlg.set_position (gtk.WIN_POS_CENTER_ON_PARENT)
        dlg.set_transient_for (self.Widget.get_toplevel ())
        dlg.set_modal (True)
        dlg.add_button (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        dlg.add_button (gtk.STOCK_OK, gtk.RESPONSE_OK).grab_default()
        dlg.set_default_response (gtk.RESPONSE_OK)
        
        selector = SingleEdgeSelector (self.current)
        alignment = gtk.Alignment ()
        alignment.set_padding (10, 10, 10, 10)
        alignment.add (selector)

        selector.set_tooltip_text (self.Setting.LongDesc)
        dlg.vbox.pack_start (alignment)
        
        dlg.vbox.show_all ()
        ret = dlg.run ()
        dlg.destroy ()

        if ret != gtk.RESPONSE_OK:
            return

        self.EdgeEdited (selector.current)

    def EdgeEdited (self, edge):
        '''Edge edited callback'''
        conflict = EdgeConflict (self.Setting, edge)
        if conflict.Resolve (GlobalUpdater):
            self.current = edge
            self.Changed ()
        self.SetButtonLabel ()

    def _Read (self):
        self.current = self.Get()
        self.SetButtonLabel ()

    def _Changed (self):
        self.Set(self.current)
        self.SetButtonLabel ()

class BellSetting (BoolSetting):

    def _Init (self):
        BoolSetting._Init (self)
        bell = ActionImage ("bell")
        self.Box.pack_start (bell, False, False)
        self.Box.reorder_child (bell, 0)

def MakeStringSetting (setting, List=False):

    if setting.Hints:
        if "file" in setting.Hints:
            if "image" in setting.Hints:
                return FileStringSetting (setting, isImage=True, List=List)
            else:
                return FileStringSetting (setting, List=List)
        elif "directory" in setting.Hints:
            return FileStringSetting (setting, isDirectory=True, List=List)
        else:
            return StringSetting (setting, List=List)
    elif (List and setting.Info[1][2]) or \
        (not List and setting.Info[2]):
        return RestrictedStringSetting (setting, List=List)
    else:
        return StringSetting (setting, List=List)

def MakeIntSetting (setting, List=False):

    if List:
        info = setting.Info[1][2]
    else:
        info = setting.Info[2]

    if info:
        return EnumSetting (setting, List=List)
    else:
        return IntSetting (setting, List=List)

def MakeListSetting (setting, List=False):

    if List:
        raise TypeError ("Lists of lists are not supported")

    if setting.Info[0] == "Int" and setting.Info[1][2]:
        return EnumFlagsSetting (setting)
    elif setting.Info[0] == "String" and setting.Info[1][2]:
        return RestrictedStringFlagsSetting (setting)
    else:
        return ListSetting (setting)
      
SettingTypeDict = {
    "Match": MatchSetting,
    "String": MakeStringSetting,
    "Bool": BoolSetting,
    "Float": FloatSetting,
    "Int": MakeIntSetting,
    "Color": ColorSetting,
    "List": MakeListSetting,
    "Key": KeySetting,
    "Button": ButtonSetting,
    "Edge": EdgeSetting,
    "Bell": BellSetting,
}

def MakeSetting(setting, List=False):

    if List:
        type = setting.Info[0]
    else:
        type = setting.Type

    stype = SettingTypeDict.get(type, None)
    if not stype:
        return

    return stype(setting, List=List)

class SubGroupArea(object):
    def __init__(self, name, subGroup):
        self.MySettings = []
        self.SubGroup = subGroup
        self.Name = name
        settings = sorted(GetSettings(subGroup), key=SettingKeyFunc)
        if not name:
            self.Child = self.Widget = gtk.VBox()
        else:
            self.Widget = gtk.Frame()
            self.Expander = gtk.Expander(name)
            self.Widget.add(self.Expander)
            self.Expander.set_expanded(False)
            self.Child = gtk.VBox()
            self.Expander.add(self.Child)

        self.Child.set_spacing(TableX)
        self.Child.set_border_width(TableX)

        # create a special widget for list subGroups
        if len(settings) > 1 and HasOnlyType(settings, 'List'):
            multiList = MultiListSetting(Settings=settings)
            multiList.Read()
            self.Child.pack_start(multiList.EBox, True, True)
            self.MySettings.append(multiList)
            self.Empty = False
            if name:
                self.Expander.set_expanded(True)

            return # exit earlier to avoid unneeded logic's
        
        self.Empty = True
        for setting in settings:
            if not (setting.Plugin.Name == 'core' and setting.Name == 'active_plugins'):
                setting = MakeSetting(setting)
                if setting is not None:
                    setting.Read()
                    self.Child.pack_start(setting.EBox, True, True)
                    self.MySettings.append(setting)
                    self.Empty = False

        if name and len(settings) < 4: # ahi hay magic numbers!
            self.Expander.set_expanded(True)

    def Filter(self, text, level=FilterAll):
        empty = True
        count = 0
        for setting in self.MySettings:
            if setting.Filter(text, level=level):
                empty = False
                count += 1

        if self.Name:
            self.Expander.set_expanded(count < 4)

        self.Widget.props.no_show_all = empty

        if empty:
            self.Widget.hide()
        else:
            self.Widget.show()

        return not empty

