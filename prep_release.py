#!/usr/bin/env python
#encoding:utf-8
"""
  Author:  Steve Barnes --<StevenJohn.Barnes@ge.com>
  Purpose: Prepare a release
  Created: 17/04/2017
"""
from __future__ import print_function
import sys
import os
import datetime
from dulwich.repo import Repo
import semantic_version as sv
import subprocess
import re
import zipfile

def get_latest_tag(repo):
    """ Get the latest tag from the repo."""
    toptag = "0.0.0"
    topbuild = None
    tag_dict = repo.refs.as_dict("refs/tags")
    tags = [(sv.Version.coerce(tag[1:]), tag_dict[tag]) for tag in tag_dict.keys()]
    if len(tags):
        toptag, topbuild = sorted(tags)[-1]
        #toptag.build = str(topbuild)
    return toptag, topbuild

def next_build(last_ver):
    """ Get the next build identifier. """
    build = last_ver.build
    def give_next_build():
        """ Construct a version string from the current."""
        newver = last_ver
        while newver <= last_ver:
            buildname = raw_input('Build Name: ')
            newver = sv.Version("%s.%s.%s-%s" % (last_ver.major, last_ver.minor,
                                                 last_ver.patch, buildname))
            if newver <= last_ver:
                print("Error:", newver, "<=", last_ver)
        return newver
    return give_next_build

def get_next_release(repo):
    """ Prompt for the information to generate the next release tag"""
    release_types = {'M':'Major', 'N':'Minor', 'P':'Patch', 'B':'Build', 'C':'Cancel',}
    last_ver, last_build = get_latest_tag(repo)
    m_next_release = {'M':last_ver.next_major, 'N':last_ver.next_minor,
                      'P':last_ver.next_patch, 'B':next_build(last_ver),
                      'C':sys.exit,}
    print('Last Tagged Version', last_ver)
    rt = '?'
    prompt = "Release Type: %s: " % ', '.join(
        ["%s=%s" % item for item in release_types.iteritems()])
    while rt not in release_types.keys():
        instr = raw_input(prompt)
        rt = instr[0].upper()
    next_release = m_next_release[rt]()
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
    commands = ['git', 'push', 'origin', 'v%s' % ver]
    result = subprocess.check_call(commands, shell=True)
    return result

def pyinstaller(target):
    """ Do the build."""
    commands = ['pyinstaller', '--clean', '-y', target]
    result = subprocess.check_call(commands, shell=True)
    return result

def zipdir(path, ziph):
    """
    add a directory to a zipfile.
    ziph is zipfile handle.
    """
    relroot = os.path.abspath(os.path.join(path, os.pardir))
    for root, dirs, files in os.walk(path):
        zip.write(root, os.path.relpath(root, relroot))
        for filename in files:
            filepath = os.path.join(root, filename)
            arcname = os.path.join(os.path.relpath(root, relroot), filename)
            ziph.write(os.path.relpath(root, relroot), filepath)

def zip_build(target, version):
    """ Zip the build."""
    zf = zipfile.ZipFile('./dist/%s_%s.zip' % (target, version), 'w',
                         zipfile.ZIP_DEFLATED)
    zipdir('./dist/%s.zip' % target, zf)
    zf.close()

def main():
    """ The main process."""
    verfile = "./version_info.py"
    repo = Repo('.')
    next_release = get_next_release(repo)
    print('Next Release:', next_release)
    msg = raw_input("Release Message: ").strip()
    update_version_file(next_release, verfile)
    add_changes_git(msg)
    add_tag_git(next_release, msg)
    try:
        push_tag_git(next_release)
    except subprocess.CalledProcessError:
        print("Push FAILED!")
    if pyinstaller('gloss_check.py') == 0:
        zip_build('gloss_check', 'v%s' % next_release)

if __name__ == '__main__':
    main()
