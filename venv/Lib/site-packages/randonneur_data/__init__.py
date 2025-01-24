__all__ = (
    "__version__",
    "Registry",
)

__version__ = "0.5.4"


import json
import lzma
import random
import shutil
from collections.abc import MutableMapping
from pathlib import Path
from typing import Any, Optional


DEFAULT_DATA_DIR = Path(__file__).parent.resolve() / "data"
DATA_LABELS = {"create", "replace", "update", "delete", "disaggregate"}


class Registry(MutableMapping):
    def __init__(self, filepath: Optional[Path] = None):
        self.registry_fp = filepath or DEFAULT_DATA_DIR / "registry.json"
        self.data_dir = self.registry_fp.parent

    def __load(self) -> dict:
        try:
            return json.load(open(self.registry_fp))
        except IOError:
            # Create if not present
            self.__save({})
            return {}

    def __save(self, data: dict) -> None:
        with open(self.registry_fp, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def __getitem__(self, key) -> Any:
        return self.__load()[key]

    def __setitem__(self, key, value) -> None:
        data = self.__load()
        data[key] = value
        self.__save(data)

    def __contains__(self, key) -> bool:
        return key in self.__load()

    def __str__(self) -> str:
        def format_file(obj: dict) -> str:
            licenses = [elem["name"] for elem in obj.get("licenses", [])]
            authors = ", ".join(
                [
                    f"{elem['title']} ({elem['role']})"
                    for elem in obj.get("contributors", [])
                ]
            )
            return f"""\t{obj['name']}
\t\tDescription: {obj['description']}
\t\tSource: {obj['source_id']}
\t\tTarget: {obj['target_id']}
\t\tGraph objects to be modified: {obj['graph_context']}
\t\tAuthors: {authors}
\t\tVersion: {obj.get("version", "(unknown)")}
\t\tLicenses: {licenses}
"""

        return f"`randonneur_data` with {len(self)} files:\n" + "".join(
            format_file(val) for val in sorted(self.values(), key=lambda x: x["name"].lower())
        )

    def __repr__(self) -> str:
        return f"`randonneur_data` registry at {str(self.data_dir)} with {len(self)} files and id {id(self)}"

    def __delitem__(self, name) -> None:
        data = self.__load()
        del data[name]

        self.__save(data)

    def __len__(self) -> int:
        return len(self.__load())

    def __iter__(self) -> Any:
        return iter(self.__load())

    def __hash__(self) -> int:
        return hash(self.__load())

    def validate_file(self, filepath: Path) -> None:
        try:
            from randonneur.validation import Contributors, MappingFields, DatapackageMetadata, validate_data_for_verb, VERBS
        except ImportError:
            raise ImportError("`validate_file` only available if `randonneur` has been installed.")

        data = json.load(open(filepath))
        for contributor in data['contributors']:
            Contributors(**contributor)
        MappingFields(**data.get("mapping", {}).get("source", {}))
        MappingFields(**data.get("mapping", {}).get("target", {}))
        DatapackageMetadata(**data)
        for verb in filter(lambda x: x in data, VERBS):
            validate_data_for_verb(verb, data[verb], data['mapping'])

    def add_file(self, filepath: Path, replace: bool = False) -> Path:
        """Add existing file to data repo."""
        if not isinstance(filepath, Path):
            filepath = Path(filepath)

        self.validate_file(filepath)

        new_path = self.data_dir / filepath.name
        if new_path.exists() and not replace:
            raise ValueError(f"File {new_path} already exists and `replace` is `False`")

        data = {
            k: v for k, v in json.load(open(filepath)).items() if k not in DATA_LABELS
        }

        size = filepath.stat().st_size
        if size > 2e5:
            data["filename"] = f"{new_path.stem}.xz"
            data["compression"] = "lzma"
            new_path = self.data_dir / data["filename"]
            with lzma.LZMAFile(
                new_path, mode="w", check=lzma.CHECK_SHA256, preset=9
            ) as lzma_file:
                lzma_file.write(open(filepath, "rb").read())
        else:
            data["filename"] = filepath.name
            data["compression"] = False
            shutil.copyfile(filepath, new_path)

        self[data["name"]] = data
        return new_path

    def sample(self, label: str, number: int = 2, verb: Optional[str] = None) -> dict:
        """
        Sample `number` transformations for each verb present in datapackage `label`.

        If `verb` is given, limit samples to that verb only.
        """
        data = self.get_file(label)
        if verb and verb not in data:
            raise KeyError("`{verb}` not given in datapackage `{label}`")
        elif verb:
            return {verb: random.sample(data[verb], min(number, len(data[verb])))}
        else:
            return {
                verb: random.sample(data[verb], min(number, len(data[verb])))
                for verb in DATA_LABELS
                if verb in data
            }

    def schema(self, label: str) -> dict:
        """
        Get mapping schema for datapackage `label`
        """
        return self.get_file(label)['mapping']

    def get_file(self, label: str) -> dict:
        metadata = self.__load()[label]
        if metadata.get("compression") == "lzma":
            return json.load(
                lzma.LZMAFile(
                    filename=self.data_dir / metadata["filename"],
                    mode="rb",
                )
            )
        else:
            return json.load(open(self.data_dir / metadata["filename"]))
