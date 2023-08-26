"""Verify the YAML file for quiz data."""
import pathlib
from typing import no_type_check

import yaml

from visailu import log, slugify


@no_type_check
def verify(path: str, options=None) -> bool:
    """Verify the path points to a valid YAML file."""
    try:
        with pathlib.Path(path).open('rt', encoding='utf-8') as handle:
            _ = yaml.safe_load(handle)
    except (RuntimeError, yaml.scanner.ScannerError) as err:
        log.error(f'path{path} is not a valid YAML file. Details: {slugify(str(err))}')
        return False
    return True
