import pandas

from .datapackage import DATAPACKAGE
from .utils import (
    write_compressed_csv,
    extract_with_pandas,
    read_xlsb,
    get_numeric_data_iterator,
    get_headers,
    md5,
)
from .version_config import VERSIONS
from pathlib import Path
import bz2
import csv
import json
import pyxlsb
import tarfile
import scipy.sparse


def convert_exiobase(sourcedir, targetdir=None, version="3.3.17 hybrid"):

    # sanitize user input: sourcedir must be path
    if not isinstance(sourcedir, Path):
        sourcedir = Path(sourcedir)

    # default target directory = source directory/datapackage
    if targetdir is None:
        targetdir = sourcedir / "datapackage"
        targetdir.mkdir(exist_ok=True)

    # extract data
    extract_metadata(sourcedir, targetdir, version)
    extract_extension_exchanges(sourcedir, targetdir, version)
    extract_production_exchanges(sourcedir, targetdir, version)
    extract_io_exchanges(sourcedir, targetdir, version)

    # turn files into one datapackage
    package_exiobase(targetdir, version)

    # print and return path of datapackage
    print(f"Conversion successful: {targetdir}")
    return targetdir



def package_exiobase(targetdir, version, datafile=None, metafile=None, flush=True):
    assert version in version_config.VERSIONS.keys()

    # delete resource metadata for which no file is present
    DATAPACKAGE["resources"] = [r for r in DATAPACKAGE["resources"] if (targetdir / r["path"]).exists()]

    # create hash for each resource
    for resource in DATAPACKAGE["resources"]:
        resource["hash"] = md5(targetdir / resource["path"])

    # serialize metadata
    if metafile is None:
        metafile = targetdir / "datapackage.json"
    with open(targetdir / metafile, "w") as f:
        json.dump(DATAPACKAGE, f, indent=2, ensure_ascii=False)

    # add files to tar
    if datafile is None:
        datafile = targetdir / "exiobase-{}.tar".format(version.replace(" ", "-"))
    with tarfile.open(datafile, "w") as tar:
        for pth in targetdir.iterdir():
            if pth in [datafile, metafile]:
                continue
            else:
                # add file to tar
                tar.add(targetdir / pth, arcname=pth.name)
                # delete file
                if flush is True:
                    (targetdir / pth).unlink()


def load_metadata(kind, targetdir):
    filepath = targetdir / (kind + ".csv.bz2")
    with bz2.open(filepath, "rt") as compressed:
        data = list(csv.reader(compressed))
    return data


def extract_extension_exchanges(sourcedir, targetdir, version):
    activities = load_metadata("activities", targetdir)
    extensions = load_metadata("extensions", targetdir)

    dct = VERSIONS[version]["biosphere"]["resource"]
    resources = read_xlsb(sourcedir / dct["filename"], dct["worksheet"])

    dct = VERSIONS[version]["biosphere"]["land_use"]
    land_uses = read_xlsb(sourcedir / dct["filename"], dct["worksheet"])

    def drop_compartment(data):
        """Drop compartment label to get in consistent form with other extension matrices"""
        return [row[:2] + row[3:] for row in data]

    dct = VERSIONS[version]["biosphere"]["emission"]
    emissions = drop_compartment(
        read_xlsb(sourcedir / dct["filename"], dct["worksheet"])
    )

    # Check to make sure our metadata is valid
    resource_headers = get_headers(resources, len(activities), 4)
    land_headers = get_headers(land_uses, len(activities), 4)
    emission_headers = get_headers(emissions, len(activities), 4)

    assert resource_headers == land_headers == emission_headers
    # location
    assert resource_headers[0] == [x[1] for x in activities]
    # names
    assert resource_headers[1] == [x[2] for x in activities]

    data = resources + land_uses[4:] + emissions[4:]

    assert [row[1] for row in extensions] == [row[0] for row in data[4:]]
    assert [row[2] for row in extensions] == [row[1] for row in data[4:]]

    write_compressed_csv(
        targetdir / "extension-exchanges",
        get_numeric_data_iterator(data, extensions, activities, only_foreign_keys=True),
    )


