from .version import version as __version__

__all__ = ("get_metadata_resource", "get_numeric_data_iterator", "list_resources")

from .utils import load_compressed_csv, iterate_compressed_csv
from pathlib import Path
import json


def _get_valid_dirpath(dirpath):
    dirpath = Path(dirpath)
    assert (dirpath / "datapackage.json").is_file()
    return dirpath


def _get_resources(dirpath):
    dirpath = _get_valid_dirpath(dirpath)
    return json.load(open(dirpath / "datapackage.json"))["resources"]


def _get_resource(dirpath, resource_name):
    resources = _get_resources(dirpath)
    assert len([r for r in resources if r["name"] == resource_name]) == 1
    return next(r for r in resources if r["name"] == resource_name)


def _get_foreign_key(dirpath, resource, field):
    fk = next(fk for fk in resource["foreignKeys"] if fk["fields"] == field)
    return (
        fk["reference"]["fields"],
        _get_resource(dirpath, fk["reference"]["resource"]),
    )


def list_resources(dirpath):
    return [resource["name"] for resource in _get_resources(dirpath)]


def get_metadata_resource(dirpath, resource_name):
    resource = _get_resource(dirpath, resource_name)
    names = [f["name"] for f in resource["schema"]["fields"]]
    data = load_compressed_csv(Path(dirpath) / resource["path"])
    return [dict(zip(names, row)) for row in data]


def get_numeric_data_iterator(dirpath, resource_name):
    resource = _get_resource(dirpath, resource_name)

    assert len(resource["foreignKeys"]) == 2

    row_id_field, row_resource = _get_foreign_key(
        dirpath, resource, resource["schema"]["fields"][0]["name"]
    )
    row_mapping = {
        elem[row_id_field]: elem
        for elem in get_metadata_resource(dirpath, row_resource["name"])
    }

    col_id_field, col_resource = _get_foreign_key(
        dirpath, resource, resource["schema"]["fields"][1]["name"]
    )
    col_mapping = {
        elem[col_id_field]: elem
        for elem in get_metadata_resource(dirpath, col_resource["name"])
    }

    for row, col, value in iterate_compressed_csv(Path(dirpath) / resource["path"]):
        yield row_mapping[row], col_mapping[col], float(value)


# DATA_DIR = Path(__file__, "..").resolve() / "data"
# DATA_DIR.mkdir(mode=0o777, exist_ok=True)


# class MissingDataPackage(Exception):
#     pass


# def _get_dir(label_or_filepath):
#     if (DATA_DIR / label_or_filepath).isdir():
#         return DATA_DIR / label_or_filepath
#     else:
#         dp = Path(label_or_filepath)
#         if not dp.isdir():
#             raise ValueError(f"{label_or_filepath} is not a recognized table or directory path")
#         return dp


# def get_datapackage(label_or_filepath):
#     """Load the contents of ``datapackage.json`` from a relative or absolute directory path"""
#     dp = _get_dir(label_or_filepath)
#     try:
#         return (dp, json.load(open(dp / "datapackage.json")))
#     except OSError:
#         raise MissingDataPackage(f"{label_or_filepath} is a directory, but `datapackage.json` is missing")


# def check_resources_integrity(label_or_filepath):
#     dp, resources = get_datapackage(label_or_filepath)
#     # TODO


# def check_resources_sentinel_values(label_or_filepath):
#     pass
#     # TODO


# def get_unique_resource(label_or_filepath, resource_name):
#     dp, resources = get_datapackage(label_or_filepath)
#     resource_possibilities = [o for o in resources if o['name'] == resource_name]

#     if not resource_possibilities:
#         raise ValueError(f"`{resource_name}` not found in this datapackage")
#     elif len(resource_possibilities) > 1:
#         raise ValueError(f"`{resource_name}` not unique in this datapackage")
#     else:
#         return dp, resource_possibilities[0]


# def get_labels(label_or_filepath, resource_name):
#     """Get row and column labels in the order used in this resource.

#     We do both at once to avoid loading the file twice."""
#     dp, resource = get_unique_resource(label_or_filepath, resource_name)

#     assert resource['mediatype'] == "text/csv+bz2"

#     row_raw, col_raw = [], []
#     rows_to_capture = max([field.get("row-index", 0) for field in itertools.chain(resource['schema']['rows'], resource['schema']['cols'])])
#     cols_to_capture = max([field.get("col-index", 0) for field in itertools.chain(resource['schema']['rows'], resource['schema']['cols'])])

#     with bz2.open(dp / resource['path'], "rt") as f:
#         reader = csv.reader(f)
#         for i, row in enumerate(reader):


#     row_offset_guess, col_offset_guess = get_offsets(filepath)
#     if row_offset is None:
#         row_offset = row_offset_guess
#     if col_offset is None:
#         col_offset = col_offset_guess


#     with bz2.open(filepath, "rt") as f:
#         reader = csv.reader(f)
#         col_labels = list(
#             itertools.zip_longest(
#                 *[row[col_offset:] for _, row in zip(range(row_offset), reader)]
#             )
#         )
#         row_labels = [row[:col_offset] for row in reader]

#     return row_labels, col_labels


# def get_data_iterator(label_or_filepath, resource_name, fill_missing=None):
#     with bz2.open(filepath, "rt") as f:
#         for i, row in enumerate(csv.reader(f)):
#             for j, value in enumerate(row):
#                 if i >= row_offset and j >= col_offset and value:
#                     if float(value) == 0:
#                     yield (i - row_offset, j - col_offset, float(value))
