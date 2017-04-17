#!/usr/bin/env python
#encoding:utf-8
"""
  Author:  Steve Barnes --<StevenJohn.Barnes@ge.com>
  Purpose: Convert MS Word doc files to docx
  Created: 04/04/2017
"""
from __future__ import print_function
import sys
import os
import time
import win32com.client as win32


def doc2docx(inpath, outpath=None):
    """ Convert a file at the specified location to docx."""
    path = os.path.abspath(inpath)
    if not os.path.exists(path) or not os.path.isfile(path):
        raise IOError('%s is missing or not a file' % path)
    if outpath is None:
        outpath = os.path.splitext(path)[0] + '.DOCX'
    else:
        outpath = os.path.abspath(outpath)
    if os.path.exists(outpath):
        raise IOError('%s already exists' % outpath)
    print("Starting Word to convert %s to .docx" % inpath)
    word = win32.gencache.EnsureDispatch('Word.Application')
    if len(word.Documents) == 0:  # Only hide word if there is nothing else open
        word.Visible = False
    word.Documents.Open(path)
    time.sleep(0.3)
    word.ActiveDocument.SaveAs(outpath, FileFormat=12)
    time.sleep(0.3)
    word.ActiveDocument.Close()
    if len(word.Documents) == 0:  # Only Quit word if there is nothing else open
        word.Quit()

    print("Written as:", outpath)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: doc2docx infile [outfile]")
    else:
        doc2docx(*sys.argv[1:])
        print("Done!")
