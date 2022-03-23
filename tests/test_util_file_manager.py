from manager.modules.file_manager import util
from tests import TMP_DIR_PATH


class TestUtilFileManager(object):
    def test_is_file(self):
        assert util.is_file(__file__)

    def test_is_folder(self):
        assert util.is_folder(TMP_DIR_PATH)
