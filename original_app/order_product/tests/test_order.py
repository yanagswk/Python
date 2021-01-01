from datetime import datetime, date
import os
import sys
import tempfile
import unittest

sys.path.append(os.path.abspath(
    r"/Users/yanagswk/個人用/Python/original_app/order_product"))

import main
from main import (
    Item, Order, load_item, write_orders, read_order)


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.items = [Item('01', '名前', '1000')]
        self.order_day = date(2020, 12, 25)
    
    def test_validate(self):
        """ 正しい値を入れて、Order.validateがTrueを返すかのテスト
        """
        order = Order('01', '1', '長野県', '03-3333-3333', '山田太郎', '2020-12-26')
        actual = order.validate(self.items, self.order_day)
        self.assertTrue(actual,
                        msg='Order.validateが成功するはずの入力でFalseが返りました')
    
    def test_validate_item_id(self):
        """ 存在しないitem_idを入れて、Order.validateがFalseを返すかのテスト
        """
        order = Order('02', '1', '長野県', '03-3333-3333', '山田太郎', '2020-12-26')
        actual = order.validate(self.items, self.order_day)
        self.assertFalse(actual,
                         msg='Itemに存在しないitem_idを入力したのにOrder.validateがTrueを返しました')

    def test_validate_amount(self):
        """ 不正なorder_amountを入れて、Order.validateがFalseを返すかのテスト
        """
        order = Order('01', '四', '長野県', '03-3333-3333', '山田太郎', '2020-12-26')
        actual = order.validate(self.items, self.order_day)
        self.assertFalse(actual,
                         msg='不正なorder_amountを入力したのにOrder.validateがTrueを返しました')
    
    def test_validate_amount_too_small(self):
        """ order_amountが1より小さい値を入れて、Order.validateがFalseを返すのかのテスト
        """
        order = Order('01', '0', '長野県', '03-3333-3333', '山田太郎', '2020-12-26')
        actual = order.validate(self.items, self.order_day)
        self.assertFalse(actual,
                        msg='order_amountが1より小さいのにOrder.validateがTrueを返しました')
    
    def test_validate_adress(self):
        """ order_adressを空文字をにして、Order.validateがFalseを返すのかのテスト
        """
        order = Order('01', '1', '', '03-3333-3333', '山田太郎', '2020-12-26')
        actual = order.validate(self.items, self.order_day)
        self.assertFalse(actual,
                         msg='order_adressが空文字なのにOrder.validateがTrueを返しました')
    
    def test_validate_tel(self):
        """ 不正なorder_telを入れて、Order.validateがFalseを返すのかのテスト
        """
        order = Order('01', '1', '長野県', '03-3333-33', '山田太郎', '2020-12-26')
        actual = order.validate(self.items, self.order_day)
        self.assertFalse(actual,
                         msg='不正なorder_telを入力したのにOrder.validateがTrueを返しました')
    
    def test_validate_name(self):
        """ order_telを空文字にして、Order.validateがFalseを返すのかのテスト
        """
        order = Order('01', '1', '長野県', '03-3333-3333', '', '2020-12-26')
        actual = order.validate(self.items, self.order_day)
        self.assertFalse(actual,
                         msg='order_nameが空文字なのにOrder.validateがTrueを返しました')
    
    def test_validate_date_str(self):
        """ 不正なorder_date_strを入れて、Order.validateがFalseを返すのかのテスト
        """
        order = Order('01', '1', '長野県', '03-3333-3333', '山田太郎', '2020-12-二十六')
        actual = order.validate(self.items, self.order_day)
        self.assertFalse(actual,
                         msg='不正なorder_date_strだったのにOrder.validateがTrueを返しました')
    
    def test_validate_after_date(self):
        """ 宅配日よりも前の日にして、Order.validateがFalseを返すのかのテスト
        """
        order = Order('01', '1', '長野県', '03-3333-3333', '山田太郎', '2020-10-26')
        actual = order.validate(self.items, self.order_day)
        self.assertFalse(actual,
                         msg='宅配日よりも前の日だったのにOrder.validateがTrueを返しました')


class TestLoadOrder(unittest.TestCase):
    def setUp(self):
        self.order_dir = main.ORDER_DIR
        self.temp = tempfile.TemporaryDirectory()
        main.ORDER_DIR = self.temp.name
        self.order_day = date(2020, 12, 25)
    
    def tearDown(self):
        self.temp.cleanup()
        main.ORDER_DIR = self.order_dir
    
    def test_load_order(self):
        """ 指定された日付のテスト用csvファイルから、注文を読み込むかのテスト
        """
        with open(os.path.join(self.temp.name, 'sato_20201225.csv'), 'w', encoding='utf-8') as f:
            f.write('01,1,埼玉県,03-3333-3333,中村俊介,2020-12-30\n')
        with open(os.path.join(self.temp.name, 'sakurai_20201225.csv'), 'w', encoding='utf-8') as f:
            f.write('01,8,埼玉県,03-8888-9999,桜井俊介,2020-12-29\n')
        with open(os.path.join(self.temp.name, 'satou_20201224.csv'), 'w', encoding='utf-8') as f:
            f.write('01,10,埼玉県,03-3333-3333,佐藤俊介,2021-01-05\n')
        
        actual = read_order(self.order_day)

        self.assertEqual(len(actual), 2,
                         msg='2つのテスト用TSVから計2つの注文を読み込むべき処理で、2つ読み込まれませんでした')


class TestWriteOrders(unittest.TestCase):
    def setUp(self):
        self.delivery_dir = main.DELIVERY
        self.temp = tempfile.TemporaryDirectory()
        self.items = [Item('01', '名前', '1000')]
        self.order_day = date(2020, 12, 25)
        self.failure_dir = main.FAILURE
        main.DELIVERY = self.temp.name
        main.FAILURE = self.temp.name

    def tearDown(self):
        self.temp.cleanup()
        main.DELIVERY = self.delivery_dir
        main.FAILURE = self.failure_dir
    
    def test_delivery_dir_write(self):
        """ 正しいテスト用のorderを読み込んで、deliveryのcsvファイルに書き込まれるかのテスト
        """
        order1 = Order('01', '1', '長野県', '03-3333-3333', '山田花太郎', '2020-12-31')
        order2 = Order('01', '1', '沖縄県', '03-7777-7777', '山田洋太郎', '2020-12-29')
        order1.validate(self.items, self.order_day)
        order2.validate(self.items, self.order_day)

        orders = [order1, order2]
        write_orders(orders)

        with open(os.path.join(self.temp.name, 'delivery_20201231.csv'), encoding='utf-8') as f:
            c = f.read()
            self.assertEqual(c, """01,1,長野県,03-3333-3333,山田花太郎,2020-12-31\n""")
        with open(os.path.join(self.temp.name, 'delivery_20201229.csv'), encoding='utf-8') as f:
            c = f.read()
            self.assertEqual(c, """01,1,沖縄県,03-7777-7777,山田洋太郎,2020-12-29\n""")

    def test_failure_dir_write(self):
        """ 不正なテスト用のorderを読み込んで、failureのcsvファイルに書き込まれるかのテスト
        """
        order = Order('01', '三', '長野県', '03-3333-3333', '山田花太郎', '2020-12-25')
        order.validate(self.items, self.order_day)

        write_orders([order], self.order_day, failure=True)
        with open (os.path.join(self.temp.name, 'failure_20201225.csv'), encoding='utf-8') as f:
            c = f.read()
            self.assertEqual(c, """01,三,長野県,03-3333-3333,山田花太郎,2020-12-25\n""")


if __name__ == '__main__':
    unittest.main()
