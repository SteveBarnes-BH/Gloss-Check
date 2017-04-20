#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Steve Barnes --<StevenJohn.Barnes@ge.com>
  Purpose: Utilties for the glossary checker
  Created: 11/04/2017
"""
from __future__ import print_function
import sys
import textwrap
import codecs
import time
try:
    import win_unicode_console as wuc
except ImportError:
    wuc = None

try:
    import enchant
except ImportError:
    enchant = None

try:
    import enchant.tokenize as etock
except ImportError:
    etock = None

def clean_wordlist(wordlist, minacc=1):
    """ Clean up a word list."""
    validwords = set()
    for word in wordlist:
        #cleanword = word.decode('utf-8', 'ignore').strip(u'“”,\'"‘ ’()./:;')
        cleanword = word.strip(u'“”,\'"‘ ’()./:;')
        if len(cleanword) >= minacc:
            validwords.add(cleanword)
    return list(validwords)

def smart_print(options, entries):
    """ Smart Printing."""
    if options.oneper:
        outtext = [u'\n'.join(entries)]
    else:
        outtext = textwrap.wrap(', '.join(entries), 78)
    if wuc:
        wuc.enable()
        print('\n'.join(outtext))
        wuc.disable()
    else:
        for output in outtext:
            if sys.version_info.major < 3 or sys.version_info.minor < 6:
                print(codecs.encode(output, 'ascii', 'backslashreplace'))
            else:
                print(output)

def get_glossary(ops):
    """ Get predefined glossaries."""
    ingloss = []
    if hasattr(ops, 'list_langs') and ops.list_langs:
        if enchant is None:
            print('No spell checker - try `pip install pyenchant`')
        else:
            print(enchant.list_languages())
        sys.exit()
    if ops.glossary:
        print('Reading Glossary:')
        for item in ops.glossary:
            if isinstance(item, str) or sys.version_info[0] == 2 and isinstance(
                    item, unicode):
                infile = open(item)
            else:
                infile = item
            print('   ', infile.name)
            ingloss.extend(tokenize(infile.read()))
            infile.close()
    ingloss = clean_wordlist(ingloss)
    ingloss = get_candidates_from_list(
        ingloss, upper_only=ops.upper_only, chars_only=ops.chars_only,
        inc_cammel=ops.inc_camel, existing_gloss=[], lang=ops.lang)
    return ingloss

def get_candidates_from_list(words, upper_only=True, inc_cammel=False,
                             chars_only=True,
                             existing_gloss=None, lang='en_GB'):
    """
    Get glossary candidates from a word list.

    Params:
        words: The word list.
        upper_only: Only consider all upper case strings as candidates.
        inc_cammel: Include any word with upper case after the first.
        chars_only: Exclude words with embedded numbers or symbols.
        existing_gloss: An existing glossary to ignore.
        lang: Language code to spell check against.
    """
    if enchant is not None and lang.upper() != "NONE":
        try:
            chker = enchant.Dict(lang)
            words = [w for w in words if len(w) and not chker.check(w)]  # Not in dictionary
        except enchant.errors.DictNotFoundError:
            print(lang, "Dictionary Not Found, use -ll for list of options.")
            time.sleep(1.5)
    if chars_only:  # Only alpha based
        words = [w for w in words if all([c.isalpha() or c == '.' for c in w])]
    if upper_only:  # All upper only
        words = [w for w in words if all(
            [c.isupper() or c == '.' for c in w[:-1]]) and (w[-1].isupper() or w[-1] == 's')]
    if inc_cammel:  # All upper only
        words = [w for w in words if len(w) > 1 and any(
            [c.isupper() for c in w[1:]])]
    if existing_gloss:  # We have a glossary
        words = [w for w in words if w not in existing_gloss]

    return sorted(words)

def tokenize(text):
    """ Split the text into words."""
    tokzr = None
    if etock is not None:
        try:
            tokzr = etock.get_tokenizer()
        except enchant.errors.TokenizerNotFoundError:
            tokzr = None

    if tokzr is None:
        return text.split()
    else:
        return [word for (word, dummy) in tokzr(text)]
