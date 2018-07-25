#!/usr/bin/env python
#encoding:utf-8
"""
  Author:  Steve Barnes --<Steven.Barnes@bhge.com>
  Purpose: Arguments for the glossary checker.
  Created: 17/04/2017
"""
from __future__ import (print_function, )
import os
import argparse
import json
import copy

import appdirs

try:
    import enchant
except ImportError:
    enchant = None
try:
    from enchant import tokenize as etock
    #import enchant.tokenize as etock
except ImportError:
    etock = None

CONFIG_DIR = appdirs.user_config_dir(appname='Gloss_Check', appauthor='GE')
CL_CFG_NAME = os.path.join(CONFIG_DIR, "config.json")
GUI_CFG_NAME = os.path.join(CONFIG_DIR, "gui_config.json")

ARG_LIST = [
    (['-M', '-m', '--min-acc'],
     {'type':int, "action":'store', "default":2, 'choices':range(2, 9),
      'lable':'&Min Length', 'savecfg':True,
      'help':"Minimum Length for a possible glossary entry"}),
    (['-u', '-U', '--upper_only'],
     {'action':'store_true',  'lable':'&Upper Only', 'savecfg':True,
      'help':"Only consider all uppercase, (may end with s), strings as candidates."}),
    (['-C', '-c', '--chars_only'],
     {'action':'store_true',  'lable':'&Chars Only', 'savecfg':True,
      "help":"Exclude words with embedded numbers or symbols."}),
    (['-K', '-k', '--inc_camel',],
     {'action':'store_true',  'lable':'Came&l Case', 'savecfg':True,
      "help":'Include any word with upper any case after the first letter.'}),
    (['-o', '-1', '--one-per-line'],
     {'action':'store_true', "dest":'oneper',  'lable':'&1 Entry/line',
      "help":"Display in a single column", 'savecfg':True}),
    (['-T', '-t', '--table_gloss',],
     {'action':'store_true', 'lable':'Glossary from &Tables', 'savecfg':True,
      "help":'Search each document for possible glossary table.'}),
    (['-gu', '-GU', '--glossary-unused'],
     {'action':'store_true', 'lable':'Show U&nused', 'dest':"glossary_unused",
      "help":"Show unused entries from the glossary, (document glossary with -t).",
      'savecfg':True}),
    (['--save-config'],
     {'action':'store_true', 'lable':'&Save Config', 'savecfg':False,
      "help":"Save configuration."}),
]

LANGS = ['NONE']
# See if we have a dictionary available
if enchant is not None:
    LANGS.extend(enchant.list_languages())

# Optional Args - depends on which packages are present.
if len(LANGS) > 1: # Add the language option if we have a dictionary available
    ARG_LIST.insert(0, (['-L', '-l', '--lang'],
                        {'action':'store', 'choices':LANGS, 'default':'en_GB',
                         'lable':'&Language', 'savecfg':True,
                         "help":'Language code to spell check against'}),
                   )
if etock is not None:
    ARG_LIST.append(
        (['-e', '-E', '--etok'],
         {'action':'store_false', 'savecfg':True,
          "help":'Enchant Tokanization (Often better BUT can give odd results)'}),
    )

CL_ARGS = [  # Items that only apply to the command line version.
    (['-G', '-g', '--glossary'],
     {'action':'append', "type":argparse.FileType('r'), 'savecfg':False,
      "help":'An existing glossary to ignore'}),
    (['-v', '--version'],
     {'action':'store_true', 'savecfg':False,
      "help":'Show version information and exit.'}),
    (['--reset-config'],
     {'action':'store_true', 'dest':'reset_config', 'savecfg':False,
      "help":'Clear any existing config values.'}),
    (['DOCS'],
     {"nargs":'*', 'savecfg':False,
      'help':'Word document(s) to check, (Wildcards OK).'}),
]

if len(LANGS) > 1:
    CL_ARGS.append(
        (['-LL', '-ll', '--list-langs'],
         {'action':'store_true', 'savecfg':False,
          "help":'List the available Language codes & exit'}))

GUI_ARGS = [
    (["--Auto-Update"], {
        'dest':'autoupdate', 'action':'store_true', 'lable':'&Auto Update',
        'help':'Automatically reprocess on settings change.', 'savecfg':True,
        }),
]

def default_config(gui=False):
    """
    Clears one of the Command Line or GUI Configuration Files.
    """
    parser = get_cl_parser('Dummy', gui, loadcfg=False)
    opts = parser.parse_args(args=[])  # This should get the deafaults.
    return save_config(opts, gui)

def save_config(optsin, gui=False):
    """ Save a configuration."""
    if isinstance(optsin, dict):
        opts = optsin
    else:
        opts = optsin.__dict__
    writeitems = {}
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    opt_list = get_option_list(gui, False)
    if gui:
        filename = GUI_CFG_NAME
    else:
        filename = CL_CFG_NAME

    for optnames, details in opt_list:
        name = details.get('dest')
        if details.get('savecfg', False):
            if hasattr(opts, '__getitem__'):
                writeitems[name] = opts[name]
            else:
                writeitems[name] = opts.__getattribute__(name)
    with open(filename, 'wt') as outfile:
        json.dump(writeitems, outfile, ensure_ascii=False, sort_keys=True)
    return filename

def read_config_dict(gui=False):
    """ Read the saved config."""
    config = {}
    if gui:
        filename = GUI_CFG_NAME
    else:
        filename = CL_CFG_NAME
    if os.path.exists(filename):
        with open(filename, 'rt') as infile:
            config = json.load(infile)
    return config

def get_option_list(gui=False, remove_specials=True):
    """ Get the options list for command line or gui."""
    optlist = []
    optlist.extend(copy.deepcopy(ARG_LIST))  # Start with the base set of Arguments
    if gui:
        optlist.extend(copy.deepcopy(GUI_ARGS))
    else:
        optlist.extend(copy.deepcopy(CL_ARGS))
    for optnames, details in optlist:
        assert isinstance(details, dict)
        names = [n[2:] for n in optnames if n.startswith('--')]
        if len(names):
            name = names[0]
            name = name.replace('-', '_')
            if not details.get('dest'):
                details['dest'] = name
            if gui and not details.get('lable'):
                lable = name.replace('_', ' ').strip()
                lable = ' '.join([w.capitalize() for w in lable.split()])
                details['lable'] = lable
                #storeas = details.get('dest', name)

        if not gui and remove_specials and details.get('lable'):
            del details['lable']
        if remove_specials and details.get('savecfg', None) is not None:
            del details['savecfg']
    return optlist

def get_cl_parser(description, gui=False, loadcfg=True):
    """ Get an argument parser."""
    parser = argparse.ArgumentParser(description=description)
    optlist = get_option_list(gui)
    for argp, argv in optlist:
        parser.add_argument(*argp, **argv)
    selected = parser.parse_args()
    if loadcfg and selected.reset_config:
        default_config(gui)
    if loadcfg:
        parser.set_defaults(**read_config_dict())
    return parser

if __name__ == '__main__':
    #print("Argument List:")
    #for ARG in ARG_LIST:
        #FLAGS, ACTION_DICT = ARG
        #print("Flag:", ', '.join(FLAGS))
        #print("Uses:")
        #for K, V in ACTION_DICT.iteritems():
            #print("\t%s: %s" % (K, V))
        #print()
    PARSER = get_cl_parser('Parser Test!')
    OPTS = PARSER.parse_args()
    print(OPTS)
    #if OPTS.reset_config:
        #default_config()
        #print(read_config_dict())
    #el
    if OPTS.save_config:
        print(save_config(OPTS))
    print(read_config_dict())
