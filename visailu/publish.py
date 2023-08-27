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
from typing import Any, Union, no_type_check

import yaml

from visailu import (
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
from visailu.validate import (
    effective_meta,
    parse_defaults,
    parse_scale_range,
    validate_defaults,
    validate_path,
)

AnswerExportType = list[dict[str, Union[str, bool]]]
QuestionExportType = dict[str, Union[int, str, AnswerExportType]]
QuizExportType = list[QuestionExportType]


@no_type_check
def etl(data: Any) -> tuple[int, str, Union[QuizExportType, list]]:
    """Extract, load, and transform the data."""
    try:
        identity = data.get('id')
        title = data.get('title', '')
        questions = data.get('questions', [])
    except (AttributeError, RuntimeError):
        return 1, MODEL_STRUCTURE_UNEXPECTED, []

    if not all(aspect for aspect in (identity, title, questions)):
        return 1, MODEL_VALUES_MISSING, []

    id_export = 1
    quiz_export: QuestionExportType = []
    num_questions = len(questions)
    if num_questions < 10 or 10 < num_questions:
        problem = 'too few' if num_questions < 10 else 'too many'
        log.warning(f'model with {problem} questions {num_questions} instead of 10')
    for entry in questions:
        question = entry.get('question', '')
        answers = entry.get('answers', [])
        meta = effective_meta(data, entry)
        target_type, maps_to, default_rating = parse_defaults(meta)
        if target_type is None:
            return 1, MODEL_META_INVALID_DEFAULTS, []
        ok, message = validate_defaults(target_type, maps_to, default_rating)
        if not ok:
            return 1, message, []
        if target_type is None or not maps_to:
            return 1, MODEL_META_INVALID_RANGE, []
        if target_type is bool:
            if default_rating not in maps_to:
                return 1, MODEL_META_INVALID_RANGE_VALUE, []
        if target_type is float:
            try:
                val = float(default_rating)
                if not isinstance(default_rating, (int, float)) or default_rating is False or default_rating is True:
                    return 1, MODEL_META_INVALID_RANGE_VALUE, []
            except (TypeError, ValueError):
                return 1, MODEL_META_INVALID_RANGE_VALUE, []
            if not maps_to[0] <= val <= maps_to[1]:
                return 1, MODEL_META_INVALID_RANGE_VALUE, []

        if not all(aspect for aspect in (question, answers)):
            return 1, MODEL_QUESTION_INCOMPLETE, []

        question_export = {
            'id': id_export,
            'question': question,
            'options': [],
        }
        num_answers = len(answers)
        if num_answers < 4 or 4 < num_answers:
            problem = 'too few' if num_answers < 4 else 'too many'
            log.warning(f'model with {problem} answers {num_answers} instead of 4 at question {id_export}')
        for option in answers:
            answer = option.get('answer', '')
            rating = option.get('rating')
            if rating is None:
                rating = default_rating
            if target_type is bool:
                if rating not in maps_to:
                    return 1, MODEL_QUESTION_INVALID_RANGE, []
            if target_type is float:
                try:
                    val = float(rating)
                    if not isinstance(rating, (int, float)) or rating is False or rating is True:
                        return 1, MODEL_QUESTION_INVALID_RANGE_VALUE, []
                except (TypeError, ValueError):
                    return 1, MODEL_QUESTION_INVALID_RANGE_VALUE, []
                if not maps_to[0] <= val <= maps_to[1]:
                    return 1, MODEL_QUESTION_INVALID_RANGE_VALUE, []
            if not answer:
                return 1, MODEL_QUESTION_ANSWER_MISSING, []
            if rating is None:
                return 1, MODEL_QUESTION_ANSWER_MISSING_RATING, []
            question_export['options'].append({'answer': answer, 'isCorrect': rating})
        quiz_export.append(question_export)
        id_export += 1
        if id_export > 10:
            break

    if len(quiz_export) < 10:
        log.warning(f'quiz with too few questions {len(quiz_export)} instead of 10')

    return 0, '', quiz_export


@no_type_check
def publish_path(path: str, options=None) -> tuple[int, str, Any]:
    """Drive the model publication."""
    code, message, data = validate_path(path)
    if code != 0:
        return code, message, data

    code, message, quiz = etl(data)
    if code != 0:
        return code, 'Failed on publish', quiz

    build_path = pathlib.Path('build')
    build_path.mkdir(parents=True, exist_ok=True)
    target_path = build_path / (pathlib.Path(path).stem + '.json')
    with target_path.open('wt', encoding='utf-8') as handle:
        json.dump(quiz, handle, indent=2)

    return 0, f'published quiz data at {target_path} (from model at {path})', quiz
