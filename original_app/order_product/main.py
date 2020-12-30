import os
import re
import datetime as dt

ITEMS_TABLE = "items.tsv"
ORDER_DIR = "order"
DELIVERY = "delivery"
FAILURE = "failure"


class Item:
    def __init__(self, item_id, item_name, item_price):
        self.item_id = item_id
        self.item_name = item_name
        self.item_price = item_price


class Order:

    AMOUNT_RE = re.compile(r'^[0-9]+$')
    TEL_RE = re.compile(r'^[0-9]{2,4}-[0-9]{4}-[0-9]{4}$')

    def __init__(self, order_item_id, order_amount, order_adress, order_tel,
                 order_name, order_date):
        self.order_item_id = order_item_id
        self.order_amount = order_amount
        self.order_adress = order_adress
        self.order_tel = order_tel
        self.order_name = order_name
        self.order_date_str = order_date
        self.order_date = None

    def validate(self, items):
        """ 注文リストが正しい表記か、バリテーションチェックをする
        """
        flag = False
        # 注文リストの商品ID(order_item_id)が、商品一覧に存在するか確認
        for item in items:
            if self.order_item_id == item.item_id:
                flag = True
                break
        if not flag:
            return False

        # 商品の個数(order_amount)が正しい表記か、正規表現で確認
        if not self.AMOUNT_RE.search(self.order_amount):
            return False
        # 0よりも大きいかを確認
        if int(self.order_amount) < 0:
            return False

        # 住所(order_adress)が指定されているか
        if not self.order_adress:
            return False

        # 電話番号(order_tel)が正しい表記か、正規表現で確認
        if not self.TEL_RE.search(self.order_tel):
            return False

        # 名前(order_name)が指定されてるか
        if not self.order_name:
            return False

        # 宅配日(order_date_str)が日付として扱えるか確認
        try:
            self.order_date = dt.datetime.strptime(self.order_date_str,
                                                   '%Y-%m-%d')
        except ValueError:
            return False

        # すべてのチェックが通ったらTrueを返す
        return True

    def row_string(self):
        """ カンマ区切りにして返す。
        """
        return ','.join((
            self.order_item_id,
            self.order_amount,
            self.order_adress,
            self.order_tel,
            self.order_name,
            self.order_date_str
        ))


def load_item():
    """ 商品を読み込む
    """
    if not os.path.exists(ITEMS_TABLE):
        raise FileNotFoundError(f"{ITEMS_TABLE}が見つかりません。")

    item_list = []
    with open(ITEMS_TABLE, 'r', encoding="utf-8") as lead_file:
        for row in lead_file:
            item_id, item_name, item_price = row.split()
            items = Item(
                item_id.strip(), item_name.strip(), item_price.strip())
            item_list.append(items)
    return item_list


def read_order(order_day):
    """ 当日の注文受付
    """
    # day_str = f"{order_day: "%Y%m%d"}"
    day_str = order_day.strftime("%Y%m%d")
    for filename in os.listdir(ORDER_DIR):
        if day_str not in filename:
            continue

        order_path = os.path.join(ORDER_DIR, filename)

        order_list = []
        with open(order_path, 'r', encoding="UTF-8") as read_order:
            for row in read_order:
                order_item_id, order_amount, order_adress, order_tel,\
                    order_name, order_date = row.split(",")
                order = Order(order_item_id.strip(),
                              order_amount.strip(),
                              order_adress.strip(),
                              order_tel.strip(),
                              order_name.strip(),
                              order_date.strip()
                              )
                order_list.append(order)
        return order_list


def write_orders(validated_orders, order_day=None, failure=False):
    """ 日別注文ファイル書き込み or 注文受付失敗書き込み
    """
    for day_order in validated_orders:
        if not failure:
            filename = f"delivery_{day_order.order_date.strftime('%Y%m%d')}.csv"
            filepath = os.path.join(DELIVERY, filename)
        else:
            filename = f"failure_{order_day.strftime('%Y%m%d')}.csv"
            filepath = os.path.join(FAILURE, filename)

        with open(filepath, 'a', encoding="UTF-8") as write_file:
            write_file.write(day_order.row_string() + "\n")


def main(order_day=None):
    """main処理
    """
    
    order_day = dt.date.today()

    # 商品一覧読み込み
    items = load_item()

    # 当日の注文受付ファイルを読み込む
    load_order = read_order(order_day)

    validated_orders = []
    failed_orders = []
    # 注文リストを一つ一つ確認する
    for order in load_order:

        # バリテーションチェックをする。
        # すべてTrueならvalidated_ordersにいれる。
        if order.validate(items):
            validated_orders.append(order)

        # １つでもFalseの場合は、failed_ordersにいれる。
        else:
            failed_orders.append(order)

    # 日別注文ファイル書き込み
    if validated_orders:
        write_orders(validated_orders)

    # 注文受付失敗ファイル書き込み
    if failed_orders:
        write_orders(failed_orders, order_day, failure=True)


if __name__ == "__main__":

    # main(dt.date(2016, 12, 14))
    main()
