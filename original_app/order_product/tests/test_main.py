from datetime import datetime, date
import os
import sys
import tempfile
import unittest

import main


class TestMain(unittest.TestCase):

    def test_main(self):
        """ テスト用のtsvファイルとcsvファイルを読み込んで、正しく日別注文ファイルと注文受付ファイルに書き込むかのテスト
        """
        with tempfile.TemporaryDirectory() as d:
            order_dir = os.path.join(d, 'order')
            failure_dir = os.path.join(d, 'failure')
            delivery_dir = os.path.join(d, 'delivery')

            os.mkdir(order_dir)
            os.mkdir(failure_dir)
            os.mkdir(delivery_dir)

            item_tsv = os.path.join(d, 'items.tsv')

            # 商品TSVを書く
            with open(item_tsv, 'w', encoding='utf-8') as f:
                f.write("1\t名前1\t1000\n")

            # OrderCSVを書く
            order_day = date(2020, 12, 25)
            order_day_str = f'{order_day:%Y%m%d}'
            order_file = f'sato_{order_day_str}.csv'
            with open(os.path.join(order_dir, order_file), 'w', encoding='utf-8') as f:
                f.write("""1,10,埼玉県,080-9999-9999,田中一郎,2021-01-11\n1,三十,埼玉県,080-9999-9999,田中一郎,2019-12-25""")

            main.ITEMS_TABLE = item_tsv
            main.ORDER_DIR = order_dir
            main.FAILURE = failure_dir
            main.DELIVERY = delivery_dir

            main.main(order_day)

            failure_file = f'failure_{order_day_str}.csv'
            with open(os.path.join(failure_dir, failure_file), encoding='utf-8') as f:
                c = f.read()
                self.assertEqual(c, '1,三十,埼玉県,080-9999-9999,田中一郎,2019-12-25\n',
                                 msg="main関数でテスト用注文受付ファイルを読み込ませたところ、"
                                     "注文受付失敗ファイルの内容が想定と違いました")

            with open(os.path.join(delivery_dir, 'delivery_20210111.csv'), encoding='utf-8') as f:
                c = f.read()
                self.assertEqual(c, '1,10,埼玉県,080-9999-9999,田中一郎,2021-01-11\n',
                                 msg="main関数でテスト用注文受付ファイルを読み込ませたところ、"
                                     "日別注文ファイルの内容が想定と違いました")


if __name__ == '__main__':
    unittest.main()
