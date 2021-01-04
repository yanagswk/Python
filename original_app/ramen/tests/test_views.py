import termcolor
import os
import string
import unittest
import sys
import tempfile


sys.path.append(os.path.abspath(
    r"/Users/yanagswk/個人用/Python/original_app/ramen"))
import settings
from views import find_file


class TestGetTemplate(unittest.TestCase):
    """ templateを読み込むテストをするテストクラス
    """
    def setUp(self):
        self.dir = find_file.template_dir_path
        self.temp = tempfile.TemporaryDirectory()
        find_file.template_dir_path = self.temp.name
        self.text_file = 'test.txt'
        self.test_path = os.path.join(find_file.template_dir_path,
                                      self.text_file)
        with open(self.test_path, 'w') as f:
            f.write("""テスト用のファイルです""")

    def tearDown(self):
        self.temp.cleanup()
        template_dir_path = self.dir

    def test_get_template_dir_path(self):
        """ settingsからディレクトリのpathを返すかのテスト
        """
        dir_path = find_file.get_template_dir_path()
        self.assertTrue(dir_path,
                        msg="正確なディレクトリのpathを指定したのにテストに失敗しました。")

    def test_find_template(self):
        """ ファイルが存在するか確認するテスト
        """
        file_path = find_file.find_template(self.text_file)
        self.assertTrue(os.path.exists(file_path),
                        msg="ファイルの存在が確認できませんでした。")

    def test_get_template(self):
        """ templateを読み込むかのテスト
        """
        get_temp = find_file.get_template(self.text_file)
        self.assertIn("テスト用のファイルです", get_temp.template,
                      msg="テスト用のtemplate通り読み込めませんでした。")


if __name__ == "__main__":
    unittest.main()
