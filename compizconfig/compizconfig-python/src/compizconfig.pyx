'''
This program is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

Authors:
    Quinn Storm (quinn@beryl-project.org)
    Patrick Niklaus (marex@opencompositing.org)
    Guillaume Seguin (guillaume@segu.in)
Copyright (C) 2007 Quinn Storm
'''

import operator
StringSettingKeyFunc = operator.itemgetter (1)

ctypedef unsigned int Bool

cdef enum CCSSettingType:
    TypeBool
    TypeInt
    TypeFloat
    TypeString
    TypeColor
    TypeAction
    TypeKey
    TypeButton
    TypeEdge
    TypeBell
    TypeMatch
    TypeList
    TypeNum

cdef enum CCSPluginConflictType:
    # produced on plugin activation
    ConflictRequiresPlugin,
    ConflictRequiresFeature,
    ConflictFeature,
    ConflictPlugin,
    # produced on plugin deactivation
    ConflictFeatureNeeded,
    ConflictPluginNeeded,
    ConflictPluginError

SettingTypeString = [
    "Bool",
    "Int",
    "Float",
    "String",
    "Color",
    "Action",
    "Key",
    "Button",
    "Edge",
    "Bell",
    "Match",
    "List",
    "Invalid"
]

ConflictTypeString = [
    "RequiresPlugin", #A
    "RequiresFeature", #A
    "ConflictFeature", #A
    "ConflictPlugin", #A
    "FeatureNeeded", #D
    "PluginNeeded", #D
    "PluginError"
]

cdef struct CCSList:
    void *    data
    CCSList * next

ctypedef CCSList CCSSettingList
ctypedef CCSList CCSPluginList
ctypedef CCSList CCSStringList
ctypedef CCSList CCSGroupList
ctypedef CCSList CCSSubGroupList
ctypedef CCSList CCSPluginConflictList
ctypedef CCSList CCSSettingValueList
ctypedef CCSList CCSBackendInfoList
ctypedef CCSList CCSIntDescList
ctypedef CCSList CCSStrRestrictionList
ctypedef CCSList CCSStrExtensionList

cdef struct CCSBackendInfo:
    char *    name
    char *    shortDesc
    char *    longDesc
    Bool      integrationSupport
    Bool      profileSupport

cdef struct CCSSettingKeyValue:
    int          keysym
    unsigned int keyModMask

cdef struct CCSSettingButtonValue:
    int          button
    unsigned int buttonModMask
    int          edgeMask

cdef struct CCSSettingColorValueColor:
    unsigned short red
    unsigned short green
    unsigned short blue
    unsigned short alpha

cdef union CCSSettingColorValue:
    CCSSettingColorValueColor color
    unsigned short            array[4]

cdef union CCSSettingValueUnion:
    Bool                  asBool
    int                   asInt
    float                 asFloat
    char *                asString
    char *                asMatch
    CCSSettingColorValue  asColor
    CCSSettingValueList * asList
    CCSSettingKeyValue    asKey
    CCSSettingButtonValue asButton
    unsigned int          asEdge
    Bool                  asBell

cdef struct CCSIntDesc:
    int    value
    char * name

cdef struct CCSStrRestriction:
    char * value
    char * name

cdef struct CCSSettingIntInfo:
    int              min
    int              max
    CCSIntDescList * desc

cdef struct CCSSettingFloatInfo:
    float min
    float max
    float precision

cdef struct CCSSettingStringInfo:
    CCSStrRestrictionList * restriction
    int                     sortStartsAt
    Bool                    extensible

cdef struct CCSSettingListInfo:
    CCSSettingType listType
    void *         listInfo # actually CCSSettingInfo *, works around pyrex

cdef struct CCSSettingActionInfo:
    Bool internal

cdef union CCSSettingInfo:
    CCSSettingIntInfo    forInt
    CCSSettingFloatInfo  forFloat
    CCSSettingStringInfo forString
    CCSSettingListInfo   forList
    CCSSettingActionInfo forAction

cdef struct CCSSettingValue:
    CCSSettingValueUnion value
    void *               parent
    Bool                 isListChild

cdef struct CCSGroup:
    char *            name
    CCSSubGroupList * subGroups

cdef struct CCSSubGroup:
    char *           name
    CCSSettingList * settings

cdef struct CCSPluginCategory:
    char *          name
    char *          shortDesc
    char *          longDesc
    CCSStringList * plugins

cdef struct CCSContext:
    CCSPluginList *     plugins
    CCSPluginCategory * categories

    void * priv
    void * ccsPrivate

    CCSSettingList * changedSettings

    unsigned int * screens
    unsigned int   numScreens

cdef struct CCSPlugin

cdef struct CCSSetting:
    char * name
    char * shortDesc
    char * longDesc

    CCSSettingType type

    Bool         isScreen
    unsigned int screenNum

    CCSSettingInfo info
    char *         group
    char *         subGroup
    char *         hints

    CCSSettingValue   defaultValue
    CCSSettingValue * value
    Bool              isDefault

    CCSPlugin * parent
    void *      priv

