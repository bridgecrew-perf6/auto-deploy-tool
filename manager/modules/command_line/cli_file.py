"""cli file manager"""
import logging
import typer

# import click_spinner
from manager.modules.file_manager import file

cli = typer.Typer()
logger = logging.getLogger()


@cli.command("copy-single-file")
def copy_file(source_path: str, dest_path: str) -> None:
    """Copy file from one path to other path"""
    try:
        f = file.File()
        f.copy_single(source_path, dest_path)
    except Exception as err:
        logger.exception(f"error to copy single file. err: {err}")
        typer.secho(f"[X] error to copy file from {source_path} to {dest_path}", fg="red")
