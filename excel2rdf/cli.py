import click

from excel2rdf import excel2rdf


@click.command()
@click.argument('input_filename')
@click.argument('output_filename')
@click.option('-f', 'format', help='RDF format', type=str, default='turtle')
# @click.option('-f', 'file', help='The Excel file to be processed', type=str, required=True)
def main(input_filename, output_filename, format):
    g = excel2rdf(input_filename)
    g.serialize(output_filename, format=format)


if __name__ == '__main__':
    main()
