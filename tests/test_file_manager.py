import pytest
import shutil
import os
import string
import random
from manager.modules.file_manager import file


class DefaultSettings:
    CURRENT_DIR_PATH = os.path.dirname(__file__)
    TMP_DIR_NAME = "tmp"
    TMP_DIR_PATH = f"{CURRENT_DIR_PATH}\\{TMP_DIR_NAME}"


@pytest.fixture(autouse=True, scope="class")
def initialize_basic_needs():

    default_settings = DefaultSettings()

    if not os.path.exists(default_settings.TMP_DIR_PATH):
        os.mkdir(default_settings.TMP_DIR_PATH)

    if not os.path.isdir(default_settings.TMP_DIR_PATH):
        return False

    # wait test to finish
    yield pytest.param

    shutil.rmtree(default_settings.TMP_DIR_PATH)


@pytest.mark.usefixtures("initialize_basic_needs")
class TestFileManager(object):

    # test with right source and dest
    # test with wrong source
    # test with wrong dest
    # test both wrong

    def test_copy_file_with_right_source_and_dest(self):

        default_settings = DefaultSettings()

        source_file = f"{default_settings.TMP_DIR_PATH}\\source_unittest.txt"
        target_file = f"{default_settings.TMP_DIR_PATH}\\target_unittest.txt"

        with open(source_file, "w+") as source:
            source.write("".join(random.choice(string.ascii_letters) for i in range(10)))

        f = file.File()
        f.copy_single(source_file, target_file)

        with open(source_file, "r") as s_content:
            source_content = s_content.read()

        with open(target_file, "r") as t_content:
            target_content = t_content.read()

        assert source_content == target_content
