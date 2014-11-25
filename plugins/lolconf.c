/*
 * Copyright © 2014 Kristian Lyngstøl <kristian@bohemians.org>
 *
 * Permission to use, copy, modify, distribute, and sell this software
 * and its documentation for any purpose is hereby granted without
 * fee, provided that the above copyright notice appear in all copies
 * and that both that copyright notice and this permission notice
 * appear in supporting documentation, and that the name of
 * Mike Dransfield not be used in advertising or publicity pertaining to
 * distribution of the software without specific, written prior permission.
 * Mike Dransfield makes no representations about the suitability of this
 * software for any purpose. It is provided "as is" without express or
 * implied warranty.
 *
 * MIKE DRANSFIELD DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
 * INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN
 * NO EVENT SHALL MIKE DRANSFIELD BE LIABLE FOR ANY SPECIAL, INDIRECT OR
 * CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
 * OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
 * NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
 * WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 *
 *
 * Still just a mess and doesn't do anything useful yet.
 *
 * I started out with ini.c and ripped out everything and put things back,
 * so things might look similar. This is still just a lolconf, so don't
 * expect it to do anything useful yet. It's mainly written to experiment
 * with option handling and figure out what works and what doesn't.
 */

#define _GNU_SOURCE		/* for asprintf */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <compiz-core.h>
#include <compiz-helpers.h>

#define GET_LOL_CORE(c) \
	((struct LolCore *) (c)->base.privates[corePrivateIndex].ptr)
#define LOL_CORE(c) \
	struct LolCore *lc = GET_LOL_CORE (c)

#define NUM_OPTIONS(s) (sizeof ((s)->opt) / sizeof (CompOption))

static int corePrivateIndex;

static CompMetadata lolMetadata;
struct LolCore {
	CompTimeoutHandle timeoutHandle;
};

/*
 * Borrowed from ini.c for now (Thanks Mike)
 */
static Bool
csvToList(CompDisplay * d, char *csv, CompListValue * list, CompOptionType type)
{
	char *splitStart = NULL;
	char *splitEnd = NULL;
	char *item = NULL;
	int itemLength, count, i;
	assert(csv);
	assert(list);
	if (csv[0] == '\0') {
		list->nValue = 0;
		return FALSE;
	}

	int length = strlen(csv);
	count = 1;
	for (i = 0; csv[i] != '\0'; i++)
		if (csv[i] == ',' && i != length - 1)
			count++;

	splitStart = csv;
	list->value = malloc(sizeof(CompOptionValue) * count);
	list->nValue = count;

	assert(list->value);

	if (list->value) {
		for (i = 0; i < count; i++) {
			splitEnd = strchr(splitStart, ',');

			if (splitEnd) {
				itemLength =
				    strlen(splitStart) - strlen(splitEnd);
				item = malloc(sizeof(char) * (itemLength + 1));
				assert(item);
				strncpy(item, splitStart, itemLength);
				item[itemLength] = 0;
			} else {
				item = strdup(splitStart);
			}
			assert(item);

			switch (type) {
			case CompOptionTypeString:
				list->value[i].s = strdup(item);
				break;
			case CompOptionTypeBool:
				list->value[i].b =
				    item[0] ? (Bool) atoi(item) : FALSE;
				break;
			case CompOptionTypeInt:
				list->value[i].i = item[0] ? atoi(item) : 0;
				break;
			case CompOptionTypeFloat:
				list->value[i].f = item[0] ? atof(item) : 0.0f;
				break;
			case CompOptionTypeKey:
				stringToKeyAction(d, item,
						  &list->value[i].action);
				break;
			case CompOptionTypeButton:
				stringToButtonAction(d, item,
						     &list->value[i].action);
				break;
			case CompOptionTypeEdge:
				list->value[i].action.edgeMask =
				    stringToEdgeMask(item);
				break;
			case CompOptionTypeBell:
				list->value[i].action.bell = (Bool) atoi(item);
				break;
			case CompOptionTypeMatch:
				matchInit(&list->value[i].match);
				matchAddFromString(&list->value[i].match, item);
				break;
			default:
				break;
			}

			splitStart = ++splitEnd;
			if (item) {
				free(item);
				item = NULL;
			}
		}
	}

	return TRUE;
}

