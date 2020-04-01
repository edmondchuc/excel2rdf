# Python excel2rdf

Generate RDF from Excel spreadsheets.


## Installation

```bash
pip3 install excel2rdf
```

## Usage
```bash
$ excel2rdf --help
Usage: excel2rdf [OPTIONS] INPUT_FILENAME OUTPUT_FILENAME

Options:
  -f TEXT  RDF format
  --help   Show this message and exit.
```

```bash
excel2rdf input.xlsx output.ttl
```

## Excel Formatting

The first sheet in the Excel document (Sheet1) can be named anything. It is used as the data table.

### Header

The first column of the header must be named `uri`. The value of the cells in the column `uri` will be the fully qualified URI of a resource for the given row. If left blank, **excel2rdf** will generate a random URI. 

The other columns of the header denote the *predicate* of the triple statement in [curie](https://www.w3.org/TR/2010/NOTE-curie-20101216/) format. The cell values can be either a curie or any literal value. 

#### Example Data Sheet

| uri                                                                  | rdf:type      | schema:name |
|----------------------------------------------------------------------|---------------|-------------|
|                                                                      | schema:Person | John Smith  |
| https://w3id.org/tern/resources/dada3918-f119-457b-a2e8-d10032ba44de | schema:Person | Jane Smith  |


### Prefix Declaration

A sheet named `prefixes` must exist. This sheet contains the prefix declarations. The first cell in the row must begin with a `#`. The second cell must be the prefix value and the third cell must be the fully qualified base URI of the prefix. 

A single base URI is declared with the first cell containing `##` and the second cell containing the base URI.

#### Example Prefix and Base URI Declaration

| ## | https://w3id.org/tern/resources/ |                                             |
|----|----------------------------------|---------------------------------------------|
| #  | schema                           | http://schema.org/                          |
| #  | rdf                              | http://www.w3.org/1999/02/22-rdf-syntax-ns# |


## Caveats

- The `.` character cannot be used in the headings of each column.