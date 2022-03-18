"""Manage file"""
import logging
import shutil
from operator import contains
from .util import is_file


class File:
    """Class to manage file"""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def copy_single(self, source_file: str, dest_file: str) -> str:
        """Copy a single file from source to targe path"""

        if not is_file(source_file):
            raise Exception(f"{source_file} is not a file")

        try:
            dest = shutil.copyfile(source_file, dest_file)
            self.logger.debug(f"file was copied from {source_file} to {dest_file}")

            return dest
        except Exception as err:
            self.logger.exception(f"unable to copy file from {source_file} to {dest_file}")
            raise err

    def update_content(self, file_path: str, contains_in_line: str, replace_by: str) -> None:
        """Update the content of a file"""

        contains_in_line = contains_in_line.lower()

        try:
            text_line = None

            with open(file_path, "r+", encoding="latin-1") as file:
                lines = file.readlines()

                for line in lines:
                    if contains(line.lower(), contains_in_line):
                        text_line = line
                        break

                if text_line is None:
                    return

                file.seek(0)
                content = file.read()
                content = content.replace(text_line.strip(), replace_by)
                file.truncate(0)
                file.seek(0)
                file.write(content)
        except Exception as err:
            self.logger.exception("unable to update the content")
            raise err
