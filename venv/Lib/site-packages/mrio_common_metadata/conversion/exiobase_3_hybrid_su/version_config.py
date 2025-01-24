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
                {
                    "filename": "Classifications_v_3_3_17.xlsx",
                    "worksheet": "waste",
                    "mapping": {
                        "Waste fractions": "name",
                        "Unit": "unit",
                    },
                    "kind": "waste",
                },
                {
                    "filename": "Classifications_v_3_3_17.xlsx",
                    "worksheet": "Crop_residues",
                    "mapping": {
                        "Category": "name",
                        "Unit": "unit",
                    },
                    "kind": "residue",
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
                        "Contry code": "location",  # Not a typo
                        "Activity name": "name",
                        "Activity code 1": "code 1",
                        "Activity code 2": "code 2",
                    },
                }
            ],
            "products": [
                {
                    "filename": "Classifications_v_3_3_17.xlsx",
                    "worksheet": "Products_HSUTs",
                    "mapping": {
                        "Country code": "location",
                        "Product name": "name",
                        "Product code 1": "code 1",
                        "product code 2": "code 2",
                        "unit": "unit",
                    },
                }
            ],
        },
        "supply": {
            "filename": "MR_HSUP_2011_v3_3_17.xlsb",
            "worksheet": "SUP",
        },
        "use": {
            "filename": "MR_HUSE_2011_v3_3_17.xlsb",
            "worksheet": "USE",
        },
        "final demand": {
            "filename": "MR_HFD_2011_v3_3_17.xlsb",
            "worksheet": "FD",
        },
        "stock to waste": {
            "filename": "MR_HFD_2011_v3_3_17.xlsb",
            "worksheet": "stock_to_waste",
        },
        "biosphere": {
            'avoided emissions due to manure': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'Avoided_emiss',
                'type': 'emission',
            },
            'Emis_unreg_w_FD': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'Emis_unreg_w_FD',
                'type': 'emission',
            },
            'Emis_unreg_w_act': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'Emis_unreg_w_act',
                'type': 'emission',
            },
            'Emiss_FD': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'Emiss_FD',
                'type': 'emission',
            },
            'Emiss_act': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'Emiss_act',
                'type': 'emission',
            },
            'Land_FD': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'Land_FD',
                'type': 'land_use',
            },
            'Land_act': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'Land_act',
                'type': 'land_use',
            },
            'crop_res_FD': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'crop_res_FD',
                'type': 'residue',
            },
            'crop_res_act': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'crop_res_act',
                'type': 'residue',
            },
            'mach_sup_waste_act': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'mach_sup_waste_act',
                'type': 'waste',
            },
            'mach_sup_waste_fd': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'mach_sup_waste_fd',
                'type': 'waste',
            },
            'mach_use_waste_act': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'mach_use_waste_act',
                'type': 'waste',
            },
            'mach_use_waste_fd': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'mach_use_waste_fd',
                'type': 'waste',
            },
            'pack_sup_waste_act': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'pack_sup_waste_act',
                'type': 'waste',
            },
            'pack_sup_waste_fd': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'pack_sup_waste_fd',
                'type': 'waste',
            },
            'pack_use_waste_act': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'pack_use_waste_act',
                'type': 'waste',
            },
            'pack_use_waste_fd': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'pack_use_waste_fd',
                'type': 'waste',
            },
            'resource_FD': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'resource_FD',
                'type': 'resource',
            },
            'resource_act': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'resource_act',
                'type': 'resource',
            },
            'stock_addition_act': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'stock_addition_act',
                'type': 'waste',
            },
            'stock_addition_fd': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'stock_addition_fd',
                'type': 'waste',
            },
            'waste_from_stock': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'waste_from_stock',
                'type': 'waste',
            },
            'waste_sup_FD': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'waste_sup_FD',
                'type': 'waste',
            },
            'waste_sup_act': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'waste_sup_act',
                'type': 'waste',
            },
            'waste_use_FD': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'waste_use_FD',
                'type': 'waste',
            },
            'waste_use_act': {
                'filename': 'MR_HSUT_2011_v3_3_17_extensions.xlsb',
                'worksheet': 'waste_use_act',
                'type': 'waste',
            },
        },
    }
}
