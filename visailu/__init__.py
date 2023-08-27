"""Quiz (Finnish: visailu) data operations."""
import datetime as dti
import logging
import os
import pathlib
from typing import List, no_type_check

# [[[fill git_describe()]]]
__version__ = '2023.8.27+parent.gf8ac9e03'
# [[[end]]] (checksum: 55c93108a923ec560e6be75c4304454e)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)

APP_ALIAS = str(pathlib.Path(__file__).parent.name)
APP_ENV = APP_ALIAS.upper()
APP_NAME = locals()['__doc__']
DEBUG = bool(os.getenv(f'{APP_ENV}_DEBUG', ''))
VERBOSE = bool(os.getenv(f'{APP_ENV}_VERBOSE', ''))
QUIET = False
STRICT = bool(os.getenv(f'{APP_ENV}_STRICT', ''))
ENCODING = 'utf-8'
ENCODING_ERRORS_POLICY = 'ignore'
DEFAULT_CONFIG_NAME = f'.{APP_ALIAS}.json'
log = logging.getLogger()  # Module level logger is sufficient
LOG_FOLDER = pathlib.Path('logs')
LOG_FILE = f'{APP_ALIAS}.log'
LOG_PATH = pathlib.Path(LOG_FOLDER, LOG_FILE) if LOG_FOLDER.is_dir() else pathlib.Path(LOG_FILE)
LOG_LEVEL = logging.INFO

TS_FORMAT_LOG = '%Y-%m-%dT%H:%M:%S'
TS_FORMAT_PAYLOADS = '%Y-%m-%d %H:%M:%S.%f UTC'

VERSION = __version__
VERSION_INFO = __version_info__

# simplistic initial output expectations:
OUT_QUESTION_COUNT = 10
OUT_ANSWERS_COUNT = 4

# messages registry:
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


__all__: List[str] = [
    'APP_ALIAS',
    'APP_ENV',
    'APP_NAME',
    'DEBUG',
    'DEFAULT_CONFIG_NAME',
    'DEFAULT_STRUCTURE_NAME',
    'ENCODING',
    'INVALID_YAML_RESOURCE',
    'MODEL_META_INVALID_DEFAULTS',
    'MODEL_META_INVALID_RANGE',
    'MODEL_META_INVALID_RANGE_VALUE',
    'MODEL_QUESTION_ANSWER_MISSING',
    'MODEL_QUESTION_ANSWER_MISSING_RATING',
    'MODEL_QUESTION_INCOMPLETE',
    'MODEL_QUESTION_INVALID_RANGE',
    'MODEL_QUESTION_INVALID_RANGE_VALUE',
    'MODEL_STRUCTURE_UNEXPECTED',
    'MODEL_VALUES_MISSING',
    'OUT_QUESTION_COUNT',
    'OUT_ANSWERS_COUNT',
    'log',
]


def slugify(text: str) -> str:
    """Remove newlines and reduce multiple spaces to single spaces."""
    return ' '.join(text.replace('\n', ' ').split())


@no_type_check
def formatTime_RFC3339(self, record, datefmt=None):  # noqa
    """HACK A DID ACK we could inject .astimezone() to localize ..."""
    return dti.datetime.fromtimestamp(record.created, dti.timezone.utc).isoformat()  # pragma: no cover


@no_type_check
def init_logger(name=None, level=None):
    """Initialize module level logger"""
    global log  # pylint: disable=global-statement

    log_format = {
        'format': '%(asctime)s %(levelname)s [%(name)s]: %(message)s',
        'datefmt': TS_FORMAT_LOG,
        # 'filename': LOG_PATH,
        'level': LOG_LEVEL if level is None else level,
    }
    logging.Formatter.formatTime = formatTime_RFC3339
    logging.basicConfig(**log_format)
    log = logging.getLogger(APP_ENV if name is None else name)
    log.propagate = True


init_logger(name=APP_ENV, level=logging.DEBUG if DEBUG else None)
