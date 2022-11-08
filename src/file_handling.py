import json
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Union


def save_json(path: Path, container: Iterable) -> None:

    """write dict to path."""
    print(f"Saving json to {path}")
    with open(path, "w") as outfile:
        json.dump(container, outfile, ensure_ascii=False, indent=4)


def read_json(
    path: Path, encoding: Optional[str] = "utf-8", verbose: Optional[bool] = True
) -> Union[Dict, List]:
    """Read json file and return an utf-8 encoded dict."""
    if verbose:
        print(f"Reading json from {path}")
    with open(path, encoding=encoding, mode="r") as json_file:
        data: Union[Dict, List[Dict]] = json.load(json_file)
    return data