cdef struct CCSStrExtension:
    char *                  basePlugin
    CCSSettingList *        baseSettings
    CCSStrRestrictionList * restriction
    Bool                    isScreen

cdef struct CCSPlugin:
    char * name
    char * shortDesc
    char * longDesc
    char * hints
    char * category

    CCSStringList * loadAfter
    CCSStringList * loadBefore
    CCSStringList * requiresPlugin
    CCSStringList * conflictPlugin
    CCSStringList * conflictFeature
    CCSStringList * providesFeature
    CCSStringList * requiresFeature

    void *       priv
    CCSContext * context
    void *       ccsPrivate

cdef struct CCSPluginConflict:
    char *                value
    CCSPluginConflictType type
    CCSPluginList *       plugins

'''Context functions'''
cdef extern void ccsSetBasicMetadata (Bool value)
cdef extern CCSContext * ccsContextNew (unsigned int * screens,
                                        unsigned int numScreens)
cdef extern CCSContext * ccsEmptyContextNew (unsigned int * screens,
                                             unsigned int   numScreens)
cdef extern void ccsContextDestroy (CCSContext * context)

'''Plugin functions'''
cdef extern Bool ccsLoadPlugin (CCSContext * context, char * name)
cdef extern CCSPlugin * ccsFindPlugin (CCSContext * context, char * name)
cdef extern CCSSetting * ccsFindSetting (CCSPlugin * plugin,
                                         char *      name,
                                         Bool        isScreen,
                                         int         screenNum)
cdef extern CCSSettingList * ccsGetPluginSettings (CCSPlugin * plugin)
cdef extern CCSGroupList * ccsGetPluginGroups (CCSPlugin * plugin)

'''Action => String'''
cdef extern char * ccsModifiersToString (unsigned int modMask)
cdef extern char * ccsEdgesToString (unsigned int edge)
cdef extern char * ccsEdgesToModString (unsigned int edge)
cdef extern char * ccsKeyBindingToString (CCSSettingKeyValue *key)
cdef extern char * ccsButtonBindingToString (CCSSettingButtonValue *button)

'''String utils'''
cdef extern from 'string.h':
    ctypedef int size_t
    cdef extern char * strdup (char * s)
    cdef extern void memset (void * s, int c, size_t n)
    cdef extern void free (void * f)
    cdef extern void * malloc (size_t s)

'''String => Action'''
cdef extern unsigned int ccsStringToModifiers (char *binding)
cdef extern unsigned int ccsStringToEdges (char *edge)
cdef extern unsigned int ccsModStringToEdges (char *edge)
cdef extern Bool ccsStringToKeyBinding (char *               binding,
                                        CCSSettingKeyValue * key)
cdef extern Bool ccsStringToButtonBinding (char *                  binding,
                                           CCSSettingButtonValue * button)

'''General settings handling'''
cdef extern Bool ccsSetValue (CCSSetting * setting,
                  CCSSettingValue * value)
cdef extern void ccsFreeSettingValue (CCSSettingValue * value)
cdef extern CCSSettingValueList * ccsSettingValueListAppend (
                                        CCSSettingValueList * l,
                                        CCSSettingValue *     v)
cdef extern CCSSettingList *ccsSettingListFree (CCSSettingList * list,
                                                Bool             freeObj)

'''Profiles'''
cdef extern CCSStringList * ccsGetExistingProfiles (CCSContext * context)
cdef extern void ccsDeleteProfile (CCSContext * context, char * name)
cdef extern void ccsSetProfile (CCSContext * context, char * name)
cdef extern char* ccsGetProfile (CCSContext * context)

'''Backends'''
cdef extern CCSBackendInfoList * ccsGetExistingBackends ()
cdef extern Bool ccsSetBackend (CCSContext * context, char * name)
cdef extern char* ccsGetBackend (CCSContext * context)

'''Sorting'''
cdef extern void ccsSetPluginListAutoSort (CCSContext *context, Bool value)
cdef extern Bool ccsGetPluginListAutoSort (CCSContext *context)

'''Integration'''
cdef extern void ccsSetIntegrationEnabled (CCSContext * context, Bool value)
cdef extern Bool ccsGetIntegrationEnabled (CCSContext * context)

'''IO handling'''
cdef extern void ccsReadSettings (CCSContext * c)
cdef extern void ccsWriteSettings (CCSContext * c)
cdef extern void ccsWriteChangedSettings (CCSContext * c)
cdef extern void ccsResetToDefault (CCSSetting * s)

'''Event loop'''
ProcessEventsNoGlibMainLoopMask = (1 << 0)
cdef extern void ccsProcessEvents (CCSContext * context, unsigned int flags)

