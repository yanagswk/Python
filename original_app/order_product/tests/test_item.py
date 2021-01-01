import tempfile
import unittest
import sys
import os

sys.path.append(os.path.abspath(
    r"/Users/yanagswk/個人用/Python/original_app/order_product"))

import main
from main import Item, load_item


class TestLoadItem(unittest.TestCase):
    def setUp(self):
        self.items_table = main.ITEMS_TABLE
        self.temp = tempfile.NamedTemporaryFile('w')
        main.ITEMS_TABLE = self.temp.name
    
    def tearDown(self):
        self.temp.close()
        main.ITEMS_TABLE = self.items_table
    
    def test(self):
        """ load_item 関数がテスト用のtsvファイルを読み込んで、正しくリストで返すかのテスト
        """
        self.temp.write("""01\t名前1\t100\n02\t名前2\t200\n03\t名前3\t300""")
        self.temp.flush()
        actual = load_item()
        self.assertEqual(len(actual), 3, 
                         msg='テスト用tsvには3つの商品があるのにload_itemは3つ返しませんでした')


if __name__ == '__main__':
    unittest.main()
