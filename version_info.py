#!/usr/bin/env python
#encoding:utf-8
"""
  Author: Steve Barnes --<StevenJohn.Barnes@ge.com>
  Purpose: Version Information Utilties
  Created: 17/04/2017
"""
from __future__ import print_function
import sys
try:
    import wx
except ImportError:
    wx = None
try:
    import enchant
except ImportError:
    enchant = None
try:
    import docx
except ImportError:
    docx = None

try:
    import textract
except ImportError:
    textract = None

__version__ = "v0.7.1"

def get_version_info():
    """ Get the version information."""
    version_info = ["Glossary Checker %s" % __version__]
    if hasattr(sys, 'frozen'):
        version_info.append('Running Executable built from Python %s' % sys.version)
    else:
        version_info.append("Running under Python %s" % sys.version)
    if wx is not None:
        version_info.append("Using: wx %s for GUI" % wx.version())
    else:
        version_info.append("No GUI! Try `pip install wxpython`")
    if enchant is not None:
        version_info.append(
            "Using: pyEnchant V%s for spelling" % enchant.__version__)
    else:
        version_info.append("No Spell Checker! Try `pip install pyenchant`")
    if docx is not None:
        version_info.append(
            "Using: python-docx %s for .DOCX parsing" % docx.__version__)
    if textract is not None:
        version_info.append("Using: Textract!")
    return version_info


def show_versions():
    """ Show version information and exit."""
    info = get_version_info()
    print('\n'.join(info))
    sys.exit()

if __name__ == '__main__':
    show_versions()
