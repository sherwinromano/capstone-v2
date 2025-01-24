import bz2
import csv
import hashlib
import json
import pandas as pd


def md5(filepath, blocksize=65536):
    """Generate MD5 hash for file at `filepath`"""
    hasher = hashlib.md5()
    fo = open(filepath, "rb")
    buf = fo.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = fo.read(blocksize)
    return hasher.hexdigest()


def load_compressed_csv(filepath):
    with bz2.open(filepath, "rt") as compressed:
        data = list(csv.reader(compressed))
    return data


def load_compressed_csv_as_dataframe(filepath, exiobase_metadata=None):
    data = load_compressed_csv(filepath)
    if not exiobase_metadata:
        exiobase_metadata = json.load(open(filepath, "r"))
    table_metadata = [r for r in exiobase_metadata["resources"] if r["path"] == filepath.name][0]
    field_names = [d["name"] for d in table_metadata["schema"]["fields"]]
    key_field_name = table_metadata["schema"]["primaryKey"]
    df = pd.DataFrame(columns=field_names, data=data).set_index(key_field_name)
    return df


def iterate_compressed_csv(filepath):
    with bz2.open(filepath, "rt") as compressed:
        for row in csv.reader(compressed):
            yield row
