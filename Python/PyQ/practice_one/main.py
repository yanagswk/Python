from datetime import datetime, date
import os
import re

# ファイルの定義（各ファイル名、ディレクトリ名を定数に代入）
ITEM_TSV_PATH = 'items.tsv'
ORDER_DIR = 'order/'
FAILURE_DIR = 'failure/'
DELIVERY_DIR = 'delivery/'


class Item:
    # Itemは辞書でもいいが、クラスにすることで、将来的にメソッドを追加するときに楽。
    """ 1商品に対応するクラス
    """
    def __init__(self, item_id, name, price):
        # 各属性を初期化
        self.item_id = item_id  # 商品ID
        self.name = name  # 商品名
        self.price = price  # 価格


class Items:
    """ 商品の一覧に対応するクラス
    """
    def __init__(self, items):
        #  属性itemsにItemインスタンスをリストに持つ値を代入する
        self.items = items

    def has_id(self, item_id):
        """ item_id をもつ商品が存在するかチェックする
        """
        # Itemsに含まれる商品一覧に引数で指定されたitem_idを持つ商品が存在するか確認
        for item in self.items:  # ここの変数itemは、Itemのインスタンス
            # 右辺のitem_idは注文ファイル側の商品ID
            if item.item_id == item_id:
                return True
        return False


class Order:
    """ 1つの注文を表すクラス
    """
    AMOUNT_RE = re.compile(r'^[0-9]+$')
    TEL_RE = re.compile(r'^[0-9]{2,4}-[0-9]{4}-[0-9]{4}$')

    def __init__(self, item_id, amount, shipping_address, tel_number,
                 fullname, shipping_date_str, order_file):
        # 各属性を初期化（注文ファイルの1行分の内容を各属性に代入）
        self.item_id = item_id  # 商品ID
        self.amount = amount  # 個数（文字列）
        self.shipping_address = shipping_address  # 宅配住所
        self.tel_number = tel_number  # 電話番号
        self.fullname = fullname  # 氏名
        self.shipping_date_str = shipping_date_str  # 宅配日（文字列）
        self.order_file = order_file  # 元のファイル名

        self.amount_int = None  # 個数（数値）
        self.shipping_date = None  # 宅配日（datetime）

    def validate(self, items):
        """ 各注文の値が正しいかバリデーションチェックする。OKの場合True、NGの場合False
        """
        # 商品マスタ（引数のitems）に存在する商品ID（item_id）が存在するか確認
        if not items.has_id(self.item_id):
            return False
        # 個数amountが数値で指定されているか正規表現で確認
        if not self.AMOUNT_RE.search(self.amount):
            return False
        # ファイルから取り出して文字列なので、整数型に変更
        self.amount_int = int(self.amount)
        # 値がマイナスでないか確認
        if self.amount_int <= 0:
            return False
        # 宅配先住所に値が設定されているか確認
        if not self.shipping_address:
            return False
        # 電話番号が正しい形式で指定されてるか正規表現で確認
        if not self.TEL_RE.search(self.tel_number):
            return False
        # 名前が指定されているか確認
        if not self.fullname:
            return False
        # 宅配日が正しく日付として扱えるか、変換して確認
        # 変換の途中でエラーが起きたら、日付として正しくない
        try:
            self.shipping_date = datetime.strptime(self.shipping_date_str, '%Y-%m-%d')
        except ValueError:
            return False
        # 全て成功したらTrueを返す
        return True

    def row_string(self):
        # 1注文の一覧をカンマ（,）区切りで結合して、返す
        return ','.join((
            self.item_id,
            self.amount,
            self.shipping_address,
            self.tel_number,
            self.fullname,
            self.shipping_date_str,
            self.order_file,
        ))


def load_items():
    """ ITEM_TSV_PATHのTSVからItemsを作る
    """
    # 読み込んだItemを保存しておくリスト
    items = []
    # 商品マスター（items.tsv）を読み込む
    with open(ITEM_TSV_PATH, encoding='utf-8') as f:
        # 1行ずつ処理
        for row in f:
            # 1行の文字列をタブ文字(\t)で分割
            # 商品ID(item_id)、商品名(name)、価格(price)の各変数に値を代入
            item_id, name, price = row.split('\t')
            # Item（1商品のデータ）作成
            item = Item(item_id.strip(), name.strip(), price.strip())
            # リストに追加
            items.append(item)
    # Items（全商品のデータ）に追加して、Itemsを作成し、返す
    return Items(items)


