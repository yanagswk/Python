from datetime import datetime
import os
import tempfile
import unittest

import main


class TestMain(unittest.TestCase):
    def test_main(self):
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
            today = f'{datetime.now():%Y%m%d}'
            order_file = 'sato_' + today + '.csv'
            with open(os.path.join(order_dir, order_file), 'w', encoding='utf-8') as f:
                f.write("""1,10,埼玉県,080-9999-9999,清原弘貴,2016-12-25
                        1,三十,埼玉県,080-9999-9999,清原弘貴,2016-12-25
                        """)

            main.ITEM_TSV_PATH = item_tsv
            main.ORDER_DIR = order_dir
            main.FAILURE_DIR = failure_dir
            main.DELIVERY_DIR = delivery_dir

            main.main()

            failure_file = 'failure_' + today + '.csv'
            with open(os.path.join(failure_dir, failure_file), encoding='utf-8') as f:
                c = f.read()
                self.assertEqual(c, '1,三十,埼玉県,080-9999-9999,清原弘貴,2016-12-25,' + order_file + '\n',
                                 msg="main関数でテスト用注文受付ファイルを読み込ませたところ、"
                                     "注文受付失敗ファイルの内容が想定と違いました")

            with open(os.path.join(delivery_dir, 'delivery_20161225.csv'), encoding='utf-8') as f:
                c = f.read()
                self.assertEqual(c, '1,10,埼玉県,080-9999-9999,清原弘貴,2016-12-25,' + order_file + '\n',
                                 msg="main関数でテスト用注文受付ファイルを読み込ませたところ、"
                                     "日別注文ファイルの内容が想定と違いました")
