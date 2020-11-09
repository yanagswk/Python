import tempfile
import unittest

import main
from practice_one.main import Item, Items, load_items


class TestItems(unittest.TestCase):
    def test_has_item_existed(self):
        """ Items.has_id の引数に指定された item_id の Item が存在する場合のテスト
        """
        target = Items([
            Item('01', '名前1', '100'),
            Item('08', '名前2', '200')
        ])
        self.assertTrue(target.has_id('08'),
                        msg="存在するitem_idを指定したのにItems.has_idがTrueを返しませんでした")

    def test_has_item_not_existed(self):
        """ Items.has_id の引数に指定された item_id の Item が存在しない場合のテスト
        """
        target = Items([
            Item('01', '名前1', '100'),
        ])
        self.assertFalse(target.has_id('08'),
                         msg="存在しないitem_idを指定したのにItems.has_idがTrueを返しました")


class TestLoadItems(unittest.TestCase):
    def setUp(self):
        self.item_tsv_path = main.ITEM_TSV_PATH
        self.temp = tempfile.NamedTemporaryFile('w')
        main.ITEM_TSV_PATH = self.temp.name

    def tearDown(self):
        self.temp.close()
        main.ITEM_TSV_PATH = self.item_tsv_path

    def test(self):
        """ load_items 関数がテスト用のTSVファイルを読み込んで正しく Items を返しているかテスト
        """
        self.temp.write("""01\t名前1\t100
02\t名前2\t200
03\t名前3\t300
""")
        self.temp.flush()
        actual = load_items()
        self.assertEqual(len(actual.items), 3,
                         msg="テスト用TSVには3つの商品があるのにload_itemsは3つ返しませんでした")
        self.assertEqual(actual.items[0].item_id, '01')
        self.assertEqual(actual.items[0].name, '名前1')
        self.assertEqual(actual.items[0].price, '100')
        self.assertEqual(actual.items[1].item_id, '02')
        self.assertEqual(actual.items[1].name, '名前2')
        self.assertEqual(actual.items[1].price, '200')
        self.assertEqual(actual.items[2].item_id, '03')
        self.assertEqual(actual.items[2].name, '名前3')
        self.assertEqual(actual.items[2].price, '300')
