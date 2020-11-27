import argparse
import datetime as dt
from dateutil.relativedelta import relativedelta



def main(day, ago):
    day_ago = day - relativedelta(months=ago)

    print(f"day    : {day}")
    print(f"day_ago: {day_ago}")



if __name__ == '__main__':
# パーサーをつくる
    parser = argparse.ArgumentParser(description="プログラムの説明")

    # parser.add_argumentで受け取る引数を追加していく
    parser.add_argument(
        'args1',                                                         # 必須引数
        help="時間",                                                     # 引数の説明
        type=lambda x: dt.datetime.strptime(x, '%Y%m%d'),                # 型指定
        # action=,                                                       # フラグとして扱う
        # choices=)                                                      # 指定内容を選択肢の中から選ぶ
       )                                                      
    parser.add_argument(
        '--args2',                                                       # --をつけるとオプション引数
        # default=,                                                      # デフォルト値設定
        # help=,
        # type=,
        # help=)    
      )
    # 引数を解析
    args = parser.parse_args()

    day = args.args1
    ago = ago if ago else 1
    main(day, ago)
