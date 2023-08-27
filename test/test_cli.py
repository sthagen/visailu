import json
import pathlib

import pytest
from typer.testing import CliRunner

import visailu
from visailu.cli import app

runner = CliRunner()

TEST_PREFIX = pathlib.Path('test', 'fixtures', 'basic')

EMPTY_MODEL_PATH = pathlib.Path(TEST_PREFIX, 'abuse', 'empty.yml')
INVALID_YAML_PATH = pathlib.Path(TEST_PREFIX, 'abuse', 'invalid-yaml.yml')
MODEL_META_INVALID_DOMAIN_PATH = pathlib.Path(TEST_PREFIX, 'abuse', 'model-meta-invalid-domain.yml')
MODEL_META_INVALID_RANGE_DEFAULT_PATH = pathlib.Path(TEST_PREFIX, 'abuse', 'model-meta-invalid-range-default.yml')
MODEL_META_INVALID_RANGE_PATH = pathlib.Path(TEST_PREFIX, 'abuse', 'model-meta-invalid-range.yml')
MODEL_META_MISSING_DEFAULTS = pathlib.Path(TEST_PREFIX, 'abuse', 'model-meta-missing-defaults.yml')
MODEL_META_MISSING_RANGE_PATH = pathlib.Path(TEST_PREFIX, 'abuse', 'model-meta-missing-range.yml')
MODEL_MISSING_ANSWERS_PATH = pathlib.Path(TEST_PREFIX, 'abuse', 'model-missing-answers.yml')
MODEL_MISSING_ID_PATH = pathlib.Path(TEST_PREFIX, 'abuse', 'model-missing-id.yml')
MODEL_MISSING_META_PATH = pathlib.Path(TEST_PREFIX, 'abuse', 'model-missing-meta.yml')
MODEL_MISSING_QUESTIONS_PATH = pathlib.Path(TEST_PREFIX, 'abuse', 'model-missing-questions.yml')
MODEL_MISSING_TITLE_PATH = pathlib.Path(TEST_PREFIX, 'abuse', 'model-missing-title.yml')
MODEL_QUESTION_INVALID_RANGE_PATH = pathlib.Path(TEST_PREFIX, 'abuse', 'model-question-invalid-range.yml')

EXACT_MODEL_PATH = pathlib.Path(TEST_PREFIX, 'use', 'ten.yml')
MINIMAL_MODEL_PATH = pathlib.Path(TEST_PREFIX, 'use', 'minimal.yml')
ONE_MORE_MODEL_PATH = pathlib.Path(TEST_PREFIX, 'use', 'eleven.yml')
ROCOCO_MODEL_PATH = pathlib.Path(TEST_PREFIX, 'use', 'rococo.yml')
VARYING_MODEL_PATH = pathlib.Path(TEST_PREFIX, 'use', 'questions-answers-counts-differing.yml')

EXACT_QUIZ_PATH = pathlib.Path(TEST_PREFIX, 'use', 'ten.json')
MINIMAL_QUIZ_PATH = pathlib.Path(TEST_PREFIX, 'use', 'minimal.json')
ONE_MORE_QUIZ_PATH = pathlib.Path(TEST_PREFIX, 'use', 'eleven.json')
ROCOCO_QUIZ_PATH = pathlib.Path(TEST_PREFIX, 'use', 'rococo.json')
VARYING_QUIZ_PATH = pathlib.Path(TEST_PREFIX, 'use', 'questions-answers-counts-differing.json')


def test_version_ok():
    result = runner.invoke(app, ['version'])
    assert result.exit_code == 0
    assert f'version {visailu.__version__}' in result.stdout


def test_verify():
    result = runner.invoke(app, ['verify', '-f', str(MINIMAL_MODEL_PATH)])
    assert result.exit_code == 0


def test_verify_pos():
    result = runner.invoke(app, ['verify', str(MINIMAL_MODEL_PATH)])
    assert result.exit_code == 0


def test_verify_bad_file():
    bad_location = 'file-does-not-exist'
    result = runner.invoke(app, ['verify', bad_location])
    assert result.exit_code == 2


def test_verify_no_file():
    result = runner.invoke(app, ['verify'])
    assert result.exit_code == 2


