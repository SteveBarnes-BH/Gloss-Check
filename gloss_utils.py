#!/usr/bin/env python
#encoding:utf-8
"""
  Author:  Steve Barnes --<StevenJohn.Barnes@ge.com>
  Purpose: Utility Functions for Glossary checking
  Created: 17/04/2017
"""
from __future__ import print_function
import os
import glob
import tempfile
try:
    import docx
except ImportError:
    docx = None
import text_utls
import docx2utils
import xmltree_utils
import doc2docx

try:
    import textract
except ImportError:
    textract = None

def get_textract_wordlist(path, minacc=1):
    """
    Take the path of a file as an argument, return the list of words.
    """
    result = (False, [])
    if textract:
        try:
            wordlist = textract.process(path, 'utf-8').split()
            result = (True, text_utls.clean_wordlist(wordlist, minacc))
        except (WindowsError, textract.exceptions.ExtensionNotSupported):
            result = (False, [])
    return result

def get_doc_wordlist(path, minacc=1):  #, extract_glossary=False):
    """
    Take the path of a doc file as argument, return the list of words.
    """
    print("Need to convert .doc to temporary .docx")
    tempdir = tempfile.gettempdir()
    temppath = os.path.join(tempdir, 'gloss_check_temp.docx')
    if os.path.exists(temppath):
        os.remove(temppath)
    doc2docx.doc2docx(path, temppath)
    # Create a temprory copy of the doc as docx
    if docx is not None:
        success, cwordlist = docx2utils.get_docx2_wordlist(temppath, minacc)
    else:
        success, cwordlist = xmltree_utils.get_docx_tree_wordlist(temppath, minacc)
    if os.path.exists(temppath):
        os.remove(temppath)
        print('Removed', temppath)
    return success, cwordlist

def get_candidates(
        path, minlen=2, upper_only=True, chars_only=True, inc_cammel=False,
        existing_gloss=None, lang='en_GB'):
    """
    Get glossary candidates from a Word Open Document Format file.

    Params:
        path: The path to the docx file.
        upper_only: Only consider all upper case strings as candidates.
        inc_cammel: Include any word with upper case after the first.
        chars_only: Exclude words with embedded numbers or symbols.
        existing_gloss: An existing glossary to ignore.
        lang: Language code to spell check against.
    """
    success = False
    words = []
    method_dict = {  # Dictionary of methods to use for specific file extensions
        '.docx': xmltree_utils.get_docx_tree_wordlist,
        '.doc': get_doc_wordlist,
    }
    if docx is not None:  # docx library available so override method
        method_dict['.docx'] = docx2utils.get_docx2_wordlist
    method = method_dict.get(os.path.splitext(path)[-1].lower())
    candiates = []
    unused = []
    if method is not None:
        success, words = method(path, minlen)
    elif textract is not None:
        success, words = get_textract_wordlist(path, minlen)
    if success:
        candiates = text_utls.get_candidates_from_list(
            words, upper_only, inc_cammel, chars_only, existing_gloss, lang)
        unused = [item for item in existing_gloss if not item in words]
    return (success, candiates, unused)

def process_docs(options, ext_gloss):
    """ Process the documents."""
    for arg in options.DOCS:
        print('Arg:', arg)
        for filename in glob.glob(arg):
            print('Processing', filename)
            success, candidates, unused = get_candidates(
                filename, minlen=options.min_acc, upper_only=options.upper_only,
                chars_only=options.chars_only, inc_cammel=options.inc_camel,
                existing_gloss=ext_gloss, lang=options.lang)
            if not success:
                print("ERROR: File is not a supported format or is corrupted/empty")
            else:
                print('%d Candidates:' % len(candidates))
                text_utls.smart_print(options, candidates)
                if options.glossary_unused:
                    print("Possible Unused Glossary Enties:")
                    text_utls.smart_print(options, unused)


if __name__ == '__main__':
    pass