'''Import/export'''
cdef extern Bool ccsExportToFile (CCSContext * context, char * fileName, Bool skipDefaults)
cdef extern Bool ccsImportFromFile (CCSContext * context,
                                    char *       fileName,
                                    Bool         overwrite)

'''Misc. Plugin/Setting utils'''
cdef extern Bool ccsSettingIsReadOnly (CCSSetting * setting)
cdef extern Bool ccsSettingIsIntegrated (CCSSetting * setting)

cdef extern void ccsPluginConflictListFree (CCSPluginConflictList * l,
                                            Bool                    freeObj)
cdef extern CCSPluginConflictList * ccsCanEnablePlugin (CCSContext * c,
                                                        CCSPlugin *  p)
cdef extern CCSPluginConflictList * ccsCanDisablePlugin (CCSContext * c,
                                                         CCSPlugin *  p)

cdef extern Bool ccsPluginSetActive (CCSPlugin * p, Bool v)
cdef extern Bool ccsPluginIsActive (CCSContext * c, char * n)

cdef extern CCSStrExtensionList * ccsGetPluginStrExtensions (CCSPlugin * plugin)

cdef class Context
cdef class Plugin
cdef class Setting

cdef CCSSettingType GetType (CCSSettingValue * value):
    if value.isListChild:
        return (<CCSSetting *> value.parent).info.forList.listType
    else:
        return (<CCSSetting *> value.parent).type

cdef CCSStringList * ListToStringList (object list):
    if len (list) <= 0:
        return NULL

    cdef CCSStringList * listStart
    cdef CCSStringList * stringList
    cdef CCSStringList * prev
    listStart = <CCSStringList *> malloc (sizeof (CCSStringList))
    listStart.data = <char *> strdup (list[0])
    listStart.next = NULL
    prev = listStart
    
    for l in list[1:]:
        stringList = <CCSStringList *> malloc (sizeof (CCSStringList))
        stringList.data = <char *> strdup (l)
        stringList.next = NULL
        prev.next = stringList
        prev = stringList
    
    return listStart
    
cdef object StringListToList (CCSList * stringList):
    list = []
    while stringList:
        item = <char *> stringList.data
        list.append (item)
        stringList = stringList.next
    return list

cdef CCSSettingList * ListToSettingList (object list):
    if len (list) <= 0:
        return NULL

    cdef CCSSettingList * listStart
    cdef CCSSettingList * settingList
    cdef CCSSettingList * prev
    cdef Setting setting

    listStart = <CCSSettingList *> malloc (sizeof (CCSSettingList))
    setting = <Setting> list[0]
    listStart.data = <CCSSetting *> setting.ccsSetting
    listStart.next = NULL
    prev = listStart
    
    for l in list[1:]:
        settingList = <CCSSettingList *> malloc (sizeof (CCSSettingList))
        setting = <Setting> l
        settingList.data = <CCSSetting *> setting.ccsSetting
        settingList.next = NULL
        prev.next = settingList
        prev = settingList
    
    return listStart

cdef object SettingListToList (Context context, CCSList * settingList):
    cdef CCSSetting * ccsSetting
    list = []
    
    while settingList:
        ccsSetting = <CCSSetting *> settingList.data
        setting = None
        plugin = context.Plugins[ccsSetting.parent.name]
        if ccsSetting.isScreen:
            setting = plugin.Screens[ccsSetting.screenNum][ccsSetting.name]
        else:
            setting = plugin.Display[ccsSetting.name]
        list.append (setting)
        settingList = settingList.next
    
    return list

cdef object IntDescListToDict (CCSIntDescList * intDescList):
    cdef CCSIntDesc * desc
    dict = {}
    while intDescList:
        desc = <CCSIntDesc *> intDescList.data
        dict[desc.name] = desc.value
        intDescList = intDescList.next
    return dict

cdef object StrRestrictionListToDict (CCSStrRestrictionList * restrictionList,
                                      object initialDict):
    cdef CCSStrRestriction * restriction
    dict = initialDict
    listOfAddedItems = []
    while restrictionList:
        restriction = <CCSStrRestriction *> restrictionList.data
        dict[restriction.name] = restriction.value
        listOfAddedItems.append ((restriction.name, restriction.value))
        restrictionList = restrictionList.next
    return (dict, listOfAddedItems)

