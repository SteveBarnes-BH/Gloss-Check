#!/usr/bin/env python3
# coding:utf-8
"""
  Purpose: Find the candidates for the glossary in a word document.

  Author: Steve Barnes --<Steven.Barnes@bhge.com>
  Created: 13/03/2017.
  Last Updated: 25/06/2018.
"""
# (Inspired by python-docx <https://github.com/mikemaccana/python-docx> &
# <http://etienned.github.io/posts/extract-text-from-word-docx-simply/>)
from __future__ import print_function
import sys
import argparse

import text_utls
import version_info
import args
from gc_gui import GUI_OK, start_gui
import gloss_utils


def parse_args():
    """Parse the arguments."""
    parser = args.get_cl_parser(__doc__)
    ops = parser.parse_args()
    if len(args.LANGS) == 0:
        ops.lang = None
    if ops.version:
        version_info.show_versions()

    return ops


def cmdline_main():
    """Run the program."""
    ops = parse_args()
    ingloss = text_utls.get_glossary(ops)
    gloss_utils.process_docs(ops, ingloss)


if __name__ == "__main__":
    if GUI_OK and len(sys.argv) < 2:
        start_gui()
    else:
        cmdline_main()
