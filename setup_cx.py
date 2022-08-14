#!/usr/bin/env python
# coding:utf-8
"""
Author:  Steve Barnes -- <Steven.Barnes@bakerhughes.com>
Purpose: Build Glossary Checker into an executable.
Created: 08/09/22

"""

# System Imports
import sys

# Library Imports
from cx_Freeze import setup, Executable
import setuptools_scm

# Local Imports

# Create the version information file
setuptools_scm.get_version(".", write_to="gloss_check/_version.py")

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = {
    "packages": ["gloss_check", "os", "enchant"],
    "excludes": ["tkinter"],
}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Glossary_Checker",
    # This should be your name or the name of the organization which owns the
    # project.
    author="Steve Barnes",  # Optional
    # This should be a valid email address corresponding to the author listed
    # above.
    author_email="Steven.Barnes@bakerhughes.com",  # Optional
    license="Baker-Hughes Internal",
    # This section is to trigger the use of setuptools_scm to automate version numbers.
    use_scm_version=True,
    setup_requires=[
        "wheel",
        "setuptools_scm",
    ],
    description="Glossary Checker!",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "gloss_check/__main__.py",
            target_name="Gloss-Check",
            base=None,
            icon="Gloss_Check.ico",
        ),
        Executable(
            "gloss_check/gc_gui.py",
            target_name="Gloss-Check-Gui",
            base=base,
            icon="Gloss_Check.ico",
        ),
    ],
)