def test_verify_bad_yaml():
    result = runner.invoke(app, ['verify', str(INVALID_YAML_PATH)])
    assert result.exit_code == 1


def test_validate():
    result = runner.invoke(app, ['validate', '-f', str(MINIMAL_MODEL_PATH)])
    assert result.exit_code == 0


def test_validate_pos():
    result = runner.invoke(app, ['validate', str(MINIMAL_MODEL_PATH)])
    assert result.exit_code == 0


def test_validate_empty_file():
    result = runner.invoke(app, ['validate', str(EMPTY_MODEL_PATH)])
    assert result.exit_code == 1


def test_validate_bad_file():
    bad_location = 'file-does-not-exist'
    result = runner.invoke(app, ['validate', bad_location])
    assert result.exit_code == 2


def test_validate_no_file():
    result = runner.invoke(app, ['validate'])
    assert result.exit_code == 2


def test_validate_bad_yaml():
    result = runner.invoke(app, ['validate', str(INVALID_YAML_PATH)])
    assert result.exit_code == 1


def test_validate_minimal_model():
    result = runner.invoke(app, ['validate', str(MINIMAL_MODEL_PATH)])
    assert result.exit_code == 0


def test_validate_exact_model():
    result = runner.invoke(app, ['validate', str(EXACT_MODEL_PATH)])
    assert result.exit_code == 0


def test_validate_one_more_model():
    result = runner.invoke(app, ['validate', str(ONE_MORE_MODEL_PATH)])
    assert result.exit_code == 0


def test_validate_varying_model():
    result = runner.invoke(app, ['validate', str(VARYING_MODEL_PATH)])
    assert result.exit_code == 0


def test_validate_rococo_model():
    result = runner.invoke(app, ['validate', str(ROCOCO_MODEL_PATH)])
    assert result.exit_code == 0


def test_validate_bad_model_meta_invalid_domain():
    result = runner.invoke(app, ['validate', str(MODEL_META_INVALID_DOMAIN_PATH)])
    assert result.exit_code == 1


def test_validate_bad_model_meta_invalid_range_default():
    result = runner.invoke(app, ['validate', str(MODEL_META_INVALID_RANGE_DEFAULT_PATH)])
    assert result.exit_code == 1


def test_validate_bad_model_meta_invalid_range():
    result = runner.invoke(app, ['validate', str(MODEL_META_INVALID_RANGE_PATH)])
    assert result.exit_code == 1


def test_validate_bad_model_meta_missing_defaults():
    result = runner.invoke(app, ['validate', str(MODEL_META_MISSING_DEFAULTS)])
    assert result.exit_code == 1


def test_validate_bad_model_meta_missing_range():
    result = runner.invoke(app, ['validate', str(MODEL_META_MISSING_RANGE_PATH)])
    assert result.exit_code == 1


def test_validate_bad_model_missing_answers():
    result = runner.invoke(app, ['validate', str(MODEL_MISSING_ANSWERS_PATH)])
    assert result.exit_code == 1


def test_validate_bad_model_missing_id():
    result = runner.invoke(app, ['validate', str(MODEL_MISSING_ID_PATH)])
    assert result.exit_code == 1


def test_validate_bad_model_missing_meta():
    result = runner.invoke(app, ['validate', str(MODEL_MISSING_META_PATH)])
    assert result.exit_code == 1


def test_validate_bad_model_missing_questions():
    result = runner.invoke(app, ['validate', str(MODEL_MISSING_QUESTIONS_PATH)])
    assert result.exit_code == 1


def test_validate_bad_model_missing_title():
    result = runner.invoke(app, ['validate', str(MODEL_MISSING_TITLE_PATH)])
    assert result.exit_code == 1


def test_validate_bad_model_question_invalid_range():
    result = runner.invoke(app, ['validate', str(MODEL_QUESTION_INVALID_RANGE_PATH)])
    assert result.exit_code == 1


def test_publish():
    result = runner.invoke(app, ['publish', '-f', str(MINIMAL_MODEL_PATH)])
    assert result.exit_code == 0


def test_publish_pos():
    result = runner.invoke(app, ['publish', str(MINIMAL_MODEL_PATH)])
    assert result.exit_code == 0


