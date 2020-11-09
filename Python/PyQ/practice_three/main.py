# 自動販売機

import random

class Drink:
    """
    飲み物に関するクラス
    """
    def __init__(self, name, price, stock):
        self.name = name  # 名称
        self.price = price  # 価格
        self.stock = stock  # 在庫

    def info(self):
        """情報（名称と価格）を返す"""
        return self.name + ' ' + str(self.price) + '円'


class VendingMachine:
    """
    自動販売機に関するクラス
    """
    def __init__(self):
        self.drink_list = []  # 飲み物一覧

    def show_all(self):
        """全ての飲み物を表示"""
        for drink in self.drink_list:
            print(drink.info())

    def add_drink(self, drink):
        """1種類の飲み物を登録"""
        self.drink_list.append(drink)

    def select_drink(self, kth):
        """kth番目の飲み物の情報を返す"""
        return self.drink_list[kth].info()
    
    def show_selected_drink(self, kth):
        """kth番目の飲み物の売り切れまたは値段を表示"""
        if self.drink_list[kth].stock:
            print(f'サイダーを選択しました。{self.drink_list[kth].price}円になります')
        else:
            print('売り切れ')

    def gacha(self):
        """ガチャ（1/5の確率で当たり（True）を返す）"""
        return random.randint(1, 5) == 1

    def purchase_drink(self, kth, fee):
        """お金feeを投入してkth番目の飲み物を1本購入"""
        if self.drink_list[kth].price > fee:
            print(f'{fee}円が投入されました。')
            print("購入金額が足りません")
            return
        
        if fee - self.drink_list[kth].price > 0:
            print(f'{fee}円が投入されました。')
            print(f'{fee - self.drink_list[kth].price}円のお釣りになります')
            self.drink_list[kth].stock -= 1
        
        if self.drink_list[kth].stock > 0 and self.gacha():
            print('大当たりーーー')
            print('もう1本 「' + self.drink_list[kth].name + "」を差し上げます！")
            self.drink_list[kth].stock -= 1



vm = VendingMachine()
vm.add_drink(Drink('珈琲', 130, 10))
vm.add_drink(Drink('お茶', 150, 12))
vm.add_drink(Drink('サイダー', 110, 2))

print('=== 全商品の表示 ===')
vm.show_all()

print('\n=== 3番目の商品のボタンを押します ===')
vm.show_selected_drink(2)

print('\n=== 3番目の商品を選択し100円を投入 ===')
vm.purchase_drink(2, 100)

print('\n=== 3番目の商品を選択し150円を投入 ===')
vm.purchase_drink(2, 150)

print('\n=== 3番目の商品のボタンを押します ===')
vm.show_selected_drink(2)

