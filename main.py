import pandas as pd
from datetime import datetime
import pytz
import os

from myclass import *

RECEIPT_FOLDER="./receipt"
os.makedirs(RECEIPT_FOLDER, exist_ok=True)

### メイン処理
def main():

    # マスタを定義しているcsvを読み込み行ごとにリスト化
    df = pd.read_csv('item_master.csv', header=None, dtype=str, encoding='utf-8-sig')
    item_list = df.to_numpy().tolist()
    
    
    # Itemクラスを通してobjectにしてlist格納へ
    item_master=[]
    for item in item_list:
        item_master.append(Item(item[0],item[1],int(item[2])))


    # オーダー登録。登録されたオーダーをdf化する
    order = Order(item_master)
    df = order.view_item_list()

    
    # オーダー登録。登録されたオーダーをdf化する
    payment = Payment(df)
    df = payment.pay(df)

    # 時間をdfの新規列として登録
    jst = pytz.timezone('Asia/Tokyo')
    time = datetime.now(tz=jst).strftime('%Y-%m-%d-%H-%M-%S')
    df['time'] = time
    
    # CSV出力
    df.to_csv(f'{RECEIPT_FOLDER}/output_{time}.txt', encoding='utf-8-sig')
    
        
if __name__ == "__main__":
    main()