def test_publish_empty_file():
    result = runner.invoke(app, ['publish', str(EMPTY_MODEL_PATH)])
    assert result.exit_code == 1


def test_publish_bad_file():
    bad_location = 'file-does-not-exist'
    result = runner.invoke(app, ['publish', bad_location])
    assert result.exit_code == 2


def test_publish_no_file():
    result = runner.invoke(app, ['publish'])
    assert result.exit_code == 2


def test_publish_bad_yaml():
    result = runner.invoke(app, ['publish', str(INVALID_YAML_PATH)])
    assert result.exit_code == 1


def test_publish_minimal_model(caplog):
    result = runner.invoke(app, ['publish', str(MINIMAL_MODEL_PATH)])
    assert result.exit_code == 0
    generated = json.load((pathlib.Path('build') / MINIMAL_QUIZ_PATH.name).open('rt', encoding='utf-8'))
    expected = json.load(MINIMAL_QUIZ_PATH.open('rt', encoding='utf-8'))
    assert generated == expected
    for record in caplog.records:
        assert record.levelname in ('INFO', 'WARNING')
    assert 'model with too few questions 1 instead of 10' in caplog.text
    assert 'quiz with too few questions 1 instead of 10' in caplog.text


def test_publish_exact_model(caplog):
    result = runner.invoke(app, ['publish', str(EXACT_MODEL_PATH)])
    assert result.exit_code == 0
    generated = json.load((pathlib.Path('build') / EXACT_QUIZ_PATH.name).open('rt', encoding='utf-8'))
    expected = json.load(EXACT_QUIZ_PATH.open('rt', encoding='utf-8'))
    assert generated == expected
    for record in caplog.records:
        assert record.levelname == 'INFO'


def test_publish_one_more_model(caplog):
    result = runner.invoke(app, ['publish', str(ONE_MORE_MODEL_PATH)])
    assert result.exit_code == 0
    generated = json.load((pathlib.Path('build') / ONE_MORE_QUIZ_PATH.name).open('rt', encoding='utf-8'))
    expected = json.load(ONE_MORE_QUIZ_PATH.open('rt', encoding='utf-8'))
    assert generated == expected
    for record in caplog.records:
        assert record.levelname in ('INFO', 'WARNING')
    assert 'model with too many questions 11 instead of 10' in caplog.text


def test_publish_rococo_model():
    result = runner.invoke(app, ['publish', str(ROCOCO_MODEL_PATH)])
    assert result.exit_code == 0


def test_publish_varying_model():
    result = runner.invoke(app, ['publish', str(VARYING_MODEL_PATH)])
    assert result.exit_code == 0


def test_publish_bad_model_meta_invalid_range_default():
    result = runner.invoke(app, ['publish', str(MODEL_META_INVALID_RANGE_DEFAULT_PATH)])
    assert result.exit_code == 1


def test_publish_bad_model_meat_invalid_range():
    result = runner.invoke(app, ['publish', str(MODEL_META_INVALID_RANGE_PATH)])
    assert result.exit_code == 1


def test_publish_bad_model_missing_answers():
    result = runner.invoke(app, ['publish', str(MODEL_MISSING_ANSWERS_PATH)])
    assert result.exit_code == 1


def test_publish_bad_model_missing_id():
    result = runner.invoke(app, ['publish', str(MODEL_MISSING_ID_PATH)])
    assert result.exit_code == 1


def test_publish_bad_model_missing_questions():
    result = runner.invoke(app, ['publish', str(MODEL_MISSING_QUESTIONS_PATH)])
    assert result.exit_code == 1


def test_publish_bad_model_missing_title():
    result = runner.invoke(app, ['publish', str(MODEL_MISSING_TITLE_PATH)])
    assert result.exit_code == 1


def test_publish_bad_model_question_invalid_range():
    result = runner.invoke(app, ['publish', str(MODEL_QUESTION_INVALID_RANGE_PATH)])
    assert result.exit_code == 1


def test_help():
    for options in ([], ['-h'], ['--help']):
        result = runner.invoke(app, options)
        assert result.exit_code == 0
        assert 'Quiz (Finnish: visailu) data operations.' in result.stdout
