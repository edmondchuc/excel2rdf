from rdflib import Graph, URIRef, Literal, Namespace, XSD
import pandas as pd
import validators

from uuid import uuid4
import re
from datetime import datetime


def is_curie(value):
    return re.fullmatch('\\S+:\\S+', value)


def is_datetime(value):
    return re.fullmatch('^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$', value)


def is_date(value):
    return re.fullmatch('^([1-9][0-9]{3})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])?$', value)


def _get_prefixes(df):
    prefixes = dict()
    base_uri = None
    g = Graph()

    for i, row in df.iterrows():
        if row.values[0].strip() == '#':
            prefixes.update({row.values[1]: row.values[2]})
            g.bind(row.values[1], Namespace(row.values[2]))
        elif row.values[0].strip() == '##':
            base_uri = row.values[1]

    return base_uri, prefixes, g


def _resolve_curie(curie, prefixes):
    try:
        if '.' in curie:
            curie = curie.split('.')[0]
        prefix, localname = curie.split(':')
    except Exception as e:
        raise Exception(str(e), curie)
    if not prefixes.get(prefix):
        raise Exception(f'Prefix {prefix} is not defined.')
    return URIRef(prefixes[prefix] + localname)


def _generate_uri(base_uri):
    return URIRef(base_uri + str(uuid4()))


def _add_object(value, prefixes):
    if not pd.isnull(value) and type(value) == str and value.__contains__(':'):
        if is_datetime(value):
            return Literal(value, datatype=XSD.dateTime)
        elif is_date(value):
            return Literal(value, datatype=XSD.date)
        elif validators.url(value):
            return URIRef(value)
        elif is_curie(value):
            return _resolve_curie(value, prefixes)
        else:
            pass

    # Check if it is a string literal and if it has a language tag.
    if type(value) == str and value.__contains__('@'):
        lang = value.split('@')[-1]
        value = value.split('@')[0]
        return Literal(value, lang=lang)

    return Literal(value)


def convert(df, base_uri, prefixes):
    g = Graph()

    for i, row in df.iterrows():
        uri = URIRef(row.uri) if not pd.isnull(row.uri) else _generate_uri(base_uri)

        for key in row.keys():
            if key != 'uri':
                if not pd.isnull(row[key]):
                    curie_value = _resolve_curie(key, prefixes)
                    object_value = _add_object(row[key], prefixes)
                    g.add((uri, curie_value, object_value))

    return g


def excel2rdf(file):
    prefixes_df = pd.read_excel(file, header=None, sheet_name='prefixes', engine='openpyxl')
    base_uri, prefixes, prefixes_g = _get_prefixes(prefixes_df)
    df = pd.read_excel(file, sheet_name=0, engine='openpyxl')
    g = convert(df, base_uri, prefixes) + prefixes_g

    return g
