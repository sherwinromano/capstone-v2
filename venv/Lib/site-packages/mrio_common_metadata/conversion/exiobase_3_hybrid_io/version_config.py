VERSIONS = {
    "3.3.17 hybrid": {
        "nomenclature": {
            "extensions": [
                {
                    "filename": "Classifications_v_3_3_17.xlsx",
                    "worksheet": "Resources",
                    "mapping": {"Resource name": "name", "Unit": "unit"},
                    "kind": "resource",
                },
                {
                    "filename": "Classifications_v_3_3_17.xlsx",
                    "worksheet": "Land",
                    "mapping": {"Land type": "name", "Unit": "unit"},
                    "kind": "land_use",
                },
                {
                    "filename": "Classifications_v_3_3_17.xlsx",
                    "worksheet": "Emissions",
                    "mapping": {
                        "Emission name": "name",
                        "Unit": "unit",
                        "Compartment": "compartment",
                    },
                    "kind": "emission",
                },
            ],
            "locations": [
                {
                    "filename": "Classifications_v_3_3_17.xlsx",
                    "worksheet": "Country",
                    "mapping": {"Country code": "code", "Country name": "name"},
                }
            ],
            "activities": [
                {
                    "filename": "Classifications_v_3_3_17.xlsx",
                    "worksheet": "Activities",
                    "mapping": {
                        "Contry code": "location",
                        "Activity name": "name",
                        "Activity code 1": "code 1",
                        "Activity code 2": "code 2",
                    },
                }
            ],
            "products": [
                {
                    "filename": "Classifications_v_3_3_17.xlsx",
                    "worksheet": "Products_HIOT",
                    "mapping": {
                        "Country code": "location",
                        "Product name": "name",
                        "Product code 1": "code 1",
                        "Product code 2": "code 2",
                        "Unit": "unit",
                    },
                }
            ],
        },
        "technosphere": {
            "filename": "Exiobase_MR_HIOT_2011_v3_3_17_by_prod_tech.xlsb",
            "worksheet": "HIOT",
        },
        "production": {
            "filename": "Exiobase_MR_HIOT_2011_v3_3_17_by_prod_tech.xlsb",
            "worksheet": "Principal_production_vector",
        },
        "biosphere": {
            "resource": {
                "filename": "MR_HIOT_2011_v3_3_17_extensions.xlsb",
                "worksheet": "resource_act",
            },
            "land_use": {
                "filename": "MR_HIOT_2011_v3_3_17_extensions.xlsb",
                "worksheet": "Land_act",
            },
            "emission": {
                "filename": "MR_HIOT_2011_v3_3_17_extensions.xlsb",
                "worksheet": "Emiss_act",
            },
        },
    },
    "3.3.18 hybrid": {
        "nomenclature": {
            "extensions": [
                {
                    "filename": "Classifications_v_3_3_18.xlsx",
                    "worksheet": "Resources",
                    "mapping": {"Resource name": "name", "Unit": "unit"},
                    "kind": "resource",
                },
                {
                    "filename": "Classifications_v_3_3_18.xlsx",
                    "worksheet": "Land",
                    "mapping": {"Land type": "name", "Unit": "unit"},
                    "kind": "land_use",
                },
                {
                    "filename": "Classifications_v_3_3_18.xlsx",
                    "worksheet": "Emissions",
                    "mapping": {
                        "Emission name": "name",
                        "Unit": "unit",
                        "Compartment": "compartment",
                    },
                    "kind": "emission",
                },
            ],
            "locations": [
                {
                    "filename": "Classifications_v_3_3_18.xlsx",
                    "worksheet": "Country",
                    "mapping": {"Country code": "code", "Country name": "name"},
                }
            ],
            "activities": [
                {
                    "filename": "Classifications_v_3_3_18.xlsx",
                    "worksheet": "Activities",
                    "mapping": {
                        "Contry code": "location",
                        "Activity name": "name",
                        "Activity code 1": "code 1",
                        "Activity code 2": "code 2",
                    },
                }
            ],
            "products": [
                {
                    "filename": "Classifications_v_3_3_18.xlsx",
                    "worksheet": "Products_HIOT",
                    "mapping": {
                        "Country code": "location",
                        "Product name": "name",
                        "Product code 1": "code 1",
                        "Product code 2": "code 2",
                        "Unit": "unit",
                    },
                }
            ],
        },
        "technosphere": {
            "filename": "MR_HIOT_2011_v3_3_18_by_product_technology.csv",
            "worksheet": "HIOT",
        },
        "production": {
            "filename": "MR_HIOT_2011_v3_3_18_principal_production.csv",
        },
        "biosphere": {
            "resource": {
                "filename": "MR_HIOT_2011_v3_3_18_extensions.xlsb",
                "worksheet": "resource_act",
            },
            "land_use": {
                "filename": "MR_HIOT_2011_v3_3_18_extensions.xlsb",
                "worksheet": "Land_act",
            },
            "emission": {
                "filename": "MR_HIOT_2011_v3_3_18_extensions.xlsb",
                "worksheet": "Emiss_act",
            },
        },
    }
}
