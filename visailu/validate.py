"""Validate the YAML file against the model for quiz data."""
import pathlib
from typing import Any, no_type_check

import yaml

from visailu import (
    INVALID_YAML_RESOURCE,
    MODEL_META_INVALID_DEFAULTS,
    MODEL_META_INVALID_RANGE,
    MODEL_META_INVALID_RANGE_VALUE,
    MODEL_QUESTION_ANSWER_MISSING,
    MODEL_QUESTION_ANSWER_MISSING_RATING,
    MODEL_QUESTION_INCOMPLETE,
    MODEL_QUESTION_INVALID_RANGE,
    MODEL_QUESTION_INVALID_RANGE_VALUE,
    MODEL_STRUCTURE_UNEXPECTED,
    MODEL_VALUES_MISSING,
    log,
)
from visailu.verify import verify as verify_path


@no_type_check
def load(path: str):
    """Load the data structure from YAML file at path."""
    with pathlib.Path(path).open('rt', encoding='utf-8') as handle:
        return yaml.safe_load(handle)


@no_type_check
def parse_scale_range(scale) -> tuple[bool | float | None, list[Any]]:
    """Parse a scale range declaration.
    Returns a tuple (ordered pair) of target type and target range
    target range: Expecting either a list (ordered pair) with low and high or
    a string value from magic keywords to derive such a pair from.
    A failed parse returns tuple with None and an empty list.
    Any target range given as list on input is understood as logical values.
    """
    maps_to = scale.get('range', None)
    if maps_to is None:
        return None, []
    if isinstance(maps_to, list):
        if len(maps_to) != 2:
            return None, []
        return bool, maps_to  # As documented
    type_code = maps_to.lower().strip()
    if type_code in ('binary', 'bool', 'boolean'):
        return bool, [False, True]
    if type_code in ('fract', 'fraction', 'relative'):
        return float, [0, 1]
    if type_code in ('perc', 'percentage'):
        return float, [0, 100]
    return None, []


@no_type_check
def effective_meta(data, entry):
    """Walk upwards until meta discovered."""
    meta = entry.get('meta')
    if meta is None:
        meta = data.get('meta')
    return meta


@no_type_check
def parse_defaults(meta):
    """Parse the effective defaults from the meta data."""
    defaults = meta.get('defaults')
    if defaults:
        default_rating = defaults.get('rating', None)
        target_type, maps_to = parse_scale_range(meta.get('scale'))
        return target_type, maps_to, default_rating
    return None, [], None


@no_type_check
def validate_defaults(target_type, maps_to, default_rating):
    """Validate the default for consistency."""
    if target_type is None or not maps_to:
        return False, MODEL_META_INVALID_RANGE
    if target_type is bool:
        if default_rating not in maps_to:
            return False, MODEL_META_INVALID_RANGE_VALUE
    if target_type is float:
        try:
            val = float(default_rating)
            if not isinstance(default_rating, (int, float)) or default_rating is False or default_rating is True:
                return False, MODEL_META_INVALID_RANGE_VALUE
        except (TypeError, ValueError):
            return False, MODEL_META_INVALID_RANGE_VALUE
        if not maps_to[0] <= val <= maps_to[1]:
            return False, MODEL_META_INVALID_RANGE_VALUE
    return True, ''


def _validate(path: str) -> tuple[bool, str]:
    """Validate the data against the model."""
    try:
        data = load(path)
    except RuntimeError:
        return False, INVALID_YAML_RESOURCE

    try:
        identity = data.get('id')
        title = data.get('title', '')
        questions = data.get('questions', [])
    except (AttributeError, RuntimeError):
        return False, MODEL_STRUCTURE_UNEXPECTED

    if not all(aspect for aspect in (identity, title, questions)):
        return False, MODEL_VALUES_MISSING

    for entry in questions:
        question = entry.get('question', '')
        answers = entry.get('answers', [])
        meta = effective_meta(data, entry)
        target_type, maps_to, default_rating = parse_defaults(meta)
        if target_type is None:
            return False, MODEL_META_INVALID_DEFAULTS
        ok, message = validate_defaults(target_type, maps_to, default_rating)
        if not ok:
            return ok, message
        if target_type is None or not maps_to:
            return False, MODEL_META_INVALID_RANGE
        if target_type is bool:
            if default_rating not in maps_to:
                return False, MODEL_META_INVALID_RANGE_VALUE
        if target_type is float:
            try:
                val = float(default_rating)
                if not isinstance(default_rating, (int, float)) or default_rating is False or default_rating is True:
                    return False, MODEL_META_INVALID_RANGE_VALUE
            except (TypeError, ValueError):
                return False, MODEL_META_INVALID_RANGE_VALUE
            if not maps_to[0] <= val <= maps_to[1]:
                return False, MODEL_META_INVALID_RANGE_VALUE

        if not all(aspect for aspect in (question, answers)):
            return False, MODEL_QUESTION_INCOMPLETE

        for option in answers:
            answer = option.get('answer', '')
            rating = option.get('rating')
            if rating is None:
                rating = default_rating
            if target_type is bool:
                if rating not in maps_to:
                    return False, MODEL_QUESTION_INVALID_RANGE
            if target_type is float:
                try:
                    val = float(rating)
                    if not isinstance(rating, (int, float)) or rating is False or rating is True:
                        return False, MODEL_QUESTION_INVALID_RANGE_VALUE
                except (TypeError, ValueError):
                    return False, MODEL_QUESTION_INVALID_RANGE_VALUE
                if not maps_to[0] <= val <= maps_to[1]:
                    return False, MODEL_QUESTION_INVALID_RANGE_VALUE
            if not answer:
                return False, MODEL_QUESTION_ANSWER_MISSING
            if rating is None:
                return False, MODEL_QUESTION_ANSWER_MISSING_RATING

    return True, ''


@no_type_check
def validate(path: str, options=None) -> tuple[bool, str]:
    """Drive the model validation."""
    if not verify_path(path):
        return False, INVALID_YAML_RESOURCE

    ok, message = _validate(path)
    if not ok:
        log.error(f'path({path}) {message}')
        return ok, message

    log.info(f'path({path}) is valid quiz data')
    return ok, ''
