import pandas as pd
import unicodecsv as csv
from faker import Factory
from collections import defaultdict
import ntpath

NUMERIC_TYPES = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
STRING_TYPES = ['object']


def get_date_fields(df):
    from dateutil.parser import parse
    date_fields = []
    for ii, v in enumerate(df.values[0]):
        try:
            parse(v)
            date_fields.append(fields[ii])
        except:
            pass
    return date_fields


def anonymize_rows_ex(rows):
    """
    Rows is an iterable of dictionaries that contain name and
    email fields that need to be anonymized.
    """
    # Load the faker and its providers
    faker  = Factory.create()

    # Create mappings of names & emails to faked names & emails.
    names  = defaultdict(faker.name)
    emails = defaultdict(faker.email)

    # Iterate over the rows and yield anonymized rows.
    for row in rows:
        # Replace the name and email fields with faked fields.
        row['name']  = names[row['name']]
        row['email'] = emails[row['email']]

        # Yield the row back to the caller
        yield row




def anonymize_rows(rows, fields_mapping):
    """
    """
    # Load the faker and its providers
    faker  = Factory.create()

    # Create mappings
    names  = defaultdict(faker.name)
    emails = defaultdict(faker.email)
    companies = defaultdict(faker.company)
    addresses = defaultdict(faker.address)

    # Iterate over the rows and yield anonymized rows.
    for row in rows:
        for string_field in fields_mapping:
            for k, v in fields_mapping.iteritems():
                if k == 'name':
                    for vi in v:
                        row[vi] = names[row[vi]]
                elif k == 'company':
                    for vi in v:
                        row[vi] = companies[row[vi]]
                elif k == 'address':
                    for vi in v:
                        row[vi] = addresses[row[vi]]
                elif k == 'email':
                    for vi in v:
                        row[vi] = emails[row[vi]]

        yield row


import os
import sys
import argparse
import numpy as np

def get_anonymous_fname(input_file):
    fpath = os.path.dirname(input_file)
    fname = ntpath.basename(input_file)
    output_fname = fname.split('.')[0] + '_anonymous.' + fname.split('.')[1]
    return os.path.join(fpath, output_fname)


def anonymize(input_file, output_file,  mapping_d):
    """
    :args input_file: path to the input CSV file
    :args output_file: path to the output CSV file
    :mapping_d: a dict of 'fake methods to list of fields in the CSV'
    """
    with open(input_file, 'rU') as f:
        with open(output_file, 'w') as o:
            reader = csv.DictReader(f)
            writer = csv.DictWriter(o, reader.fieldnames)
            writer.writeheader()
            for row in anonymize_rows(reader, mapping_d):
                writer.writerow(row)



def add_noise(fname):
    df = pd.read_csv(fname)

    df_types = df.dtypes
    for ii in range(len(df_types)):
        field = df_types.index[ii]
        field_type = df_types.values[ii]
        if field_type in NUMERIC_TYPES:

            np.random.normal(0,1,100)

            m = df[field].mean()
            s = df[field].std()
            if 'int' in str(field_type):
                df[field] = df[field].apply(
                    lambda x: x + int(abs(np.random.normal(m,s,1)[0])))
            else:
                df[field] = df[field].apply(
                    lambda x: x + abs(np.random.normal(m,s,1)[0]))


    df.to_csv(fname)


if __name__ == "__main__":
    argv = sys.argv[1:]
    parser = argparse.ArgumentParser(
        description="Input path to local file system were the data is saved.")
    parser.add_argument('--input_file', required=True)
    parser.add_argument('--name_fields', nargs='+', required=False)
    parser.add_argument('--company_fields', nargs='+',  required=False)
    parser.add_argument('--email_fields', nargs='+', required=False)
    parser.add_argument('--address_fields', nargs='+', required=False)

    opts = parser.parse_args(argv)
    input_file = opts.input_file
    mapping_d = {}
    if opts.name_fields: mapping_d['name'] = opts.name_fields
    if opts.company_fields: mapping_d['company'] = opts.company_fields
    if opts.email_fields: mapping_d['email'] = opts.email_fields
    if opts.address_fields: mapping_d['address'] = opts.address_fields

    output_file = get_anonymous_fname(input_file)

    anonymize(input_file, output_file, mapping_d)
    add_noise(output_file)