def load_orders(target_date):
    """ ORDER_DIR のCSVからOrderのリストを作る

    * 各値の前後から空白を除外する
    """
    date_str = f'{target_date:%Y%m%d}'
    orders = []
    # 注文受付ファイル（order/の下のcsvファイル）読み込み
    for filename in os.listdir(ORDER_DIR):
        if date_str not in filename:
            # 対象日でないファイルは無視する
            continue

        filepath = os.path.join(ORDER_DIR, filename)
        with open(filepath, encoding='utf-8') as f:
            for row in f:
                # 各行のデータからOrder（1注文のデータ）を作成
                item_id, amount, address, tel, name, shipping_date = row.split(',')
                order = Order(
                    item_id.strip(),
                    amount.strip(),
                    address.strip(),
                    tel.strip(),
                    name.strip(),
                    shipping_date.strip(),
                    filename,
                )
                # リストordersに作成した注文データを追加
                orders.append(order)
    # 読み込んだ注文のリストを作成し、返す
    return orders


def write_deliver_orders(orders):
    """ Orderのリストを受け取って日別注文ファイルに書き込み
    """
    # 宅配日毎に集計。ファイルをオープンする回数を減らすため事前にまとめる
    date_orders = {}
    for order in orders:
        if order.shipping_date in date_orders:
            date_orders[order.shipping_date].append(order)
        else:
            date_orders[order.shipping_date] = [order]

    for d, day_orders in date_orders.items():
        filename = 'delivery_{}.csv'.format(d.strftime('%Y%m%d'))
        filepath = os.path.join(DELIVERY_DIR, filename)
        with open(filepath, 'a', encoding='utf-8') as f:
            for order in day_orders:
                f.write(order.row_string() + '\n')


def write_failure_orders(orders, order_date):
    """ Orderのリストを受け取って注文受付失敗ファイルに書き込み
    """
    filename = 'failure_{}.csv'.format(order_date.strftime('%Y%m%d'))
    filepath = os.path.join(FAILURE_DIR, filename)
    with open(filepath, 'a', encoding='utf-8') as f:
        for order in orders:
            f.write(order.row_string() + '\n')


def main(target_date=None):
    """ 毎日の注文集計用スクリプト

    1. 商品マスター読み込み
    2. 当日分の注文受付ファイル読み込み
    3. 注文をバリデーションチェック
    4. 日別注文ファイル書き込み
    5. 注文受付失敗ファイル書き込み
    """
    # 集計を行う日付を決め、変数target_dateに指定
    # 引数としてtarget_dateが指定されていれば、
    # 指定された日（今回の場合は、2016-12-14）
    # 引数のtarget_dateがNoneの場合は、実行時の日付を代入
    target_date = target_date or date.today()

    # 1. 商品マスター読み込み（load_items関数を呼び出し）
    # 結果を変数itemsに代入
    items = load_items()

    # 2. 当日分の注文受付ファイル読み込み（関数load_ordersを呼び出し）
    # 結果を変数ordersに代入
    orders = load_orders(target_date)

    # 保存用に空のリストvalidated_ordersとfailed_ordersを作成
    # 注文受け付けできる注文の場合は、リストvalidated_ordersに追加、
    # 注文受付失敗の注文の場合は、リストfailed_ordersに追加していきます。
    validated_orders = []
    failed_orders = []
    # 注文リストを1つずつ確認
    for order in orders:
        # 3. 注文をバリデーションチェック
        # 注文が正しいかチェック
        # Orderクラスに定義されているvalidateメソッドで確認
        # このチェックですべての確認が成功したらTrueが返り、失敗したらFalseが返ります。
        if order.validate(items):
            # 戻り値がTrueの場合はリストvalidated_ordersに追加
            validated_orders.append(order)
        else:
            # Falseの場合は、リストfailed_ordersに追加します。
            failed_orders.append(order)

    if validated_orders:
        # 4. 日別注文ファイル書き込み
        write_deliver_orders(validated_orders)
    if failed_orders:
        # 5. 注文受付失敗ファイル書き込み
        write_failure_orders(failed_orders, target_date)

# Start
if __name__ == '__main__':
    # 注文を確認する日付として動作確認用に2016-12-14を指定
    # main関数を呼び出し
    main(date(2016, 12, 14))  # あくまで動作確認用に日付を指定している