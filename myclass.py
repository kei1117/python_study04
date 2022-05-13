import pandas as pd
import copy

# ## print文に表示する色管理クラス
class Color:
    RED = '\033[31m'#(文字)赤
    GREEN = '\033[32m'#(文字)緑
    YELLOW = '\033[33m'#(文字)黄
    BLUE = '\033[34m'#(文字)青
    RESET = '\033[0m'#全てリセット

	
### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code = item_code
        self.item_name = item_name
        self.price = price

    def get_price(self):
        return self.price
    
    
### オーダークラス
class Order():
    def __init__(self,item_master):
        self.item_order_list = []
        self.item_master = item_master
        
        self.confirm_order()
        
        
    def confirm_order(self):

        while True:
            try:
                start = input(f'★商品の登録をする場合 : {Color.YELLOW}1{Color.RESET}\n★登録を完了する場合   : {Color.YELLOW}0{Color.RESET} を入力してください ... ')
                if int(start) != 0:
                    
                    # 購入する商品と個数を登録
                    buy_item = self.check_item_code(self.item_master)
                    item_number = self.confirm_count()
                    
                    self.add_item_order(buy_item, item_number)
        
                else:
                    print(f'{Color.YELLOW}商品登録を終了します。{Color.RESET}')
                    break    
            except Exception as e:
                print('エラーーー！',e)
                print(f'{Color.RED}入力値エラー! 1か0を入力してください{Color.RESET}')


    def check_item_code(self,item_master):
        print(f'対象の商品コード:{Color.YELLOW}{[ item.item_code for item in item_master ]}{Color.RESET}')
        item_code = input('購入する商品コードを上の数字の中から選択してください ... ')
        
        for item in item_master:
            if item.item_code == item_code:
                return item_code
            
        print(f'{Color.RED}該当の商品コードがありません。下記の商品コードの中から選択してください！{Color.RESET}')
        return self.check_item_code(item_master)


    def confirm_count(self):
        item_count = input(f'購入する個数は? ... ')
    
        try:
            item_count = int(item_count)
        except:
            print(f'{Color.RED}文字ではなく数値を入力してください!{Color.RESET}')
            return self.confirm_count()
        
        if item_count <= 0 :
            print(f'{Color.RED}1以上を入力してください!{Color.RESET}')
            return self.confirm_count()
        else:
            print(f'{Color.YELLOW}続いて{Color.RESET}')
            return item_count
        
        
    def add_item_order(self, buy_item, item_number):
        
        for i in self.item_master:
            if i.item_code == buy_item:
                # クラスオブジェクトをdictへ変換してオーダーのあった個数を追加
                # https://kuzunoha-ne.hateblo.jp/entry/2019/01/25/213300
                # そしてdeepコピー
                # https://docs.python.org/ja/3/library/copy.html
                dict = copy.deepcopy(i.__dict__)
                dict['count'] = item_number
                self.item_order_list.append(dict)

        
    def view_item_list(self):
        df = pd.DataFrame(self.item_order_list)
        
        df['total'] = df['price'] * df['count']# 商品ごとの合計値(単価×個数)列を追加
        df = df.groupby(['item_code', 'item_name'],as_index=False).sum() # 同一商品はサマリにして合計する
        df['price'] = (df['total'] / df['count']) # 単価もサマリされてしまうので元に戻す(合計値/個数)
        df.loc['total'] = df.sum(numeric_only=True) # 全商品の合計金額と合計数の「行」を追加。
        print(f'{Color.GREEN}オーダーされた商品は\n{Color.RESET}{df}')
        
        return df
    
    

### 支払い処理クラス
class Payment():
    def __init__(self, df):
        self.total_count = df.loc['total','count']
        self.total_amount = df.loc['total','total']
        
        print(f'合計個数 : {Color.GREEN}{int(self.total_count)}個{Color.RESET}です。')
        print(f'合計金額 : {Color.GREEN}{int(self.total_amount)}円{Color.RESET}です。') 
        

    def pay(self, df):
        payment = input(f'合計金額は{Color.YELLOW}{int(self.total_amount)}円{Color.RESET}です。お支払い金額を入力してください？{Color.RESET}')
        
        try:
            change = int(payment) - int(self.total_amount)
        except:
            print(f'{Color.RED}支払い金額を入力してください!{Color.RESET}')
            return self.pay(df)
        
        if int(payment) < int(self.total_amount) :
            print(f'{Color.RED}支払い金額が足りません!もう一度入力してください{Color.RESET}')
            return self.pay(df)
        else:
            print(f'ありがとうございます。お釣りは{Color.YELLOW}{change}円{Color.RESET}です')
            
            df.loc['payment','total'] = payment
            df.loc['change','total'] = change
        
        return df
            
    
    
    