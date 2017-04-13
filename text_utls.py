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
    for output in outtext:
        if sys.version_info.major < 3 or sys.version_info.minor < 6:
            print(codecs.encode(output, 'ascii', 'backslashreplace'))
        else:
            print(output)