def extract_production_exchanges(sourcedir, targetdir, version):
    activities = load_metadata("activities", targetdir)
    products = load_metadata("products", targetdir)

    dct = VERSIONS[version]["production"]
    if (sourcedir / dct["filename"]).suffix == '.xlsb':
        data = read_xlsb(sourcedir / dct["filename"], dct["worksheet"])
        headers = get_headers(data, len(activities), 8)
    elif (sourcedir / dct["filename"]).suffix == '.csv':
        data = pandas.read_csv(sourcedir / dct["filename"], header=None).transpose()
        headers = [data[i].to_list() for i in data.columns]


    # activity location
    assert headers[0] == [x[1] for x in activities]
    # activity names
    assert headers[1] == [x[2] for x in activities]
    # product location
    assert headers[0] == [x[1] for x in products]
    # product names
    assert headers[4] == [x[2] for x in products]

    def single_row_iterator():
        for index, value in enumerate(data[8][1:]):
            yield products[index][0], activities[index][0], value

    write_compressed_csv(targetdir / "production-exchanges", single_row_iterator())


def extract_io_exchanges(sourcedir, targetdir, version, sparse=True):
    activities = load_metadata("activities", targetdir)
    products = load_metadata("products", targetdir)

    dct = VERSIONS[version]["technosphere"]

    # load data
    file = sourcedir / dct["filename"]
    if file.suffix == ".csv":

        # read data
        df = pandas.read_csv(file, index_col=list(range(5)), header=list(range(4)))

        # name indices and columns
        df.index.names = ['location', 'product', 'product code 1', 'product code 2', 'unit']
        df.columns.names = ['location', 'activity', 'activity code 1', 'activity code 2']

        # check if order of locations and products is correct
        # activity locations
        assert df.columns.get_level_values('location').to_list() == [x[1] for x in activities]
        # activity names
        assert df.columns.get_level_values('activity').to_list() == [x[2] for x in activities]
        # product location
        assert df.index.get_level_values('location').to_list() == [x[1] for x in products]
        # product name
        assert df.index.get_level_values('product').to_list() == [x[2] for x in products]

        # write sparse matrix to npz
        if sparse is True:
            sparse_matrix = scipy.sparse.coo_matrix(df.values)
            scipy.sparse.save_npz(targetdir / "hiot.npz", sparse_matrix)
        # write dense matrix to compressed csv
        else:
            with bz2.open(targetdir / "hiot.csv.bz2", "wt", newline="") as compressed:
                writer = csv.writer(compressed)
                writer.writerows(df.values)
    else:
        wb = pyxlsb.open_workbook(str(sourcedir / dct["filename"]))
        sheet = iter(wb.get_sheet(dct["worksheet"]))

        def next_row(sheet):
            return [o.v for o in next(sheet)]

        headers = [next_row(sheet)[5:] for _ in range(4)]

        # activity location
        assert headers[0] == [x[1] for x in activities]
        # activity names
        assert headers[1] == [x[2] for x in activities]

        with bz2.open(targetdir / "hiot.csv.bz2", "wt", newline="") as compressed:
            writer = csv.writer(compressed)

            for row_index, row_raw in enumerate(sheet):
                if not row_index % 250:
                    print("{} / {}".format(row_index, len(activities)))

                row = [o.v for o in row_raw]
                assert row[0] == products[row_index][1]
                assert row[1] == products[row_index][2]

                for col_index, value in enumerate(row[5:]):
                    if value:
                        writer.writerow(
                            (products[row_index][0], activities[col_index][0], value)
                        )


def extract_metadata(sourcedir, targetdir, version):
    def reformat_extension(record, obj):
        return (
            "{}-{}".format(obj["kind"], record["name"]),
            record["name"],
            record["unit"],
            record.get("compartment"),
            obj["kind"],
        )

    def reformat_location(record, obj):
        return (record["code"], record["name"])

    def reformat_activity(record, obj):
        return (
            "{}-{}".format(record["location"], record["name"]),
            record["location"],
            record["name"],
            record["code 1"],
            record["code 2"],
        )

    def reformat_product(record, obj):
        return (
            "{}-{}".format(record["location"], record["name"]),
            record["location"],
            record["name"],
            record["code 1"],
            record["code 2"],
            record["unit"],
        )

    config = {
        "extensions": reformat_extension,
        "locations": reformat_location,
        "products": reformat_product,
        "activities": reformat_activity,
    }

    for kind, func in config.items():
        data = []
        for obj in VERSIONS[version]["nomenclature"][kind]:
            mapping = obj["mapping"]
            for record in extract_with_pandas(
                sourcedir / obj["filename"], obj["worksheet"]
            ):
                record = {mapping[k.strip()]: v for k, v in record.items()}
                data.append(func(record, obj))
        write_compressed_csv(targetdir / kind, data)
