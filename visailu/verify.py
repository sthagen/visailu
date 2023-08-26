#! /usr/bin/env python
"""Verify the YAML file for quiz data."""
import pathlib
import sys

import yaml


def main(path: str) -> int:
    """Drive the verification."""
    try:
        with pathlib.Path(path).open('rt', encoding='utf-8') as handle:
            _ = yaml.safe_load(handle)
    except (RuntimeError, yaml.scanner.ScannerError):
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
