import pytest

from manager.modules.file_manager import file
from tests import TMP_DIR_PATH
from tests.conftest import random_string

SOURCE_FILE_NAME = "source_unittest.txt"
TARGET_FILE_NAME = "target_unittest.txt"


class TestFileManager(object):
    @pytest.fixture(autouse=True)
    def __setup(self) -> None:
        """Replace init function for test classes"""

        self.source_file_path = f"{TMP_DIR_PATH}\\{SOURCE_FILE_NAME}"
        self.target_file_path = f"{TMP_DIR_PATH}\\{TARGET_FILE_NAME}"

    def test_copy_file_with_right_source_and_dest(self):

        with open(self.source_file_path, "w+") as source:
            source.write(random_string())

        f = file.File()
        f.copy_single(self.source_file_path, self.target_file_path)

        with open(self.source_file_path, "r") as s_content:
            source_content = s_content.read()

        with open(self.target_file_path, "r") as t_content:
            target_content = t_content.read()

        assert source_content == target_content

    # def test_update_content_in_a_file(self):
