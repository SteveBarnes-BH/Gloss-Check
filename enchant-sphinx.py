#!/usr/bin/env python
#coding:utf-8
"""
  Author:  Steve Barnes --<StevenJohn.Barnes@ge.com>
  Purpose: Spell check all of the RST files in a sphinx project.
  Created: 14/03/2017
"""
from __future__ import (print_function, )
import os
import fnmatch
import textwrap
import enchant

def get_file_lists(start_dir='.'):
    """ Get a list of files to process."""
    file_list = set()
    glossary_list = set()
    excludedirs = ['.svn', '.git', '.hg']

    for root, dirs, files in os.walk(start_dir):
        for ex in excludedirs:
            if ex in dirs:
                dirs.remove(ex)
        file_list.update([
            os.path.join(root, fn) for fn in fnmatch.filter(files, '*.rst')])
        file_list.update([
            os.path.join(root, fn) for fn in fnmatch.filter(files, '*.txt')])
        glossary_list.update([
            os.path.join(root, fn) for fn in fnmatch.filter(
                files, 'glossary*.rst')])
        glossary_list.update([
            os.path.join(root, fn) for fn in fnmatch.filter(
                files, 'glossary*.txt')])
        file_list = file_list
    return file_list, glossary_list

def get_words(path):
    """ Get a list of each of the words in a file."""
    strips = set()
    adds = set()
    with open(path) as infile:
        wordset = set(infile.read().split())
    for word in wordset:
        sword = word.strip('`.+:()_*"\'-=#,')
        if sword != word:
            strips.add(word)
            if len(sword):
                adds.add(sword)
        if sword.startswith('[') or word.startswith('['):
            strips.add(word)
            strips.add(sword)
    wordset.difference_update(strips)
    wordset.update(adds)
    return wordset

def main(startdir='.', lang='en_UK'):
    """ Get a list of misspelt words that are not in the glossary."""
    checker = enchant.Dict(lang)
    glossaries = set()
    file_list, glossary_list = get_file_lists()
    for path in glossary_list:
        print('Getting glossaries from', path)
        glossaries.update(get_words(path))
    for path in file_list:
        print(path, ':', end=' ')
        bad = [word for word in get_words(path) if not checker.check(
            word) and word not in glossaries]
        if len(bad) == 0:
            print('OK')
        else:
            print(len(bad), "Unknown words:")
            print('\n'.join(textwrap.wrap(', '.join(
                sorted(bad, key=lambda s: s.lower())), 78)))

if __name__ == '__main__':
    main()
