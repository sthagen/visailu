"""Command line interface for quiz (Finnish: visailu) data operations."""
import logging
import pathlib
import sys

import typer

from visailu import APP_NAME, QUIET, __version__ as APP_VERSION, log
from visailu.publish import publish as publish_path
from visailu.validate import validate as validate_path
from visailu.verify import verify as verify_path

app = typer.Typer(
    add_completion=False,
    context_settings={'help_option_names': ['-h', '--help']},
    no_args_is_help=True,
)

DocumentPath = typer.Option(
    '',
    '-f',
    '--file',
    help='File path to read model from',
)
Verbosity = typer.Option(
    False,
    '-v',
    '--verbose',
    help='Verbose output (default is False)',
)
Strictness = typer.Option(
    False,
    '-s',
    '--strict',
    help='Ouput noisy warnings on console (default is False)',
)
OutputPath = typer.Option(
    '',
    '-o',
    '--output-path',
    help='Path to output unambiguous content to - like when ejecting a template',
)


@app.callback(invoke_without_command=True)
def callback(
    version: bool = typer.Option(
        False,
        '-V',
        '--version',
        help='Display the application version and exit',
        is_eager=True,
    )
) -> None:
    """
    Quiz (Finnish: visailu) data operations.
    """
    if version:
        typer.echo(f'{APP_NAME} version {APP_VERSION}')
        raise typer.Exit()


def _verify_call_vector(
    doc_path: str, doc_path_pos: str, verbose: bool, strict: bool
) -> tuple[int, str, str, dict[str, bool]]:
    """DRY"""
    doc = doc_path.strip()
    if not doc and doc_path_pos:
        doc = doc_path_pos
    if not doc:
        return 2, 'Document path required', '', {}

    doc_path_path = pathlib.Path(doc)
    if doc_path_path.exists():
        if not doc_path_path.is_file():
            return 2, f'requested model file path at ({doc}) is not a file', '', {}
    else:
        return 2, f'requested model file path at ({doc}) does not exist', '', {}

    options = {
        'quiet': QUIET and not verbose and not strict,
        'strict': strict,
        'verbose': verbose,
    }
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    return 0, '', doc, options


@app.command('verify')
def verify(  # noqa
    doc_path_pos: str = typer.Argument(''),
    doc_path: str = DocumentPath,
    verbose: bool = Verbosity,
    strict: bool = Strictness,
) -> int:
    """
    Verify the model data against YAML syntax.
    """
    code, message, path, options = _verify_call_vector(doc_path, doc_path_pos, verbose, strict)
    log.error(f'{code=}, {message=}')
    if code:
        log.error(message)
        raise typer.Exit(code=code)

    if verify_path(path, options=options):
        raise typer.Exit(code=0)
    raise typer.Exit(code=1)


@app.command('validate')
def validate(  # noqa
    doc_path_pos: str = typer.Argument(''),
    doc_path: str = DocumentPath,
    verbose: bool = Verbosity,
    strict: bool = Strictness,
) -> int:
    """
    Validate the YAML data against the model.
    """
    code, message, path, options = _verify_call_vector(doc_path, doc_path_pos, verbose, strict)
    if code:
        log.error(message)
        raise typer.Exit(code=code)

    ok, _ = validate_path(path, options=options)

    if ok:
        raise typer.Exit(code=0)
    raise typer.Exit(code=1)


@app.command('publish')
def publish(  # noqa
    doc_path_pos: str = typer.Argument(''),
    doc_path: str = DocumentPath,
    verbose: bool = Verbosity,
    strict: bool = Strictness,
) -> int:
    """
    Publish the model data in simplified JSON syntax.
    """
    code, message, path, options = _verify_call_vector(doc_path, doc_path_pos, verbose, strict)
    if code:
        log.error(message)
        raise typer.Exit(code=code)

    ok, _ = publish_path(path, options=options)

    if ok:
        raise typer.Exit(code=0)
    raise typer.Exit(code=1)


@app.command('version')
def app_version() -> None:
    """
    Display the application version and exit.
    """
    callback(True)
