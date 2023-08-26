#! /usr/bin/env python
"""Publish a valid YAML model as application specific JSON.

Target format is a naive 10 question array with 4 options each array:
[
  {
    "id": 1,
    "question": "A",
    "options": [
      { "answer": "1", "isCorrect": false },
      { "answer": "2", "isCorrect": false },
      { "answer": "3", "isCorrect": true },
      { "answer": "4", "isCorrect": false }
    ]
  },
  ...
  {
    "id": 10,
    "question": "J",
    "options": [
      { "answer": "a", "isCorrect": false },
      { "answer": "b", "isCorrect": false },
      { "answer": "c", "isCorrect": true },
      { "answer": "d", "isCorrect": false }
    ]
  },
]
"""
import json
import pathlib
import sys
from typing import Any, Union, no_type_check

import yaml

AnswerExportType = list[dict[str, Union[str, bool]]]
QuestionExportType = dict[str, Union[int, str, AnswerExportType]]
QuizExportType = list[QuestionExportType]

INVALID_YAML_RESOURCE = 'is invalid yaml or the resource is inaccessible'
MODEL_META_INVALID_DEFAULTS = 'contains invalid defaults for scale in meta'
MODEL_META_INVALID_RANGE = 'contains an invalid range of scale in meta'
MODEL_META_INVALID_RANGE_VALUE = 'contains an invalid default value for the scale'
MODEL_QUESTION_ANSWER_MISSING = 'misses an answer'
MODEL_QUESTION_ANSWER_MISSING_RATING = 'misses a rating for an answer'
MODEL_QUESTION_INCOMPLETE = 'has incomplete questions'
MODEL_QUESTION_INVALID_RANGE = 'contains an invalid range value for the scale'
MODEL_QUESTION_INVALID_RANGE_VALUE = 'contains an invalid answer rating for the scale'
MODEL_STRUCTURE_UNEXPECTED = 'has unexpected model structure'
MODEL_VALUES_MISSING = 'misses model values'


@no_type_check
def load(path: str):
    """Load the data structure from YAML file at path."""
    with pathlib.Path(path).open('rt', encoding='utf-8') as handle:
        return yaml.safe_load(handle)


def verify(path: str) -> bool:
    """Drive the verification."""
    try:
        load(path)
    except (RuntimeError, yaml.scanner.ScannerError):
        return False
    return True


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


def validate(path: str) -> tuple[bool, str]:
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


def etl(path: str) -> tuple[bool, str, Union[QuizExportType, list]]:
    """Extract, load, and transform the data."""
    try:
        data = load(path)
    except RuntimeError:
        return False, INVALID_YAML_RESOURCE, []

    try:
        identity = data.get('id')
        title = data.get('title', '')
        questions = data.get('questions', [])
    except (AttributeError, RuntimeError):
        return False, MODEL_STRUCTURE_UNEXPECTED, []

    if not all(aspect for aspect in (identity, title, questions)):
        return False, MODEL_VALUES_MISSING, []

    id_export = 1
    quiz_export: QuestionExportType = []
    for entry in questions:
        question = entry.get('question', '')
        answers = entry.get('answers', [])
        meta = effective_meta(data, entry)
        target_type, maps_to, default_rating = parse_defaults(meta)
        if target_type is None:
            return False, MODEL_META_INVALID_DEFAULTS, []
        ok, message = validate_defaults(target_type, maps_to, default_rating)
        if not ok:
            return ok, message
        if target_type is None or not maps_to:
            return False, MODEL_META_INVALID_RANGE, []
        if target_type is bool:
            if default_rating not in maps_to:
                return False, MODEL_META_INVALID_RANGE_VALUE, []
        if target_type is float:
            try:
                val = float(default_rating)
                if not isinstance(default_rating, (int, float)) or default_rating is False or default_rating is True:
                    return False, MODEL_META_INVALID_RANGE_VALUE, []
            except (TypeError, ValueError):
                return False, MODEL_META_INVALID_RANGE_VALUE, []
            if not maps_to[0] <= val <= maps_to[1]:
                return False, MODEL_META_INVALID_RANGE_VALUE, []

        if not all(aspect for aspect in (question, answers)):
            return False, MODEL_QUESTION_INCOMPLETE, []

        question_export = {
            'id': id_export,
            'question': question,
            'options': [],
        }
        for option in answers:
            answer = option.get('answer', '')
            rating = option.get('rating')
            if rating is None:
                rating = default_rating
            if target_type is bool:
                if rating not in maps_to:
                    return False, MODEL_QUESTION_INVALID_RANGE, []
            if target_type is float:
                try:
                    val = float(rating)
                    if not isinstance(rating, (int, float)) or rating is False or rating is True:
                        return False, MODEL_QUESTION_INVALID_RANGE_VALUE, []
                except (TypeError, ValueError):
                    return False, MODEL_QUESTION_INVALID_RANGE_VALUE, []
                if not maps_to[0] <= val <= maps_to[1]:
                    return False, MODEL_QUESTION_INVALID_RANGE_VALUE, []
            if not answer:
                return False, MODEL_QUESTION_ANSWER_MISSING, []
            if rating is None:
                return False, MODEL_QUESTION_ANSWER_MISSING_RATING, []
            question_export['options'].append({'answer': answer, 'isCorrect': rating})
        quiz_export.append(question_export)
        id_export += 1
        if id_export > 10:
            break

    return True, '', quiz_export


def main(path: str) -> int:
    """Drive the model publication."""
    if not verify(path):
        print(f'path({path}) is no well-formed yaml')
        return 2

    ok, message = validate(path)
    if not ok:
        print(f'path({path}) {message}')
        return 1

    print(f'path({path}) is valid quiz data')

    ok, message, quiz = etl(path)
    if not ok:
        print(f'ETL::path({path}) {message}')
        return 1
    build_path = pathlib.Path('build')
    build_path.mkdir(parents=True, exist_ok=True)
    target_path = build_path / (pathlib.Path(path).stem + '.json')
    with target_path.open('wt', encoding='utf-8') as handle:
        json.dump(quiz, handle, indent=2)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
