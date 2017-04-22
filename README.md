### Welcome to GitHub Pages for Gloss-Check.
The intention of Gloss-Check is to make it easier to ensure that our documents contain **acurate** & **complete** glossaries with minimal effort.

The concept and original code for this project came from Steve Barnes, (@212303160), at GE Oil & Gas (UK) in Nailsea. It is coded in [Python](https://www.python.org/) and offers a [wxPython](https://wxpython.org/) GUI or a command line interface. A Windows compatible build is produced using pyinstaller and is available in [releases](./releases).

### Installation
On Windows simply download the zip of the desired release from [releases](./releases) and unzip it to a location that you wish to use it from, you can then invoke it from that location or add it to your path. **N.B.** The GUI build will only work in GUI mode but will not open a command window when started, the default build will.

On other platforms, *or Windows with python installed,* either get the latest source code, or the latest release, via git or the web interface. There are a number of dependencies which can be obtained by running: `pip install -r requries.txt`

### Command Line Usage

The basic command line usage of the console build is one of:

 - `gloss_check --help` - *to get the current options*
 - `gloss_check --version` - *to get version information*
 - `gloss_check [options] filename|wildcard [...]` - *to run with the selected options on the docx or doc files specified*.
 - `gloss_check` - *to start the GUI*

***The GUI build only offers the last option!***

The Options are given via the `gloss_check --help` command as:

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

### GUI Usage
Either start the GUI from the command line with `gloss_check`, double click on the `gloss_check.exe` file or add an icon to the desktop.

### Authors and Contributors
The following have contributed to the development of this package:

 - Steve Barnes, (@212303160), at GE Oil & Gas (UK) in Nailsea.

### Open Source Elements

This software uses the following Open Source components:

 - [Python](https://www.python.org/) Programming Language
 - [wxpython](https://wxpython.org/) GUI
 - [python-docx](https://github.com/python-openxml/python-docx) Docx Parsing.
 - [pywin32](http://sourceforge.net/projects/pypiwin32/) calling Word for Doc-Docx conversion.
 - [lxml](http://lxml.de/) XML Parsing
 - [pyenchant](https://pythonhosted.org/pyenchant/) Spell Checking
 - [pyinstaller](http://www.pyinstaller.org/) Windows compatible binary build.
