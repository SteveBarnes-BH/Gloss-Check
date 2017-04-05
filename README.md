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
positional arguments:
  DOCS                  Word document(s) to check, (Wildcards OK).

optional arguments:
  -h, --help            show this help message and exit
  -L {de_DE,en_AU,en_GB,en_US,fr_FR}, -l {de_DE,en_AU,en_GB,en_US,fr_FR}, --lang {de_DE,en_AU,en_GB,en_US,fr_FR}
                        Language code to spell check against
  -M {2,3,4,5,6,7,8}, -m {2,3,4,5,6,7,8}, --min-acc {2,3,4,5,6,7,8}
                        Minimum Length for a possible glossary entry
  -u, -U, --upper_only  Only consider all uppercase strings as candidates.
  -C, -c, --chars_only  Exclude words with embedded numbers or symbols.
  -K, -k, --inc_camel   Include any word with upper any case after the first
                        letter.
  -o, -1, --one-per-line
                        Display in a single column
  -gu, -GU, --glossary-unused
                        Show unused entries from the glossary.
  -G GLOSSARY, -g GLOSSARY, --glossary GLOSSARY
                        An existing glossary to ignore
  -LL, -ll, --list-langs
                        List the available Language codes & exit
```