cdef CCSSettingValue * EncodeValue (object       data,
                                    CCSSetting * setting,
                                    Bool         isListChild):
    cdef CCSSettingValue * bv
    cdef CCSSettingType t
    cdef CCSList * l
    bv = <CCSSettingValue *> malloc (sizeof (CCSSettingValue))
    memset (bv, 0, sizeof (CCSSettingValue))
    bv.isListChild = isListChild
    bv.parent = setting
    if isListChild:
        t = setting.info.forList.listType
    else:
        t = setting.type
    if t == TypeString:
        bv.value.asString = strdup (data)
    elif t == TypeMatch:
        bv.value.asMatch = strdup (data)
    elif t == TypeInt:
        bv.value.asInt = data
    elif t == TypeFloat:
        bv.value.asFloat = data
    elif t == TypeBool:
        if data:
            bv.value.asBool = 1
        else:
            bv.value.asBool = 0
    elif t == TypeColor:
        bv.value.asColor.color.red = data[0]
        bv.value.asColor.color.green = data[1]
        bv.value.asColor.color.blue = data[2]
        bv.value.asColor.color.alpha = data[3]
    elif t == TypeKey:
        ccsStringToKeyBinding (data, &bv.value.asKey)
    elif t == TypeButton:
        ccsStringToButtonBinding (data, &bv.value.asButton)
    elif t == TypeEdge:
        bv.value.asEdge = ccsStringToEdges (data)
    elif t == TypeBell:
        if (data):
            bv.value.asBell = 1
        else:
            bv.value.asBell = 0
    elif t == TypeList:
        l = NULL
        for item in data:
            l = ccsSettingValueListAppend (l, EncodeValue (item, setting, 1))
        bv.value.asList = l
    return bv

cdef object DecodeValue (CCSSettingValue * value):
    cdef CCSSettingType t
    cdef char * s
    cdef CCSList * l
    cdef object cs
    cdef object ks
    cdef object bs
    cdef object es
    cdef object eb
    t = GetType (value)
    if t == TypeString:
        return value.value.asString
    elif t == TypeMatch:
        return value.value.asMatch
    elif t == TypeBool:
        if value.value.asBool:
            return True
        return False
    elif t == TypeInt:
        return value.value.asInt
    elif t == TypeFloat:
        return value.value.asFloat
    elif t == TypeColor:
        return [value.value.asColor.color.red,
                value.value.asColor.color.green,
                value.value.asColor.color.blue,
                value.value.asColor.color.alpha]
    elif t == TypeKey:
        s = ccsKeyBindingToString (&value.value.asKey)
        if s != NULL:
            ks = s
            free (s)
        else:
            ks = "None"
        return ks
    elif t == TypeButton:
        s = ccsButtonBindingToString (&value.value.asButton)
        if s != NULL:
            bs = s
            free (s)
        else:
            bs = "None"
        if bs == "Button0":
            bs = "None"
        return bs
    elif t == TypeEdge:
        s = ccsEdgesToString (value.value.asEdge)
        if s != NULL:
            es = s
            free (s)
        else:
            es = "None"
        return es
    elif t == TypeBell:
        bb = False
        if value.value.asBell:
            bb = True
        return bb
    elif t == TypeList:
        lret = []
        l = value.value.asList
        while l != NULL:
            lret.append (DecodeValue (<CCSSettingValue *> l.data))
            l = l.next
        return lret
    return "Unhandled"

cdef class Setting:
    cdef CCSSetting * ccsSetting
    cdef object info
    cdef Plugin plugin
    cdef object extendedStrRestrictions
    cdef object baseStrRestrictions

    def __cinit__ (self, Plugin plugin, name, isScreen, screenNum = 0):
        cdef CCSSettingType t
        cdef CCSSettingInfo * i

        self.ccsSetting = ccsFindSetting (plugin.ccsPlugin,
                                          name, isScreen, screenNum)
        self.plugin = plugin

        self.extendedStrRestrictions = None
        self.baseStrRestrictions = None
        info = ()
        t = self.ccsSetting.type
        i = &self.ccsSetting.info
        if t == TypeList:
            t = self.ccsSetting.info.forList.listType
            i = <CCSSettingInfo *> self.ccsSetting.info.forList.listInfo
        if t == TypeInt:
            desc = IntDescListToDict (i.forInt.desc)
            info = (i.forInt.min, i.forInt.max, desc)
        elif t == TypeFloat:
            info = (i.forFloat.min, i.forFloat.max,
                    i.forFloat.precision)
        elif t == TypeString:
            # info is filled later in Plugin.SortSingleStringSetting
            info = ({}, {}, [])
            self.baseStrRestrictions = []
            self.extendedStrRestrictions = {}
        elif t in (TypeKey, TypeButton, TypeEdge, TypeBell):
            info = (bool (i.forAction.internal),)
        if self.ccsSetting.type == TypeList:
            info = (SettingTypeString[t], info)
        self.info = info
    
    def Reset (self):
        ccsResetToDefault (self.ccsSetting)

    property Plugin:
        def __get__ (self):
            return self.plugin

    property Name:
        def __get__ (self):
            return self.ccsSetting.name

    property ShortDesc:
        def __get__ (self):
            return self.ccsSetting.shortDesc

    property LongDesc:
        def __get__ (self):
            return self.ccsSetting.longDesc

    property Group:
        def __get__ (self):
            return self.ccsSetting.group

    property SubGroup:
        def __get__ (self):
            return self.ccsSetting.subGroup

    property Type:
        def __get__ (self):
            return SettingTypeString[self.ccsSetting.type]

    property Info:
        def __get__ (self):
            return self.info

    property Hints:
        def __get__ (self):
            if self.ccsSetting.hints == '':
                return []
            else:
                return str (self.ccsSetting.hints).split (";")[:-1]

    property IsDefault:
        def __get__ (self):
            if self.ccsSetting.isDefault:
                return True
            return False

    property DefaultValue:
        def __get__ (self):
            return DecodeValue (&self.ccsSetting.defaultValue)

    property Value:
        def __get__ (self):
            return DecodeValue (self.ccsSetting.value)
        def __set__ (self, value):
            cdef CCSSettingValue * sv
            sv = EncodeValue (value, self.ccsSetting, 0)
            ccsSetValue (self.ccsSetting, sv)
            ccsFreeSettingValue (sv)

    property Integrated:
        def __get__ (self):
            return bool (ccsSettingIsIntegrated (self.ccsSetting))

    property ReadOnly:
        def __get__ (self):
            return bool (ccsSettingIsReadOnly (self.ccsSetting))

