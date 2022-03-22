import filecmp
import os
import shutil
from pathlib import Path

import pytest

from manager.modules.file_manager import folder
from tests import TMP_DIR_PATH
from tests.conftest import create_random_tree

SOURCE_FOLDER_NAME = "folder_source"
TARGET_FOLDER_NAME = "folder_target"


@pytest.fixture(autouse=True, scope="class")
def create_random_source_folder():

    source_folder_path = f"{TMP_DIR_PATH}\\{SOURCE_FOLDER_NAME}"
    target_folder_path = f"{TMP_DIR_PATH}\\{TARGET_FOLDER_NAME}"

    if not os.path.exists(source_folder_path):
        os.mkdir(source_folder_path)

    if not os.path.isdir(source_folder_path):
        raise IsADirectoryError(f"{source_folder_path} is not a directory")

    create_random_tree(source_folder_path)

    if not os.path.exists(target_folder_path):
        os.mkdir(target_folder_path)

    if not os.path.isdir(target_folder_path):
        raise IsADirectoryError(f"{target_folder_path} is not a directory")


class TestFolderManager(object):
    @pytest.fixture(autouse=True)
    def __setup(self) -> None:
        """Replace init function for test classes"""

        self.source_folder_path = f"{TMP_DIR_PATH}\\{SOURCE_FOLDER_NAME}"
        self.target_folder_path = f"{TMP_DIR_PATH}\\{TARGET_FOLDER_NAME}"

    def test_copy_folder_with_right_source_and_dest(self) -> None:
        """Test if it's possible to copy a entire folder content to an target place"""

        f = folder.Folder()
        f.copy(self.source_folder_path, self.target_folder_path)

        dir_cmp = filecmp.dircmp(self.source_folder_path, self.target_folder_path)
        left = dir_cmp.left_list
        right = dir_cmp.right_list

        shutil.rmtree(self.target_folder_path)

        assert left == right, "target directory contains different items compared to source directory"

    def test_copy_folder_ignoring_patterns(self) -> None:
        """Test if it's possible to copy a entire folder content to an target place.
        However it should not copy items base on a specific patter.

        In thos case we don't want to copy files *.xml and *.pdf

        we create the files with these extensions and the functions must not copy them
        """

        _ignore_xml = "_ignore.xml"
        p_xml = Path(self.source_folder_path) / _ignore_xml
        p_xml.touch(exist_ok=True)

        _ignore_pdf = "_ignore.pdf"
        p_pdf = Path(self.source_folder_path) / _ignore_pdf
        p_pdf.touch(exist_ok=True)

        _ignore_pattern = ["*.xml", "*.pdf"]

        f = folder.Folder()
        f.copy(self.source_folder_path, self.target_folder_path, _ignore_pattern)

        dir_cmp = filecmp.dircmp(self.source_folder_path, self.target_folder_path)
        left = dir_cmp.left_list
        right = dir_cmp.right_list

        left.remove(_ignore_xml)
        left.remove(_ignore_pdf)

        assert (
            left == right
        ), "target directory contains items that should not be there due to the ignore pattern applied"
