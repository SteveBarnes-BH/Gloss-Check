#!/usr/bin/env python
#encoding:utf-8
"""
  Author:  Steve Barnes --<StevenJohn.Barnes@ge.com>
  Purpose: Arguments for the glossary checker.
  Created: 17/04/2017
"""

try:
    import enchant
except ImportError:
    enchant = None

ARG_LIST = [
    (['-M', '-m', '--min-acc'],
     {'type':int, "action":'store', "default":2, 'choices':range(2, 9),
      'help':"Minimum Length for a possible glossary entry"}),
    (['-u', '-U', '--upper_only'],
     {'action':'store_true',
      'help':"Only consider all uppercase strings as candidates."}),
    (['-C', '-c', '--chars_only'],
     {'action':'store_true',
      "help":"Exclude words with embedded numbers or symbols."}),
    (['-K', '-k', '--inc_camel',],
     {'action':'store_true',
      "help":'Include any word with upper any case after the first letter.'}),
    (['-o', '-1', '--one-per-line'],
     {'action':'store_true', "dest":'oneper',
      "help":"Display in a single column"}),
    (['-gu', '-GU', '--glossary-unused'],
     {'action':'store_true',
      "help":"Show unused entries from the glossary."}),
]


LANGS = []
# See if we have a dictionary available
if enchant is not None:
    LANGS = enchant.list_languages()

# Command Line Arguments
if len(LANGS): # Add the language option if we have a dictionary available
    ARG_LIST.insert(0, (['-L', '-l', '--lang'],
                        {'action':'store', 'choices':LANGS, 'default':'en_GB',
                         "help":'Language code to spell check against'}),
                   )


if __name__ == '__main__':
    pass
