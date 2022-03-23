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

    def test_update_content_in_a_file(self):

        file_path = f"{TMP_DIR_PATH}\\update_content.txt"
        contains_str = "mudar esse conteúdo"
        replace_by_str = "conteúdo novo"

        with open(file_path, "w+") as source:
            source.write(
                f"""The beauty of the sunset [{contains_str}] was
             obscured by the industrial cranes"""
            )

        f = file.File()
        f.update_content(file_path, contains_str, replace_by_str)

        with open(file_path, "r") as target:
            content = target.read()

        assert content.find(replace_by_str) != -1
