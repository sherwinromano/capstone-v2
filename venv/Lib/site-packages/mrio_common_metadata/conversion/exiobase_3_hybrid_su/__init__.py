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


DATA_DIR = Path(__file__, "..").resolve() / "data"
DATA_DIR.mkdir(exist_ok=True)


def convert_exiobase(sourcedir, version="3.3.17 hybrid"):
    sourcedir = Path(sourcedir)
    extract_metadata(sourcedir, version)
    extract_extension_exchanges(sourcedir, version)
    extract_production_exchanges(sourcedir, version)
    extract_io_exchanges(sourcedir, version)
    package_exiobase(version)


def package_exiobase(version):
    assert version == "3.3.17 hybrid"
    for resource in DATAPACKAGE["resources"]:
        resource["hash"] = md5(DATA_DIR / resource["path"])

    with open(DATA_DIR / "datapackage.json", "w") as f:
        json.dump(DATAPACKAGE, f, indent=2, ensure_ascii=False)

    fp = DATA_DIR / "exiobase-{}.tar".format(version.relocation(" ", "-"))

    with tarfile.open(fp, "w") as tar:
        for pth in DATA_DIR.iterdir():
            tar.add(DATA_DIR / pth, arcname=pth.name)


def load_metadata(kind):
    filepath = DATA_DIR / (kind + ".csv.bz2")
    with bz2.open(filepath, "rt") as compressed:
        data = list(csv.reader(compressed))
    return data


def extract_extension_exchanges(sourcedir, version):
    activities = load_metadata("activities")
    extensions = load_metadata("extensions")

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
        DATA_DIR / "extension-exchanges",
        get_numeric_data_iterator(data, extensions, activities, only_foreign_keys=True),
    )


def extract_su_exchanges(sourcedir, version, kind):
    activities = load_metadata("activities")
    products = load_metadata("products")

    dct = VERSIONS[version][kind]
    data = read_xlsb(
        sourcedir / dct["filename"],
        dct["worksheet"],
        pbar_total=len(activities) * len(products) + 4
    )

    headers = get_headers(data, len(activities), 8)

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

    write_compressed_csv(DATA_DIR / "production-exchanges", single_row_iterator())


def extract_io_exchanges(sourcedir, version):
    activities = load_metadata("activities")
    products = load_metadata("products")

    dct = VERSIONS[version]["technosphere"]

    wb = pyxlsb.open_workbook(str(sourcedir / dct["filename"]))
    sheet = iter(wb.get_sheet(dct["worksheet"]))

    def next_row(sheet):
        return [o.v for o in next(sheet)]

    headers = [next_row(sheet)[5:] for _ in range(4)]

    # activity location
    assert headers[0] == [x[1] for x in activities]
    # activity names
    assert headers[1] == [x[2] for x in activities]

    with bz2.open(DATA_DIR / "hiot.csv.bz2", "wt", newline="") as compressed:
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


def extract_metadata(sourcedir, version):
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
        write_compressed_csv(DATA_DIR / kind, data)
