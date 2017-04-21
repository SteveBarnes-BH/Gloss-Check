# Gloss-Check
Check documents against a seperate glossary file to ensure that it covers all of the things that it should.

Usage:
------
Can be used either as a command line tool or without arguments will start a drag & drop GUI.

Current file types supported:
-----------------------------
As target files:

 - MS-Word .docx files, *even without MS-Word installed*
 - MS-Word .doc files   **Only** if a *recent* version of MS-Word is installed

As glossary files:

 - .txt  - All words found in the .txt files specified are assumed to be in your glossary.

```
usage: gloss_check.py [-h] [-L {NONE,de_DE,en_AU,en_GB,en_US,fr_FR}]
                      [-M {2,3,4,5,6,7,8}] [-u] [-C] [-K] [-o] [-T] [-gu] [-e]
                      [-G GLOSSARY] [-v] [-LL]
                      [DOCS [DOCS ...]]

Purpose: Find the candidates for the glossary in a word document. Author:
Steve Barnes --<StevenJohn.Barnes@ge.com> Created: 13/03/2017. Updated:
21/04/2017. Find the candidates for the glossary in a word document.

positional arguments:
  DOCS                  Word document(s) to check, (Wildcards OK).

optional arguments:
  -h, --help            show this help message and exit
  -L {NONE,de_DE,en_AU,en_GB,en_US,fr_FR}, -l {NONE,de_DE,en_AU,en_GB,en_US,fr_FR}, --lang {NONE,de_DE,en_AU,en_GB,en_US,fr_FR}
                        Language code to spell check against
  -M {2,3,4,5,6,7,8}, -m {2,3,4,5,6,7,8}, --min-acc {2,3,4,5,6,7,8}
                        Minimum Length for a possible glossary entry
  -u, -U, --upper_only  Only consider all uppercase strings as candidates.
  -C, -c, --chars_only  Exclude words with embedded numbers or symbols.
  -K, -k, --inc_camel   Include any word with upper any case after the first
                        letter.
  -o, -1, --one-per-line
                        Display in a single column
  -T, -t, --table_gloss
                        Search each document for possible glossary table.
  -gu, -GU, --glossary-unused
                        Show unused entries from the glossary, (document
                        glossary with -t).
  -e, -E, --etok        Enchant Tokanization
  -G GLOSSARY, -g GLOSSARY, --glossary GLOSSARY
                        An existing glossary to ignore
  -v, --version         Show version information and exit.
  -LL, -ll, --list-langs
                        List the available Language codes & exit
```
