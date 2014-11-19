/*
 * Copyright © 2014 Kristian Lyngstøl <kristian@bohemians.org>
 *
 * Permission to use, copy, modify, distribute, and sell this software
 * and its documentation for any purpose is hereby granted without
 * fee, provided that the above copyright notice appear in all copies
 * and that both that copyright notice and this permission notice
 * appear in supporting documentation, and that the name of
 * Novell, Inc. not be used in advertising or publicity pertaining to
 * distribution of the software without specific, written prior permission.
 * Novell, Inc. makes no representations about the suitability of this
 * software for any purpose. It is provided "as is" without express or
 * implied warranty.
 *
 * NOVELL, INC. DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE,
 * INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN
 * NO EVENT SHALL NOVELL, INC. BE LIABLE FOR ANY SPECIAL, INDIRECT OR
 * CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
 * OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
 * NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
 * WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 *
 * Author: Kristian Lyngstøl <kristian@bohemians.org>
 *
 */


#ifndef COMPIZ_HELPER_H
#define COMPIZ_HELPER_H

/*
 * Need this to make sure DEBUG is set.
 *
 * It's nasty if people add compiz-helper.h and forget config.h, since you
 * end up with some files with and some files without DEBUG set.
 */
#include "config.h"


/*
 * Skip past .'s and /'s in s, to turn 
 * ../../../src/screen.c into src/screen.c
 *
 * This could probably be a proper function, but since it's used (so far)
 * only for compLogRaw(), it's simpler to keep it as a macro.
 */
#define baseishname(s)			    \
    do {				    \
    while (*s && (*s == '.' || *s == '/'))  \
	s++;				    \
    } while(0)				    \

/*
 * Simple logger-wrapper that prints to stdout.
 *
 * XXX: The fmt is split on a separate line instead of doing a single
 * fprintf. This is to allow using a variable as input (e..g.: char *foo;
 * blatti(foo); compLog(foo, value);) which is some times done by X.
 * The down-side of this is that you can't do compLog("") or compLog()
 * without a warning or error, so for an empty line, compLog(" ") is the
 * best cheat. This is mainly relevant for compDebug(), where it's presumed
 * that the output is largely for developers and just doing a little "hello"
 * is enough.
 *
 */
#define compLogRaw(out, fmt, ...) do {	    \
    char *tmp_base = __FILE__;		    \
    baseishname(tmp_base);		    \
    fprintf(out,"%s (%s:%d): ", __func__,   \
	   tmp_base, __LINE__);		    \
    fprintf(out, fmt, ##__VA_ARGS__);	    \
    fprintf(out, "\n");			    \
} while(0)

#define compLog(fmt, ...) compLogRaw(stdout, fmt, ##__VA_ARGS__)
#define compWarn(fmt, ...) compLogRaw(stderr, fmt, ##__VA_ARGS__)
#ifdef DEBUG
#define compDebug(fmt, ...) compLogRaw(stdout, fmt, ##__VA_ARGS__)
#else
#define compDebug(fmt, ...)
#endif


#endif
