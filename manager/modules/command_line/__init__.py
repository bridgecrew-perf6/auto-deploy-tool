"""Module to manage the command line"""
from typing import Optional

import typer

from . import cli_file
from . import cli_windows_service

__version__ = "0.1.0"

cli = typer.Typer()
cli.add_typer(cli_windows_service.cli, name="windows-service")
cli.add_typer(cli_file.cli, name="file-manager")


def _version_callback(value: bool) -> None:
    """show the version of the cli application"""

    if value:
        typer.echo(f"Awesome CLI Version:  v{__version__}")
        raise typer.Exit()


@cli.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    """main cli function"""

    return
