#!/usr/bin/env python
#coding:utf-8
"""
  Purpose: Find the candidates for the glossary in a word document.
  Author: Steve Barnes --<StevenJohn.Barnes@ge.com>
  Created: 13/03/2017.
  Updated: 22/04/2017.

  Find the candidates for the glossary in a word document.
"""
#(Inspired by python-docx <https://github.com/mikemaccana/python-docx> &
#<http://etienned.github.io/posts/extract-text-from-word-docx-simply/>)
from __future__ import print_function
import sys
import argparse

import text_utls
import version_info
import args
from gc_gui import (GUI_OK, start_gui)
import gloss_utils


def parse_args():
    """ Parse the arguments."""
    cl_args = [  # Items that only apply to the command line version.
        (['-G', '-g', '--glossary'],
         {'action':'append', "type":argparse.FileType('r'),
          "help":'An existing glossary to ignore'}),
        (['-v', '--version'],
         {'action':'store_true',
          "help":'Show version information and exit.'}),
        (['DOCS'],
         {"nargs":'*',
          'help':'Word document(s) to check, (Wildcards OK).'}),
    ]
    if len(args.LANGS):
        cl_args.append(
            (['-LL', '-ll', '--list-langs'],
             {'action':'store_true',
              "help":'List the available Language codes & exit'}))
    parser = argparse.ArgumentParser(
        #usage=USAGE,
        description=__doc__,
        #version='0.4'
    )
    for argp, argv in args.ARG_LIST:
        parser.add_argument(*argp, **argv)
    for argp, argv in cl_args:
        parser.add_argument(*argp, **argv)

    ops = parser.parse_args()
    if len(args.LANGS) == 0:
        ops.lang = None
    if ops.version:
        version_info.show_versions()

    return ops

def cmdline_main():
    """ Run the program."""
    ops = parse_args()
    ingloss = text_utls.get_glossary(ops)
    gloss_utils.process_docs(ops, ingloss)


if __name__ == '__main__':
    if GUI_OK and len(sys.argv) < 2:
        start_gui()
    else:
        cmdline_main()
