from datetime import datetime
import os
import tempfile
import unittest

import main
from practice_one.main import (
    Item, Items,
    Order, load_orders,
    write_deliver_orders, write_failure_orders,
)


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.items = Items([Item('01', '名前', '1000')])

    def test_validate(self):
        order = Order('01', '1', '埼玉県', '03-3333-3333', '清原弘貴', '2014-11-05', './file.csv')
        actual = order.validate(self.items)
        self.assertTrue(actual,
                        msg="Order.validateが成功するはずの入力でFalseが返りました")

    def test_validate_item_id(self):
        order = Order('02', '1', '埼玉県', '03-3333-3333', '清原弘貴', '2014-11-05', './file.csv')
        actual = order.validate(self.items)
        self.assertFalse(actual,
                         msg="Itemsに存在しないitem_idを入力したのにOrder.validateがTrueを返しました")

    def test_validate_amount(self):
        order = Order('01', '四', '埼玉県', '03-3333-3333', '清原弘貴', '2014-11-05', './file.csv')
        actual = order.validate(self.items)
        self.assertFalse(actual,
                         msg="不正なamountを入力したのにOrder.validateがTrueを返しました")

    def test_validate_amount_too_small(self):
        order = Order('01', '0', '埼玉県', '03-3333-3333', '清原弘貴', '2014-11-05', './file.csv')
        actual = order.validate(self.items)
        self.assertFalse(actual,
                         msg="amountが1より小さいのにOrder.validateがTrueを返しました")

    def test_validate_shipping_address(self):
        order = Order('01', '1', '', '03-3333-3333', '清原弘貴', '2014-11-05', './file.csv')
        actual = order.validate(self.items)
        self.assertFalse(actual,
                         msg="shipping_addressが空文字なのにOrder.validateがTrueを返しました")

    def test_validate_tel(self):
        order = Order('01', '1', '埼玉県', '03-3-3', '清原弘貴', '2014-11-05', './file.csv')
        actual = order.validate(self.items)
        self.assertFalse(actual,
                         msg="不正なtel_numberを入力したのにOrder.validateがTrueを返しました")

    def test_validate_fullname(self):
        order = Order('01', '1', '埼玉県', '03-3333-3333', '', '2014-11-05', './file.csv')
        actual = order.validate(self.items)
        self.assertFalse(actual,
                         msg="fullnameが空文字なのにOrder.validateがTrueを返しました")

    def test_validate_shipping_date(self):
        order = Order('01', '1', '埼玉県', '03-3333-3333', '清原弘貴', '20141105', './file.csv')
        actual = order.validate(self.items)
        self.assertFalse(actual,
                         "不正なshipping_date_strを入力したのにOrder.validateがTrueを返しました")

    def test_row_string(self):
        order = Order('01', '1', '埼玉県', '03-3333-3333', '清原弘貴', '2014-11-05', './file.csv')
        actual = order.row_string()
        self.assertEqual(actual, '01,1,埼玉県,03-3333-3333,清原弘貴,2014-11-05,./file.csv')


