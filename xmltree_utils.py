#!/usr/bin/env python
#encoding:utf-8
"""
  Author:  Steve Barnes --<StevenJohn.Barnes@ge.com>
  Purpose: XML Tree based document processing.
  Created: 17/04/2017
"""
from __future__ import (print_function, )

import os
import zipfile

try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML

import text_utls

# Constants used to decode MS Word Open Document Format
WRD_NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
TABLE = WRD_NS + 'tbl'
PARA = WRD_NS + 'p'
TEXT = WRD_NS + 't'

def get_tree_table_wordlist(tree, minacc=1, tabno=None):
    """
    Get the wordlist from an XML tree.
    If tabno is None then all tables, if it is a simple number then that one and
    if it is a list those.
    """
    tables = []
    indexes = []
    texts = []
    for index, tab in enumerate(tree.getiterator(TABLE)):
        tables.append([node.text for node in tab.getiterator(TEXT)])
        indexes.append(index)
    if tabno is None:
        req_tabs = indexes
    elif isinstance(tabno, int):
        req_tabs = [tabno]
    elif isinstance(tabno, list) and all([isinstance(mem, int) for mem in tabno]):
        req_tabs = tabno
    else:
        raise ValueError("tabno must be one of None, int, list of ints")
    for index in req_tabs:
        texts.extend(tables[index])
    wordlist = set()
    if texts:
        text = ''.join(texts)
        wordlist.update(text.split())
    cwordlist = text_utls.clean_wordlist(wordlist, minacc)
    return cwordlist

def get_docx_tree_wordlist(path, options):  #, extract_glossary=False):
    """
    Take the path of a docx file as argument, return the list of words.
    Note that this doesn't work as well as get_docx2_wordlist
    """
    if not os.path.splitext(path)[-1].lower() == '.docx':
        return False, []
    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml')
    document.close()
    tree = XML(xml_content)

    wordlist = set()
    for paragraph in tree.getiterator(PARA):
        texts = [
            node.text
            for node in paragraph.getiterator(TEXT)
            if node.text]
        if texts:
            text = ''.join(texts)
            wordlist.update(text.split())

    cwordlist = text_utls.clean_wordlist(wordlist, options.min_acc)
    tabwords = get_tree_table_wordlist(tree, minacc=options.min_acc)
    print(len(tabwords), 'words from tables.')
    for word in tabwords:
        if word not in cwordlist:
            cwordlist.append(word)

    return len(cwordlist) > 0, sorted(cwordlist, key=lambda s: s.lower()), []

if __name__ == '__main__':
    pass
