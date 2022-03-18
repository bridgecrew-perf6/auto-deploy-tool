"""Util functions"""
import os


def is_file(file: str) -> bool:
    """Check if is a file or not"""

    return os.path.isfile(file)


def is_folder(folder: str) -> bool:
    """Check if is a folder or not"""

    return os.path.isdir(folder)