cdef class SSGroup:
    cdef object display
    cdef object screens

    def __cinit__ (self, disp, screen):
        self.display = disp
        self.screens = screen

    property Display:
        def __get__ (self):
            return self.display
        def __set__ (self, value):
            self.display = value

    property Screens:
        def __get__ (self):
            return self.screens
        def __set__ (self, value):
            self.screens = value

cdef class Plugin:
    cdef CCSPlugin * ccsPlugin
    cdef Context context
    cdef object screens
    cdef object display
    cdef object groups
    cdef object loaded
    cdef object ranking
    cdef object hasExtendedString
    
    def __cinit__ (self, Context context, name):
        self.ccsPlugin = ccsFindPlugin (context.ccsContext, name)
        self.context = context
        self.screens = []
        self.display = {}
        self.groups = {}
        self.loaded = False
        self.ranking = {}
        self.hasExtendedString = False

        for n in range (0, context.NScreens):
            self.screens.append ({})

    def Update (self):
        cdef CCSList * setlist
        cdef CCSList * glist
        cdef CCSList * sglist
        cdef CCSSetting * sett
        cdef CCSGroup * gr
        cdef CCSSubGroup * sgr
        cdef CCSSettingType t
        cdef CCSSettingInfo * i

        groupIndex = 0
        glist = ccsGetPluginGroups (self.ccsPlugin)
        while glist != NULL:
            gr = <CCSGroup *> glist.data
            self.groups[gr.name] = (groupIndex, {})
            subGroupIndex = 0
            sglist = gr.subGroups
            while sglist != NULL:
                sgr = <CCSSubGroup *> sglist.data
                scr = []
                for n in range (0, self.context.NScreens):
                    scr.append ({})
                self.groups[gr.name][1][sgr.name] = (subGroupIndex,
                                                     SSGroup ({}, scr))
                subGroupIndex = subGroupIndex + 1
                sglist = sglist.next
            groupIndex = groupIndex + 1
            glist = glist.next
        setlist = ccsGetPluginSettings (self.ccsPlugin)

        self.hasExtendedString = False
        rank = 0
        while setlist != NULL:
            sett = <CCSSetting *> setlist.data

            subgroup = self.groups[sett.group][1][sett.subGroup][1]

            if sett.isScreen:
                setting = Setting (self, sett.name, True, sett.screenNum)
                self.screens[sett.screenNum][sett.name] = setting
                subgroup.Screens[sett.screenNum][sett.name] = setting
            else:
                setting = Setting (self, sett.name, False)
                self.display[sett.name] = setting
                subgroup.Display[sett.name] = setting

            t = sett.type
            i = &sett.info
            if t == TypeList:
                t = i.forList.listType
                i = <CCSSettingInfo *> i.forList.listInfo
            if t == TypeString and i.forString.extensible:
                self.hasExtendedString = True

            if not self.ranking.has_key (sett.name):
                self.ranking[sett.name] = rank
                rank = rank + 1
            
            setlist = setlist.next

        self.loaded = True

        self.ApplyStringExtensions (True, self.Enabled)
        self.SortStringSettings ()

    def SortStringSettings (self):
        for i in xrange (self.context.nScreens):
            for name, setting in self.Screens[i].items ():
                self.SortSingleStringSetting (setting)
        for name, setting in self.Display.items ():
            self.SortSingleStringSetting (setting)

    def SortSingleStringSetting (self, Setting setting):
        cdef CCSSettingType t
        cdef CCSSettingInfo * i

        t = setting.ccsSetting.type
        i = &setting.ccsSetting.info
        if t == TypeList:
            t = i.forList.listType
            i = <CCSSettingInfo *> i.forList.listInfo
        if t != TypeString:
            return

        (itemsByName, listOfAddedItems) = \
            StrRestrictionListToDict (i.forString.restriction,
                                      setting.extendedStrRestrictions)

        # Let base string restrictions be the ones given in the option metadata
        # in the base plugin plus the ones found in the extensions in the same
        # plugin.
        setting.baseStrRestrictions = \
            listOfAddedItems + setting.baseStrRestrictions

        if i.forString.sortStartsAt < 0:
            # don't sort
            sortedItems = itemsByName.items ()
        elif i.forString.sortStartsAt == 0:
            # Sort all items by value
            sortedItems = sorted (itemsByName.items (),
                                  key=StringSettingKeyFunc)
        else:
            # Sort first sortStartsAt many items by value and
            # the remaining ones by name
            itemsNotSorted = \
                setting.baseStrRestrictions[:i.forString.sortStartsAt]
            itemsNotSortedSet = set (itemsNotSorted)
            allItemsSet = set (itemsByName.items ())
            itemsSortedByName = sorted (list (allItemsSet - itemsNotSortedSet),
                                        key=operator.itemgetter (0))
            sortedItems = itemsNotSorted + itemsSortedByName

        itemsByValue = {}
        for (index, (name, value)) in enumerate (sortedItems):
            itemsByValue[value] = (name, index)

        # Insert itemsByName and sortedItems into setting.info
        if setting.ccsSetting.type == TypeList:
            setting.info = (setting.info[0], (itemsByName,
                                              itemsByValue,
                                              sortedItems))
        else:
            setting.info = (itemsByName, itemsByValue, sortedItems)

    def ApplyStringExtensions (self, sortBaseSetting, extendOthersToo):
        cdef CCSStrExtensionList * extList
        cdef CCSStrExtension * ext
        cdef char * baseSettingName
        cdef CCSStringList * baseSettingList
        cdef CCSSettingType t
        cdef CCSSettingInfo * i
        cdef CCSStrRestrictionList * restrictionList
        cdef CCSStrRestriction * restriction
        cdef Plugin basePlugin
        cdef Setting setting

        extList = ccsGetPluginStrExtensions (self.ccsPlugin)
        while extList:
            ext = <CCSStrExtension *> extList.data

            # If not extending others and extension base is not self, skip
            if (not (extendOthersToo or ext.basePlugin == self.Name)) or \
            ext.basePlugin not in self.context.Plugins:
                extList = extList.next
                continue

            basePlugin = self.context.Plugins[ext.basePlugin]

            baseSettingList = ext.baseSettings
            while baseSettingList:
                baseSettingName = <char *> baseSettingList.data

                if ext.isScreen:
                    settings = []
                    for x in xrange (self.context.nScreens):
                        settings.append (basePlugin.Screens[x][baseSettingName])
                else:
                    settings = [basePlugin.Display[baseSettingName]]

                for settingItem in settings:
                    setting = settingItem
                    t = setting.ccsSetting.type
                    i = &setting.ccsSetting.info
                    if t == TypeList:
                        t = i.forList.listType
                        i = <CCSSettingInfo *> i.forList.listInfo
                    if not (t == TypeString and i.forString.extensible):
                        return

                    restrictionList = ext.restriction

                    # Add each item in restriction list to the setting
                    while restrictionList != NULL:
                        restriction = <CCSStrRestriction *> restrictionList.data
                        setting.extendedStrRestrictions[restriction.name] = \
                            restriction.value
                        if ext.basePlugin == self.Name:
                            setting.baseStrRestrictions.append ((restriction.name,
                                                                 restriction.value))
                        restrictionList = restrictionList.next

                    if sortBaseSetting:
                        basePlugin.SortSingleStringSetting (setting)

                baseSettingList = baseSettingList.next

            extList = extList.next

    def GetExtensionBasePlugins (self):
        cdef CCSStrExtensionList * extList
        cdef CCSStrExtension * ext

        basePlugins = set ([])
        extList = ccsGetPluginStrExtensions (self.ccsPlugin)
        while extList:
            ext = <CCSStrExtension *> extList.data
            basePlugins.add (self.context.Plugins[ext.basePlugin])
            extList = extList.next

        return list (basePlugins)

    property Context:
        def __get__ (self):
            return self.context

    property Groups:
        def __get__ (self):
            if not self.loaded:
                self.Update ()
            return self.groups

    property Display:
        def __get__ (self):
            if not self.loaded:
                self.Update ()
            return self.display

    property Screens:
        def __get__ (self):
            if not self.loaded:
                self.Update ()
            return self.screens

    property Ranking:
        def __get__ (self):
            if not self.loaded:
                self.Update ()
            return self.ranking

    property Name:
        def __get__ (self):
            return self.ccsPlugin.name

    property ShortDesc:
        def __get__ (self):
            return self.ccsPlugin.shortDesc

    property LongDesc:
        def __get__ (self):
            return self.ccsPlugin.longDesc

    property Category:
        def __get__ (self):
            return self.ccsPlugin.category

    property Features:
        def __get__ (self):
            features = StringListToList (self.ccsPlugin.providesFeature)
            return features

    property Initialized:
        def __get__ (self):
            return bool (self.loaded)

    property Enabled:
        def __get__ (self):
            return bool (ccsPluginIsActive (self.context.ccsContext,
                                            self.ccsPlugin.name))
        def __set__ (self, val):
            if val:
                if len (self.EnableConflicts):
                    return
                ccsPluginSetActive (self.ccsPlugin, True)
            else:
                if len (self.DisableConflicts):
                    return
                ccsPluginSetActive (self.ccsPlugin, False)

    property EnableConflicts:
        def __get__ (self):
            cdef CCSPluginConflictList * pl, * pls
            cdef CCSPluginConflict * pc
            cdef CCSPluginList * ppl
            cdef CCSPlugin * plg

            if self.Enabled:
                return []

            ret = []
            pl = ccsCanEnablePlugin (self.context.ccsContext,
                                     self.ccsPlugin)
            pls = pl
            while pls != NULL:
                pc = <CCSPluginConflict *> pls.data
                rpl = []
                ppl = pc.plugins
                while ppl != NULL:
                    plg = <CCSPlugin *> ppl.data
                    rpl.append (self.context.Plugins[plg.name])
                    ppl = ppl.next
                ret.append ((ConflictTypeString[pc.type], pc.value, rpl))
                pls = pls.next
            if pl != NULL:
                ccsPluginConflictListFree (pl, True)
            return ret

    property DisableConflicts:
        def __get__ (self):
            cdef CCSPluginConflictList * pl, * pls
            cdef CCSPluginConflict * pc
            cdef CCSPluginList * ppl
            cdef CCSPlugin * plg

            if not self.Enabled:
                return []

            ret = []
            pl = ccsCanDisablePlugin (self.context.ccsContext,
                                      self.ccsPlugin)
            pls = pl
            while pls != NULL:
                pc = <CCSPluginConflict *> pls.data
                rpl = []
                ppl = pc.plugins
                while ppl != NULL:
                    plg = <CCSPlugin *> ppl.data
                    rpl.append (self.context.Plugins[plg.name])
                    ppl = ppl.next
                ret.append ((ConflictTypeString[pc.type], pc.value, rpl))
                pls = pls.next
            if pl != NULL:
                ccsPluginConflictListFree (pl, True)
            return ret

