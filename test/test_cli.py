import pathlib

from typer.testing import CliRunner

import visailu
from visailu.cli import app

runner = CliRunner()

TEST_PREFIX = pathlib.Path('test', 'fixtures', 'basic')
INVALID_YAML_PATH = pathlib.Path(TEST_PREFIX, 'abuse', 'invalid-yaml.yml')
MODEL_META_INVALID_RANGE_DEFAULT_PATH = pathlib.Path(TEST_PREFIX, 'abuse', 'model-meta-invalid-range-default.yml')
MINIMAL_MODEL_PATH = pathlib.Path(TEST_PREFIX, 'use', 'minimal.yml')
EXACT_MODEL_PATH = pathlib.Path(TEST_PREFIX, 'use', 'ten.yml')
ONE_MORE_MODEL_PATH = pathlib.Path(TEST_PREFIX, 'use', 'eleven.yml')
VARYING_MODEL_PATH = pathlib.Path(TEST_PREFIX, 'use', 'questions-answers-counts-differing.yml')

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


def test_validate_bad_model():
    result = runner.invoke(app, ['validate', str(MODEL_META_INVALID_RANGE_DEFAULT_PATH)])
    assert result.exit_code == 1


def test_publish():
    result = runner.invoke(app, ['publish', '-f', str(MINIMAL_MODEL_PATH)])
    assert result.exit_code == 0


def test_publish_pos():
    result = runner.invoke(app, ['publish', str(MINIMAL_MODEL_PATH)])
    assert result.exit_code == 0


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


def test_publish_minimal_model():
    result = runner.invoke(app, ['publish', str(MINIMAL_MODEL_PATH)])
    assert result.exit_code == 0


def test_publish_exact_model():
    result = runner.invoke(app, ['publish', str(EXACT_MODEL_PATH)])
    assert result.exit_code == 0


def test_publish_one_more_model():
    result = runner.invoke(app, ['publish', str(ONE_MORE_MODEL_PATH)])
    assert result.exit_code == 0


def test_publish_varying_model():
    result = runner.invoke(app, ['publish', str(VARYING_MODEL_PATH)])
    assert result.exit_code == 0


def test_publish_bad_model():
    result = runner.invoke(app, ['publish', str(MODEL_META_INVALID_RANGE_DEFAULT_PATH)])
    assert result.exit_code == 1


def test_help():
    for options in ([], ['-h'], ['--help']):
        result = runner.invoke(app, options)
        assert result.exit_code == 0
        assert 'Quiz (Finnish: visailu) data operations.' in result.stdout