class TestLoadOrders(unittest.TestCase):
    def setUp(self):
        self.order_dir = main.ORDER_DIR
        self.temp = tempfile.TemporaryDirectory()
        main.ORDER_DIR = self.temp.name

    def tearDown(self):
        self.temp.cleanup()
        main.ORDER_DIR = self.order_dir

    def test_load_orders(self):
        with open(os.path.join(self.temp.name, 'sato_20141105.csv'), 'w', encoding='utf-8') as f:
            f.write("01,1,埼玉県,03-3333-3333,清原弘貴,2014-11-05\n")
        with open(os.path.join(self.temp.name, 'sawai_20141105.csv'), 'w', encoding='utf-8') as f:
            f.write("01,8,東京都,03-8888-8888,佐藤治夫,2014-11-20\n")
        with open(os.path.join(self.temp.name, 'sato_20141104.csv'), 'w', encoding='utf-8') as f:
            f.write("01,10,埼玉県,03-3333-3333,清原弘貴,2014-11-08\n")
        actual = load_orders(datetime(2014, 11, 5))
        self.assertEqual(len(actual), 2,
                         msg="2つのテスト用TSVから計2つの注文を読み込むべき処理で、2つ読み込まれませんでした")
        if actual[0].fullname == '清原弘貴':
            a_ky = actual[0]
            a_haru = actual[1]
        else:
            a_ky = actual[1]
            a_haru = actual[0]
        self.assertEqual(a_ky.item_id, '01',
                         msg='商品IDが想定と違いました')
        self.assertEqual(a_ky.amount, '1',
                         msg='個数が想定と違いました')
        self.assertEqual(a_ky.shipping_address, '埼玉県',
                         msg='宅配先住所が想定と違いました')
        self.assertEqual(a_ky.tel_number, '03-3333-3333',
                         msg='電話番号が想定と違いました')
        self.assertEqual(a_ky.fullname, '清原弘貴',
                         msg='氏名が想定と違いました')
        self.assertEqual(a_ky.shipping_date_str, '2014-11-05',
                         msg='宅配日が想定と違いました')
        self.assertEqual(a_ky.order_file, 'sato_20141105.csv',
                         msg='取込元の注文受付ファイルが想定と違いました')
        self.assertEqual(a_haru.item_id, '01',
                         msg='商品IDが違いました')
        self.assertEqual(a_haru.amount, '8',
                         msg='個数が想定と違いました')
        self.assertEqual(a_haru.shipping_address, '東京都',
                         msg='宅配先住所が想定と違いました')
        self.assertEqual(a_haru.tel_number, '03-8888-8888',
                         msg='電話番号が想定と違いました')
        self.assertEqual(a_haru.fullname, '佐藤治夫',
                         msg='氏名が想定と違いました')
        self.assertEqual(a_haru.shipping_date_str, '2014-11-20',
                         msg='宅配日が想定と違いました')
        self.assertEqual(a_haru.order_file, 'sawai_20141105.csv',
                         msg='取込元の注文受付ファイルが想定と違いました')


class TestWriteDeliver(unittest.TestCase):
    def setUp(self):
        self.delivery_dir = main.DELIVERY_DIR
        self.temp = tempfile.TemporaryDirectory()
        main.DELIVERY_DIR = self.temp.name

        self.items = Items([Item('01', '名前', '1000')])

    def tearDown(self):
        self.temp.cleanup()
        main.DELIVERY_DIR = self.delivery_dir

    def test_write(self):
        order1 = Order('01', '1', '埼玉県', '03-3333-3333',
                       '清原弘貴', '2018-12-25', 'sato_20181130.csv')
        order2 = Order('01', '3', '埼玉県', '03-3333-3333',
                       '清原弘貴', '2018-12-25', 'sato_20181130.csv')
        order3 = Order('01', '1', '埼玉県', '03-3333-3333',
                       '清原弘貴', '2018-12-24', 'sato_20181130.csv')
        order1.validate(self.items)
        order2.validate(self.items)
        order3.validate(self.items)

        orders = [order1, order2, order3]
        write_deliver_orders(orders)
        with open(os.path.join(self.temp.name, 'delivery_20181225.csv'), encoding='utf-8') as f:
            c = f.read()
            self.assertEqual(c, """01,1,埼玉県,03-3333-3333,清原弘貴,2018-12-25,sato_20181130.csv
                                01,3,埼玉県,03-3333-3333,清原弘貴,2018-12-25,sato_20181130.csv
                                """)

        with open(os.path.join(self.temp.name, 'delivery_20181224.csv'), encoding='utf-8') as f:
            c = f.read()
            self.assertEqual(c, """01,1,埼玉県,03-3333-3333,清原弘貴,2018-12-24,sato_20181130.csv
                                """)


class TestWriteFailure(unittest.TestCase):
    def setUp(self):
        self.failure_dir = main.FAILURE_DIR
        self.temp = tempfile.TemporaryDirectory()
        main.FAILURE_DIR = self.temp.name

        self.items = Items([Item('01', '名前', '1000')])

    def tearDown(self):
        self.temp.cleanup()
        main.FAILURE_DIR = self.failure_dir

    def test_write(self):
        order = Order('01', '三', '埼玉県', '03-3333-3333',
                      '清原弘貴', '2018-12-25', 'sato_20181130.csv')
        order.validate(self.items)

        write_failure_orders([order], datetime(2018, 11, 30))
        with open(os.path.join(self.temp.name, 'failure_20181130.csv'), encoding='utf-8') as f:
            c = f.read()
            self.assertEqual(c, "01,三,埼玉県,03-3333-3333,清原弘貴,2018-12-25,sato_20181130.csv\n",
                             msg="テスト用データで write_failure_orders を実行したところ、"
                                 "注文受付失敗ファイルの内容が想定と違いました")
