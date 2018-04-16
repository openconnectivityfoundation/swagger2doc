# swagger2doc

swagger2doc tool

## description
This tool creates the documentation for an OCF resource in an supplied word document.

The tools needs to be called for each resource that needs to be added to the word document.


## installation
This tool is python3 based.

It should automatically install all the packages that it needs to run, or do it explicitly by running:

```python3 src\install.py```

just do an clone of the repository.
and use the tool relative of where the respository is located on your system.


## usage
from the src directory:

```python3 swagger2doc.py <options>```
use -h to see all the options.

```
usage: swagger2doc.py [-h] [-ver] [-swagger [SWAGGER]] [-schema [SCHEMA]]
                      [-docx [DOCX]] [-word_out [WORD_OUT]]
                      [-resource [RESOURCE]] [-schemadir [SCHEMADIR]]
                      [-derived DERIVED] [-annex ANNEX]

optional arguments:
  -h, --help            show this help message and exit
  -ver, --verbose       Execute in verbose mode
  -swagger [SWAGGER], --swagger [SWAGGER]
                        swagger file name
  -schema [SCHEMA], --schema [SCHEMA]
                        schema to be added to word document
  -docx [DOCX], --docx [DOCX]
                        word file in
  -word_out [WORD_OUT], --word_out [WORD_OUT]
                        word file out
  -resource [RESOURCE], --resource [RESOURCE]
                        resource (path) to be put in the word document
  -schemadir [SCHEMADIR], --schemadir [SCHEMADIR]
                        path to dir with additional referenced schemas
  -derived DERIVED, --derived DERIVED
                        derived data model specificaton (--derived XXX) e.g.
                        XXX Property Name in table use "." to ignore the
                        property name setting
  -annex ANNEX, --annex ANNEX
                        uses a annex heading instead of normal heading
                        (--annex true)

```
## enhancements

1.0.1 :
- added caption to table.
- text description of resources is now left alligned.
- added read-write when readOnly is not available on property.
- 4th column in property overview is now left alligned. 