cdef class Profile:
    cdef Context context
    cdef char * name

    def __cinit__ (self, Context context, name):
        self.context = context
        self.name = strdup (name)

    def __dealloc (self):
        free (self.name)

    def Delete (self):
        ccsDeleteProfile (self.context.ccsContext, self.name)

    property Name:
        def __get__ (self):
            return self.name

cdef class Backend:
    cdef Context context
    cdef char * name
    cdef char * shortDesc
    cdef char * longDesc
    cdef Bool profileSupport
    cdef Bool integrationSupport

    def __cinit__ (self, Context context, info):
        self.context = context
        self.name = strdup (info[0])
        self.shortDesc = strdup (info[1])
        self.longDesc = strdup (info[2])
        self.profileSupport = bool (info[3])
        self.integrationSupport = bool (info[4])
    
    def __dealloc__ (self):
        free (self.name)
        free (self.shortDesc)
        free (self.longDesc)

    property Name:
        def __get__ (self):
            return self.name
 
    property ShortDesc:
        def __get__ (self):
            return self.shortDesc

    property LongDesc:
        def __get__ (self):
            return self.longDesc

    property IntegrationSupport:
        def __get__ (self):
            return self.integrationSupport

    property ProfileSupport:
        def __get__ (self):
            return self.profileSupport