/*
 * FIXME: Move to core and make it handle everything
 */
#if 0
static void debugOption(CompOption * o)
{
	int i;
	assert(o);
	switch (o->type) {
	case CompOptionTypeBool:
		compDebug("%s: %s", o->name, o->value.b ? "TRUE" : "FALSE");
		break;
	case CompOptionTypeInt:
		compDebug("%s: %d", o->name, o->value.i);
		break;
	case CompOptionTypeFloat:
		compDebug("%s: %f", o->name, o->value.f);
		break;
	case CompOptionTypeString:
		compDebug("%s: %s", o->name, o->value.s);
		break;
	case CompOptionTypeList:
		compDebug("%s list: ", o->name);
		CompOption o2;
		o2.name = "list-item";
		o2.type = o->value.list.type;
		for (i = 0; i < o->value.list.nValue; i++) {
			o2.value = o->value.list.value[i];
			debugOption(&o2);
		}
		break;
	default:
		break;
	}
}
#endif

/*
 * Set an option for a given plugin.
 *
 */
static CompBool setOption(char *plug, char *strscreen, char *name, char *strvalue)
{
	CompDisplay *d;
	CompOptionValue value;
	CompBool result;
	CompObject *obj;
	int screen;

	if (!strscreen)
		screen = -1;
	else if (!*strscreen)
		screen = -1;
	else
		screen = atoi(strscreen);

	d = core.displays;
	assert(d);
	assert(plug);
	assert(name);
	assert(strvalue);
	if (screen < 0)
		obj = &d->base;
	else
		obj = &d->screens->base;



	result = csvToList(d, strvalue, &value.list, CompOptionTypeString);
	assert(result);
	value.list.type = CompOptionTypeString;
	result = (*core.setOptionForPlugin) (obj,
					     plug, name, &value);

	return result;
}
/*
 * Magic, magic I tell you.
 */
static CompBool handleTimeout(void *closure)
{
	CompBool result;

#if 0	
	d = core.displays;
	o = compFindOption(d->opt, NUM_OPTIONS(d), "active_plugins", &index);
	if (o)
		debugOption(o);
	else
		compLog("... vat");
#endif
	result = setOption("core", "", "active_plugins", "png,move,mousepoll,ezoom,staticswitcher,resize,cube,rotate,lolconf,decoration,core");
	compLog("%s", result ? "TRUE" : "FALSE");

	return FALSE;
}

static Bool lolInit(CompPlugin * p)
{
	struct LolCore *lc;
	lc = malloc(sizeof(struct LolCore));
	assert(lc);
	if (!compInitPluginMetadataFromInfo(&lolMetadata, p->vTable->name,
					    0, 0, 0, 0))
		compLog("Failed to init plugin metadata");

	corePrivateIndex = allocateCorePrivateIndex();
	assert(corePrivateIndex >= 0);

	core.base.privates[corePrivateIndex].ptr = lc;
	lc->timeoutHandle = compAddTimeout(1, 1000, handleTimeout, lc);

	//    compAddMetadataFromFile (&lolMetadata, p->vTable->name);

	return TRUE;
}

static void lolFini(CompPlugin * p)
{
	struct LolCore *lc;
	assert(corePrivateIndex >= 0);
	lc = core.base.privates[corePrivateIndex].ptr;
	assert(lc);
	free(lc);
	freeCorePrivateIndex(corePrivateIndex);
}

static CompMetadata *lolGetMetadata(CompPlugin * plugin)
{
	return &lolMetadata;
}

CompPluginVTable lolVTable = {
	"lolconf",
	lolGetMetadata,
	lolInit,
	lolFini,
	0,
	0,
	0,			/* GetObjectOptions */
	0			/* SetObjectOption */
};

CompPluginVTable *getCompPluginInfo20070830(void)
{
	return &lolVTable;
}
