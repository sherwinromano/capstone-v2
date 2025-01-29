DATAPACKAGE = {
    "name": "EXIOBASE 3.3.17 Hybrid",
    "id": "exiobase-3.3.17-hybrid",
    "licenses": [
        {
            "name": "CC-BY-SA-4.0",
            "path": "https://creativecommons.org/licenses/by-sa/4.0/",
            "title": "Creative Commons Attribution Share-Alike 4.0",
        }
    ],
    "description": """The hybrid supply-use and input-output tables of EXOBASE are available for the year 2011. When new data become available the hybrid supply-use and input-output tables may be generated. The latest version can be identified by its version number and its advised to use this latest version. Previous versions will still be available for reference purpose.

References:

* Merciai, Stefano, and Jannick Schmidt. 2016. [Physical/Hybrid Supply and Use Tables. Methodological Report. EU FP7 DESIRE Project](http://fp7desire.eu/documents/category/3-public-deliverables).
* Merciai, Stefano, and Jannick Schmidt. 2018. [Methodology for the Construction of Global Multi-Regional Hybrid Supply and Use Tables for the EXIOBASE v3 Database](https://onlinelibrary.wiley.com/doi/full/10.1111/jiec.12713). Journal of Industrial Ecology 22, no. 3 (2018): 516–31. doi:10.1111/jiec.12713.""",
    "version": "3.3.17",
    "sources": [
        {
            "title": "EXIOBASE raw data download",
            "path": "https://exiobase.eu/index.php/data-download/exiobase3hyb/125-exiobase-3-3-17-hsut-2011",
        }
    ],
    "contributors": [
        {
            "title": "Chris Mutel",
            "email": "cmutel@gmail.com",
            "path": "https://chris.mutel.org/",
            "role": "author",
        }
    ],
    "image": "https://exiobase.eu/images/basisafbeeldingen/ExioBase_Logo_600.png",
    "resources": [
        {
            "name": "extensions",
            "path": "extensions.csv.bz2",
            "profile": "tabular-data-resource",
            "mediatype": "text/csv+bz2",
            "title": "Environmental Extensions",
            "format": "csv",
            "schema": {
                "fields": [
                    {"name": "id"},
                    {"name": "name"},
                    {"name": "unit"},
                    {
                        "name": "compartment",
                        "type": ["string", None],
                        "description": "The environmental compartment; used only for emissions",
                    },
                    {
                        "name": "kind",
                        "type": "string",
                        "description": "The kind of environmental extension, e.g. resource consumption, land use, emission",
                    },
                ],
                "primaryKey": "id",
            },
        },
        {
            "name": "products",
            "path": "products.csv.bz2",
            "profile": "tabular-data-resource",
            "mediatype": "text/csv+bz2",
            "title": "Products (for HIOT)",
            "format": "csv",
            "schema": {
                "fields": [
                    {"name": "id"},
                    {"name": "location"},
                    {"name": "name"},
                    {"name": "code 1"},
                    {"name": "code 2"},
                    {"name": "unit"},
                ],
                "primaryKey": "id",
            },
        },
        {
            "name": "activities",
            "path": "activities.csv.bz2",
            "profile": "tabular-data-resource",
            "mediatype": "text/csv+bz2",
            "title": "Activities",
            "format": "csv",
            "schema": {
                "fields": [
                    {"name": "id"},
                    {"name": "location"},
                    {"name": "name"},
                    {"name": "code 1"},
                    {"name": "code 2"},
                ],
                "primaryKey": "id",
            },
        },
        {
            "name": "locations",
            "path": "locations.csv.bz2",
            "profile": "tabular-data-resource",
            "mediatype": "text/csv+bz2",
            "title": "Locations",
            "description": "ISO 31622-2 country code, plus custom EXIOBASE locations",
            "format": "csv",
            "schema": {
                "fields": [{"name": "code"}, {"name": "name"}],
                "primaryKey": "code",
            },
        },
        {
            "name": "extension-exchanges",
            "path": "extension-exchanges.csv.bz2",
            "profile": "tabular-data-resource",
            "mediatype": "text/csv+bz2",
            "title": "Extension exchange values",
            "format": "csv",
            "schema": {
                "fields": [
                    {"name": "extension"},
                    {"name": "activity"},
                    {"name": "value", "type": "number"},
                ]
            },
            "foreignKeys": [
                {
                    "fields": "extension",
                    "reference": {"resource": "extensions", "fields": "id"},
                },
                {
                    "fields": "activity",
                    "reference": {"resource": "activities", "fields": "id"},
                },
            ],
        },
        {
            "name": "production-exchanges",
            "path": "production-exchanges.csv.bz2",
            "profile": "tabular-data-resource",
            "mediatype": "text/csv+bz2",
            "title": "Diagonal principal production values",
            "format": "csv",
            "schema": {
                "fields": [
                    {"name": "product"},
                    {"name": "activity"},
                    {"name": "value", "type": "number"},
                ]
            },
            "foreignKeys": [
                {
                    "fields": "product",
                    "reference": {"resource": "products", "fields": "id"},
                },
                {
                    "fields": "activity",
                    "reference": {"resource": "activities", "fields": "id"},
                },
            ],
        },
        {
            "name": "hiot",
            "path": "hiot.csv.bz2",
            "profile": "tabular-data-resource",
            "mediatype": "text/csv+bz2",
            "title": "Values from Input-Output table (excluding production)",
            "format": "csv",
            "schema": {
                "fields": [
                    {"name": "product"},
                    {"name": "activity"},
                    {"name": "value", "type": "number"},
                ]
            },
            "foreignKeys": [
                {
                    "fields": "product",
                    "reference": {"resource": "products", "fields": "id"},
                },
                {
                    "fields": "activity",
                    "reference": {"resource": "activities", "fields": "id"},
                },
            ],
        },
    ],
}
