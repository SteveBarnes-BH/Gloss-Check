#!/usr/bin/env python
# encoding:utf-8
"""
  Author: Steve Barnes --<Steven.Barnes@bhge.com>
  Purpose: Version Information Utilties
  Created: 17/04/2017
"""
from __future__ import (
    print_function,
)

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

try:
    from _version import __version__
except ImportError:
    try:
        from gloss_check._version import __version__
    except ImportError:
        print(
            "Can't get version information\nUse: \n"
            "python -c\"import setuptools_scm;setuptools_scm.get_version('.', write_to='gloss_check/_version.py')\""
            "\nto fix!"
        )
        # __version__ = version("gloss_check")
        __version__ = "0.0.0.NoVersion"


# __version__ = "v1.1.2"  # "v" +
# setuptools_scm.get_version(root="..")


def get_version_info():
    """Get the version information."""
    version_info = ["Glossary Checker %s" % __version__]
    if hasattr(sys, "frozen"):
        version_info.append("Running Executable built from Python %s" % sys.version)
    else:
        version_info.append("Running under Python %s" % sys.version)
    if wx is not None:
        version_info.append("Using: wx %s for GUI" % wx.version())
    else:
        version_info.append("No GUI! Try `pip install wxpython`")
    if enchant is not None:
        version_info.append("Using: pyEnchant V%s for spelling" % enchant.__version__)
    else:
        version_info.append("No Spell Checker! Try `pip install pyenchant`")
    if docx is not None:
        version_info.append(
            "Using: python-docx %s for .DOCX parsing" % docx.__version__
        )
    if textract is None:
        pass
    else:
        version_info.append(f"Using: Textract {textract.VERSION}")
    return version_info


def show_versions():
    """Show version information and exit."""
    info = get_version_info()
    print("\n".join(info))
    sys.exit()


if __name__ == "__main__":
    show_versions()
