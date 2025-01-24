from .version import version as __version__

__all__ = (
    "get_migration",
    "migrate_data",
    "load_and_clean_exiobase_3_ecoinvent_36_migration",
)

import pandas as pd
from bw2data import Database
from .strategies import migrate_data, get_migration


def load_and_clean_exiobase_3_ecoinvent_36_migration(
    ecoinvent_biosphere_name=None, explode=False
):

    # load migration data
    migration = get_migration("exiobase-3-ecoinvent-3.6")

    # convert migration data into dataframe
    df = pd.DataFrame(
        [
            {"exiobase name": k[0], "exiobase compartment": k[1], "value": v}
            if isinstance(v, list)
            else {"exiobase name": k[0], "exiobase compartment": k[1], "value": [v]}
            for k, v in migration["data"]
        ]
    )

    # convert lists into individual rows
    df = df.explode("value").reset_index(drop=True)

    # convert dicts into individual columns
    df = df.join(df["value"].apply(pd.Series)).drop(columns=["value"])

    # rename columns
    df = df.rename(
        columns={
            "unit": "ecoinvent unit",
            "name": "ecoinvent name",
            "categories": "ecoinvent categories",
            "__multiplier__": "multiplier",
            "__disaggregation__": "disaggregation",
        }
    )

    # fill in missing data
    df = df.fillna(
        {
            "exiobase compartment": "undef",
            "ecoinvent name": df["exiobase name"],
            "disaggregation": 1,
            "ecoinvent categories": df["exiobase compartment"],
        }
    )

    # convert ecoinvent categories into tuples
    df.loc[:, "ecoinvent categories"] = df["ecoinvent categories"].apply(
        lambda x: tuple(x) if isinstance(x, list) else (x,)
    )

    # combine multiplier and disaggregation into one 'factor' column
    df["factor"] = df["multiplier"] * df["disaggregation"]

    # merge with ecoinvent biosphere to extract global flow indices
    if ecoinvent_biosphere_name is not None:
        df["biosphere index"] = df.merge(
            pd.DataFrame(
                Database(ecoinvent_biosphere_name)
            ),  # get ecoinvent biosphere as dataframe
            how="left",  # keep left index
            left_on=[
                "ecoinvent name",
                "ecoinvent categories",
                "ecoinvent unit",
            ],  # columns to merge on
            right_on=["name", "categories", "unit"],  # columns to merge on
        )["id"]

    # undo exploding for unique index
    if explode is False:
        df = df.groupby(["exiobase name", "exiobase compartment"], dropna=False).agg(
            list
        )

    return df


# def create_core_migrations():
#     """Add pre-defined core migrations data files"""
#     Migration("biosphere-2-3-categories").write(
#         get_biosphere_2_3_category_migration_data(),
#         "Change biosphere category and subcategory labels to ecoinvent version 3"
#     )
#     Migration("biosphere-2-3-names").write(
#         get_biosphere_2_3_name_migration_data(),
#         "Change biosphere flow names to ecoinvent version 3"
#     )
#     Migration("simapro-ecoinvent-3.1").write(
#         get_simapro_ecoinvent_3_migration_data("3.1"),
#         "Change SimaPro names from ecoinvent 3.1 to ecoinvent names"
#     )
#     Migration("simapro-ecoinvent-3.2").write(
#         get_simapro_ecoinvent_3_migration_data("3.2"),
#         "Change SimaPro names from ecoinvent 3.2 to ecoinvent names"
#     )
#     Migration("simapro-ecoinvent-3.3").write(
#         get_simapro_ecoinvent_3_migration_data("3.3"),
#         "Change SimaPro names from ecoinvent 3.3 to ecoinvent names"
#     )
#     Migration("simapro-water").write(
#         get_simapro_water_migration_data(),
#         "Change SimaPro water flows to more standard names"
#     )
#     Migration("us-lci").write(
#         get_us_lci_migration_data(),
#         "Fix names in US LCI database"
#     )
#     Migration("default-units").write(
#         get_default_units_migration_data(),
#         "Convert to default units"
#     )
#     Migration("unusual-units").write(
#         get_unusual_units_migration_data(),
#         "Convert non-Ecoinvent units"
#     )
#     Migration("exiobase-biosphere").write(
#         get_exiobase_biosphere_migration_data(),
#         "Change biosphere flow names to ecoinvent version 3"
#     )
#     Migration("fix-ecoinvent-flows-pre-35").write(
#         get_ecoinvent_pre35_migration_data(),
#         "Update new biosphere UUIDs in Consequential 3.4"
#     )
