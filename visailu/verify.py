"""Verify the YAML file for quiz data."""
import pathlib
from typing import Any, no_type_check

import yaml

from visailu import slugify


@no_type_check
def verify_path(path: str, options=None) -> tuple[int, str, Any]:
    """Verify the path points to a valid YAML file."""
    try:
        with pathlib.Path(path).open('rt', encoding='utf-8') as handle:
            data = yaml.safe_load(handle)
    except (RuntimeError, yaml.scanner.ScannerError) as err:
        message = f'path{path} is not a valid YAML file. Details: {slugify(str(err))}'
        return 1, message, {}
    return 0, '', data
