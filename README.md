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

The other columns of the header denote the _predicate_ of the triple statement in [curie](https://www.w3.org/TR/2010/NOTE-curie-20101216/) format. The cell values can be either a curie or any literal value.

#### Example Data Sheet

The following table demonstrates the usage of the same property `skos:prefLabel` across many columns with values in different language tags.

| uri                           | rdf:type     | skos:prefLabel | skos:prefLabel | skos:prefLabel | skos:prefLabel |
| ----------------------------- | ------------ | -------------- | -------------- | -------------- | -------------- |
| https://example.com/concept/m | skos:Concept | metre          | meter@en-us    | metre@en-gb    | metre@en-au    |

Output:

```ttl
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

<https://example.com/concept/m> a skos:Concept ;
    skos:prefLabel "metre",
        "metre"@en-au,
        "metre"@en-gb,
        "meter"@en-us .
```

### Prefix Declaration

A sheet named `prefixes` must exist. This sheet contains the prefix declarations. The first cell in the row must begin with a `#`. The second cell must be the prefix value and the third cell must be the fully qualified base URI of the prefix.

A single base URI is declared with the first cell containing `##` and the second cell containing the base URI.

#### Example Prefix and Base URI Declaration

| ##  | https://example.com/concept/ |                                             |
| --- | ---------------------------- | ------------------------------------------- |
| #   | skos                         | http://www.w3.org/2004/02/skos/core#        |
| #   | rdf                          | http://www.w3.org/1999/02/22-rdf-syntax-ns# |

### Full Excel Spreadsheet Example

See [examples/manufacturers.xlsx](https://github.com/edmondchuc/excel2rdf/blob/master/examples/manufacturers.xlsx) for a full example.

## Caveats

- The `.` character cannot be used in the headings of each column.
