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

from visailu import (
    OUT_QUESTION_COUNT,
    OUT_ANSWERS_COUNT,
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
    validate_defaults,
    validate_path,
)

AnswerExportType = list[dict[str, Union[str, bool]]]
QuestionExportType = dict[str, Union[int, str, AnswerExportType]]
QuizExportType = list[QuestionExportType]


@no_type_check
def etl(data: Any) -> QuizExportType:
    """Extract, load, and transform the data."""
    id_export = 1
    quiz_export: QuestionExportType = []
    questions = data['questions']
    num_questions = len(questions)
    if num_questions < OUT_QUESTION_COUNT or OUT_QUESTION_COUNT < num_questions:
        problem = 'too few' if num_questions < OUT_QUESTION_COUNT else 'too many'
        log.warning(f'model with {problem} questions {num_questions} instead of 10')
    for entry in questions:
        question_export = {
            'id': id_export,
            'question': entry['question'],
            'options': [],
        }
        answers = entry['answers']
        num_answers = len(answers)
        if num_answers < OUT_ANSWERS_COUNT or OUT_ANSWERS_COUNT < num_answers:
            problem = 'too few' if num_answers < OUT_ANSWERS_COUNT else 'too many'
            log.warning(f'model with {problem} answers {num_answers} instead of 4 at question {id_export}')
        for option in answers:
            question_export['options'].append({'answer': option['answer'], 'isCorrect': option['rating']})
        quiz_export.append(question_export)
        id_export += 1
        if id_export > OUT_QUESTION_COUNT:
            break

    if len(quiz_export) < OUT_QUESTION_COUNT:
        log.warning(f'quiz with too few questions {len(quiz_export)} instead of 10')

    return quiz_export


@no_type_check
def publish_path(path: str, options=None) -> tuple[int, str, Any]:
    """Drive the model publication."""
    code, message, data = validate_path(path)
    if code != 0:
        return code, message, data

    quiz = etl(data)
    build_path = pathlib.Path('build')
    build_path.mkdir(parents=True, exist_ok=True)
    target_path = build_path / (pathlib.Path(path).stem + '.json')
    with target_path.open('wt', encoding='utf-8') as handle:
        json.dump(quiz, handle, indent=2)

    return 0, f'published quiz data at {target_path} (from model at {path})', quiz
