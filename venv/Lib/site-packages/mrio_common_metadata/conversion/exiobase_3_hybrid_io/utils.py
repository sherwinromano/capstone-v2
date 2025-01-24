from pathlib import Path
import bz2
import csv
import hashlib
import pandas as pd
import pyxlsb


def read_xlsb(filepath, worksheet):
    wb = pyxlsb.open_workbook(str(filepath))
    sheet = wb.get_sheet(worksheet)
    return [[o.v for o in row] for row in sheet.rows()]


def convert_xlsb(workbook, worksheet, sourcedir, targetdir):
    wb = pyxlsb.open_workbook(workbook)
    sheet = wb.get_sheet(worksheet)

    directory = CONVERTED_DATA_DIR / Path(workbook).name.replace(".xlsb", "")
    directory.mkdir(mode=0o755, exist_ok=True)

    with bz2.open(directory / (worksheet + ".csv.bz2"), "wt", newline="") as compressed:
        writer = csv.writer(compressed)
        for i, row in enumerate(sheet.rows()):
            writer.writerow([c.v for c in row])
            if i and not i % 250:
                print(f"Row {i}")


def extract_with_pandas(filepath, worksheet):
    return pd.read_excel(filepath, sheet_name=worksheet).to_dict(orient="records")


def write_compressed_csv(filepath, data):
    filepath = str(filepath)
    if not filepath.endswith(".csv.bz2"):
        filepath += ".csv.bz2"

    with bz2.open(filepath, "wt", newline="") as compressed:
        writer = csv.writer(compressed)
        for row in data:
            writer.writerow(row)


def get_numeric_data_iterator(
    data, rows, cols, skip_zeros=True, only_foreign_keys=False
):
    row_offset = len(data) - len(rows)
    col_offset = len(data[0]) - len(cols)
    for row_index, row_data in enumerate(data[row_offset:]):
        for col_index, value in enumerate(row_data[col_offset:]):
            if value or not skip_zeros:
                if only_foreign_keys:
                    yield (rows[row_index][0], cols[col_index][0], value)
                else:
                    yield (rows[row_index], cols[col_index], value)


def get_headers(data, cols, rows):
    return [row[-cols:] for row in data[:rows]]


def md5(filepath, blocksize=65536):
    """Generate MD5 hash for file at `filepath`"""
    hasher = hashlib.md5()
    fo = open(filepath, "rb")
    buf = fo.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = fo.read(blocksize)
    return hasher.hexdigest()
