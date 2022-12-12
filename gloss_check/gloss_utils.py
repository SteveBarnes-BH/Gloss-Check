#!/usr/bin/env python
# encoding:utf-8
"""
  Author:  Steve Barnes --<Steven.Barnes@bhge.com>
  Purpose: Utility Functions for Glossary checking
  Created: 17/04/2017
"""
from __future__ import (
    print_function,
)
import sys
import os
import glob
import tempfile

try:
    import docx
except ImportError:
    docx = None
try:
    import textract
except ImportError:
    textract = None

try:
    import text_utls
    import docx2utils
    import xmltree_utils
    import doc2docx
except ImportError:
    from gloss_check import text_utls
    from gloss_check import docx2utils
    from gloss_check import xmltree_utils
    from gloss_check import doc2docx


def get_textract_wordlist(path, minacc=1):
    """
    Take the path of a file as an argument, return the list of words.
    """
    result = (False, [])
    if textract:
        try:
            wordlist = textract.process(path, "utf-8").split()
            result = (True, text_utls.clean_wordlist(wordlist, minacc))
        except (WindowsError, textract.exceptions.ExtensionNotSupported):
            result = (False, [])
    return result


def get_doc_wordlist(path, options):  # , extract_glossary=False):
    """
    Take the path of a doc file as argument, return the list of words.
    """
    docgloss = []
    print("Need to convert .doc to temporary .docx")
    tempdir = tempfile.gettempdir()
    temppath = os.path.join(tempdir, "gloss_check_temp.docx")
    if os.path.exists(temppath):
        os.remove(temppath)
    doc2docx.doc2docx(path, temppath)
    # Create a temprory copy of the doc as docx
    if docx is not None:
        success, cwordlist, docgloss = docx2utils.get_docx2_wordlist(temppath, options)
    else:
        success, cwordlist, docgloss = xmltree_utils.get_docx_tree_wordlist(
            temppath, options
        )
    if os.path.exists(temppath):
        os.remove(temppath)
        print("Removed", temppath)
    return success, cwordlist, docgloss


def get_candidates(path, extern_gloss=None, options=None):
    """
    Get glossary candidates from a Word Open Document Format file.

    Params:
        path: The path to the docx file.
        options: Options namespace including:
        upper_only: Only consider all upper case strings as candidates.
        inc_cammel: Include any word with upper case after the first.
        chars_only: Exclude words with embedded numbers or symbols.
        extern_gloss: An existing glossary to ignore.
        lang: Language code to spell check against.
    """
    success = False
    words = []
    doc_gloss = []
    method_dict = {  # Dictionary of methods to use for specific file extensions
        ".docx": xmltree_utils.get_docx_tree_wordlist,
        ".doc": get_doc_wordlist,
    }
    if docx is not None:  # docx library available so override method
        method_dict[".docx"] = docx2utils.get_docx2_wordlist
    method = method_dict.get(os.path.splitext(path)[-1].lower())
    candiates = []
    unused = []
    if method is not None:
        success, words, doc_gloss = method(path, options)
    elif textract is not None:
        success, words = get_textract_wordlist(path, options.min_acc)
    if success:
        candiates = text_utls.get_candidates_from_list(
            words, extern_gloss, doc_gloss, options
        )
        if options.glossary_unused:
            if options.table_gloss:
                unused = [item for item in doc_gloss if not item in words]
            else:
                unused = [item for item in extern_gloss if not item in words]
    return (
        success,
        candiates,
        unused,
        len(doc_gloss),
    )


def process_docs(options, ext_gloss):
    """Process the documents."""
    errors = []
    for arg in options.DOCS:
        print("Document/Wildcard:", arg)
        if os.path.isfile(arg):
            filelist = [
                arg,
            ]
        else:
            filelist = glob.glob(arg)
        if len(filelist) == 0:
            print("ERROR: No files match", arg)
        for filename in filelist:
            print("Processing", filename)
            success, candidates, unused, gloss_len = get_candidates(
                filename, ext_gloss, options=options
            )
            if not success:
                errors.append(
                    f"ERROR: File {filename} is not a supported format or is corrupted/empty"
                )
            else:
                print("%d Candidates:" % len(candidates))
                text_utls.smart_print(options, candidates)
                if options.glossary_unused:
                    print("Possible Unused Glossary Enties:")
                    text_utls.smart_print(options, unused)
                if (
                    options.fail_missing_count
                    and len(candidates) >= options.fail_missing_count
                ):
                    errors.append(
                        f"{len(candidates)} Undefined items > permitted in {filename}"
                    )
                if (
                    options.fail_unused_count
                    and len(unused) >= options.fail_unused_count
                ):
                    errors.append(
                        f"{len(unused)} Unused items > {options.fail_unused_count} permitted in {filename}"
                    )
        if errors:
            sys.exit("FAIL!\n" + "\n".join(errors))


if __name__ == "__main__":
    pass