cdef class Context:
    cdef CCSContext * ccsContext
    cdef object plugins
    cdef object categories
    cdef object profiles
    cdef object currentProfile
    cdef object backends
    cdef object currentBackend
    cdef int nScreens
    cdef Bool integration

    def __cinit__ (self, screens = [0], plugins = [], basic_metadata = False):
        cdef CCSPlugin * pl
        cdef CCSList * pll
        if basic_metadata:
            ccsSetBasicMetadata (True)
        self.nScreens = nScreens = len (screens)
        self.plugins = {}
        cdef unsigned int * screensBuf
        screensBuf = <unsigned int *> malloc (sizeof (unsigned int) * nScreens)
        for i in range (nScreens):
            screensBuf[i] = screens[i]
        if not len (plugins):
            self.ccsContext = ccsContextNew (screensBuf, nScreens)
        else:
            self.ccsContext = ccsEmptyContextNew (screensBuf, nScreens)
        free (screensBuf)

        for plugin in plugins:
            self.LoadPlugin (plugin)

        ccsReadSettings (self.ccsContext)
        pll = self.ccsContext.plugins
        self.categories = {}
        while pll != NULL:
            pl = <CCSPlugin *> pll.data
            self.plugins[pl.name] = Plugin (self, pl.name)
            if pl.category == NULL:
                cat = ''
            else:
                cat = pl.category
            if not self.categories.has_key (cat):
                self.categories[cat] = []
            self.categories[cat].append (self.plugins[pl.name])
            pll = pll.next

        self.integration = ccsGetIntegrationEnabled (self.ccsContext)
        
        self.UpdateProfiles ()

    def UpdateExtensiblePlugins (self):
        cdef Plugin plugin

        # Reset all extensible plugins
        for name, pluginItem in self.plugins.items ():
            plugin = pluginItem
            if plugin.hasExtendedString:
                plugin.Update ()

        # Apply restricted string extensions
        for name, pluginItem in self.plugins.items ():
            plugin = pluginItem
            if plugin.Enabled:
                plugin.ApplyStringExtensions (False, True)

        # Sort restricted string settings
        for name, pluginItem in self.plugins.items ():
            plugin = pluginItem
            if plugin.Enabled and plugin.hasExtendedString:
                plugin.SortStringSettings ()

    def __dealloc__ (self):
        ccsContextDestroy (self.ccsContext)

    def LoadPlugin (self, plugin):
        return ccsLoadPlugin (self.ccsContext, plugin)

    # Returns the settings that should be updated
    def ProcessEvents (self, flags = 0):
        ccsProcessEvents (self.ccsContext, flags)
        if len (self.ChangedSettings):
            self.Read ()
            return True
        return False

    def Write (self, onlyChanged = True):
        if onlyChanged:
            ccsWriteChangedSettings (self.ccsContext)
        else:
            ccsWriteSettings (self.ccsContext)

    def Read (self):
        ccsReadSettings (self.ccsContext)

    def UpdateProfiles (self):
        self.profiles = {}
        self.currentProfile = Profile (self, ccsGetProfile (self.ccsContext))
        cdef CCSStringList * profileList
        cdef char * profileName
        profileList = ccsGetExistingProfiles (self.ccsContext)
        while profileList != NULL:
            profileName = <char *> profileList.data
            self.profiles[profileName] = Profile (self, profileName)
            profileList = profileList.next

        self.backends = {}
        cdef CCSBackendInfoList * backendList
        cdef CCSBackendInfo * backendInfo
        backendList = ccsGetExistingBackends ()
        while backendList != NULL:
            backendInfo = <CCSBackendInfo *> backendList.data
            info = (backendInfo.name, backendInfo.shortDesc,
                    backendInfo.longDesc, backendInfo.profileSupport,
                    backendInfo.integrationSupport)
            self.backends[backendInfo.name] = Backend (self, info)
            backendList = backendList.next
        self.currentBackend = self.backends[ccsGetBackend (self.ccsContext)]
    
    def ResetProfile (self):
        self.currentProfile = Profile (self, "")
        ccsSetProfile (self.ccsContext, "")
        ccsReadSettings (self.ccsContext)

    def Import (self, path, autoSave = True):
        ret = bool (ccsImportFromFile (self.ccsContext, path, True))
        if autoSave:
            ccsWriteSettings (self.ccsContext)
        return ret

    def Export (self, path, skipDefaults = False):
        return bool (ccsExportToFile (self.ccsContext, path, skipDefaults))

    property Plugins:
        def __get__ (self):
            return self.plugins

    property Categories:
        def __get__ (self):
            return self.categories

    property CurrentProfile:
        def __get__ (self):
            return self.currentProfile
        def __set__ (self, profile):
            self.currentProfile = profile
            ccsSetProfile (self.ccsContext, profile.Name)
            ccsReadSettings (self.ccsContext)

    property Profiles:
        def __get__ (self):
            return self.profiles

    property CurrentBackend:
        def __get__ (self):
            return self.currentBackend
        def __set__ (self, backend):
            self.currentBackend = backend
            ccsSetBackend (self.ccsContext, backend.Name)
            ccsReadSettings (self.ccsContext)

    property Backends:
        def __get__ (self):
            return self.backends

    property ChangedSettings:
        def __get__ (self):
            return SettingListToList (self, self.ccsContext.changedSettings)
        def __set__ (self, value):
            cdef CCSSettingList * settingList
            if self.ccsContext.changedSettings != NULL:
                self.ccsContext.changedSettings = \
                    ccsSettingListFree (self.ccsContext.changedSettings, False)
            if value != None and len (value) != 0:
                settingList = ListToSettingList (value)
                self.ccsContext.changedSettings = settingList
                
    property AutoSort:
        def __get__ (self):
            return bool (ccsGetPluginListAutoSort (self.ccsContext))
        def __set__ (self, value):
            ccsSetPluginListAutoSort (self.ccsContext, bool (value))

    property NScreens:
        def __get__ (self):
            return self.nScreens

    property Integration:
        def __get__ (self):
            return bool (self.integration)
        def __set__ (self, value):
            self.integration = value
            ccsSetIntegrationEnabled (self.ccsContext, value)
            ccsReadSettings (self.ccsContext)

