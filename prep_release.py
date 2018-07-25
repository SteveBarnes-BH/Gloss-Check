#!/usr/bin/env python
#encoding:utf-8
"""
  Author:  Steve Barnes --<Steven.Barnes@bhge.com>
  Purpose: Prepare a release
  Created: 17/04/2017
"""
from __future__ import (print_function, )
import sys
import os
import datetime
import subprocess
import re
import shutil
import collections
from dulwich.repo import Repo
import semantic_version as sv

BOX_PATH = r'"D:\Users\212303160\Desktop\Box Sync (New)\Box Sync\Software\Gloss-Check"'

def get_latest_tag(repo):
    """ Get the latest tag from the repo."""
    toptag = sv.Version("0.0.0")
    topbuild = None
    tag_dict = repo.refs.as_dict("refs/tags")
    tags = [(sv.Version.coerce(tag[1:]), tag_dict[tag]) for tag in tag_dict.keys()]
    if len(tags):
        toptag, topbuild = sorted(tags)[-1]
        #toptag.build = str(topbuild)
    return toptag, topbuild

def next_build(last_ver):
    """ Get the next build identifier. """
    #build = last_ver.build
    def give_next_build():
        """ Construct a version string from the current."""
        newver = sv.Version(str(last_ver))
        now = datetime.datetime.now()
        newver.build = [now.strftime('%Y_%m_%d_%H%M')]
        while newver <= last_ver:
            buildname = raw_input('Build Name: ')
            newver = sv.Version("%s.%s.%s+%s" % (last_ver.major, last_ver.minor,
                                                 last_ver.patch, buildname))
            if newver == last_ver:
                print("Error:", newver, "==", last_ver)
        return newver
    return give_next_build

def get_next_release(repo):
    """ Prompt for the information to generate the next release tag"""
    release_types = collections.OrderedDict()
    if check_connected():
        for k, t in [('M', 'Major'), ('N', 'Minor'), ('P', 'Patch')]:
            release_types[k] = t
    else:
        print("It doesn't lool like we have a connection for releases!")
    release_types['B'] = 'Build'
    release_types['C'] = 'Cancel'
    last_ver, last_build = get_latest_tag(repo)
    m_next_release = {'M':last_ver.next_major, 'N':last_ver.next_minor,
                      'P':last_ver.next_patch, 'B':next_build(last_ver),
                      'C':sys.exit,}
    print('Last Tagged Version', last_ver)
    reltype = '?'
    prompt = "Release Type: %s: " % ', '.join(
        ["%s=%s" % item for item in release_types.iteritems()])
    while reltype not in release_types.keys():
        instr = raw_input(prompt)
        reltype = instr[0].upper()
    next_release = m_next_release[reltype]()
    return next_release

def update_version_file(newver, fpath="./version_info.py"):
    """ Update the version file."""
    with open(fpath) as infile:
        content = infile.read()
    newcontent = re.sub(r"__version__\s*=\s*([\"'].*[\"'])",
                        '__version__ = "v%s"' % newver, content, 1)
    with open(fpath, "wt") as outfile:
        outfile.write(newcontent)

def add_changes_git(msg):
    """ Add the changes to the the git repo."""
    commands = ['git', 'commit', '-a', '-m"%s"' % msg]
    result = subprocess.check_call(commands, shell=True)
    return result

def add_tag_git(ver, msg):
    """ Add the changes to the the git repo."""
    commands = ['git', 'tag', '-a', 'v%s' % ver, '-m"%s"' % msg]
    result = subprocess.check_call(commands, shell=True)
    return result

def push_tag_git(ver):
    """ Add the changes to the the git repo."""
    print('Pushing', ver)
    commands = ['git', 'push', 'origin', 'v%s' % ver]
    result = subprocess.check_call(commands, shell=True)
    return result

def push_git():
    """ Add the changes to the the git repo."""
    print('Pushing file changes')
    commands = ['git', 'push']
    result = subprocess.check_call(commands, shell=True)
    return result

def pyinstaller(target, gui_only=False):
    """ Do the build."""
    commands = [
        'pyinstaller', '--clean', '-y',  # Force Clean Build
        gui_only and '-w' or '-c',  # Windowed or console
        target,
        # Add the tokenizer
        r'--add-data=C:\Python35-32\Lib\site-packages\enchant\tokenize;enchant\tokenize',]
    result = subprocess.check_call(commands, shell=True)
    return result

def zipdir(path, ziph):
    """
    add a directory to a zipfile.
    ziph is zipfile handle.
    """
    relroot = os.path.abspath(os.path.join(path, os.pardir))
    for root, dirs, files in os.walk(path):
        ziph.write(root, os.path.relpath(root, relroot))
        for filename in files:
            filepath = os.path.join(root, filename)
            arcname = os.path.join(os.path.relpath(root, relroot), filename)
            ziph.write(os.path.relpath(root, relroot), filepath)
    ziph.close()

def zip_build(target, version):
    """ Zip the build."""
    outpath = './dist/%s_%s' % (target, version)
    zipped_to = shutil.make_archive(outpath, 'zip', './dist', target)
    #zf = zipfile.ZipFile(outpath, 'w',
                         #zipfile.ZIP_DEFLATED)
    #zf.close()
    print("Zipped to:", zipped_to)
    return zipped_to

def check_connected():
    """ Check if currently connected to network directly or via F5."""
    # Currently a bit of a hack but I have D:/Org2 mapped to a network drive
    # that is only available when connected directly or via F5.
    return os.path.isdir(r'D:/Org2/Engineering/')

def main():
    """ The main process."""
    outfiles = []
    verfile = "./version_info.py"
    repo = Repo('.')
    next_release = get_next_release(repo)
    print('Next Release:', next_release)
    status = "Changes NOT Pushed"
    update_version_file(next_release, verfile)
    release_build = len(next_release.build) == 0
    if release_build:
        pre = raw_input('Pre-Release?: ')
        if len(pre):
            next_release.prerelease = [pre]
            update_version_file(next_release, verfile)
        msg = raw_input("Release Message: ").strip()
        add_changes_git(msg)
        try:
            push_git()
            status = "Changes Pushed"
        except subprocess.CalledProcessError:
            print("Push Changes FAILED!")
        add_tag_git(next_release, msg)
        try:
            push_tag_git(next_release)
            status += ", Tag %s Pushed" % next_release
        except subprocess.CalledProcessError:
            print("Push Tag FAILED!")
            status += ", Tag %s NOT Pushed" % next_release
    if pyinstaller('gloss_check.py', True) == 0:
        outfile =  zip_build('gloss_check', 'v%s-GUI' % next_release)
        status += "\nGUI Only Build Zipped to: %s" % outfile
        outfiles.append(outfile)
    if pyinstaller('gloss_check.py', False) == 0:
        outfile = zip_build('gloss_check', 'v%s' % next_release)
        status += "\nBuild Zipped to: %s" % outfile
        outfiles.append(outfile)
    if release_build and len(outfiles) > 0 and os.path.exists(BOX_PATH):
        print('Copy zips to Box!')
        for oufile in outfiles:
            shutil.copy(outfile, BOX_PATH)
        print('Done!')
    print(status)

if __name__ == '__main__':
    main()
