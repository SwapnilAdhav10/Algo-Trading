# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 13:54:32 2022

@author: neera
"""
from fyers_api.Websocket import ws
from fyers_api import fyersModel
from fyers_api import accessToken
import datetime
import time
import document_file
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from fyers_api import fyersModel
from fyers_api import accessToken
import login
import os

client_id = '8S56FEB6JI-100'
secret_key = 'BGOWTLDD3I'
redirect_url = 'http://127.0.0.1:5000/login'

open_position = []


def getTime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def custom_message(msg):
    # print(msg)
    script = msg[0]['symbol']
    ltp = msg[0]['ltp']
    high = msg[0]['high_price']
    low = msg[0]['low_price']
    ltt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(msg[0]['timestamp']))
    print(f"Script: {script}, Ltp:{ltp}, High:{high}, Low:{low}, ltt:{ltt}")

    if (ltp <= low) and (script not in open_position):
        open_position.append(script)
        placeOrder("SELL", script, ltp)

    if (ltp >= high) and (script not in open_position):
        open_position.append(script)
        placeOrder("BUY", script, ltp)


def placeOrder(order, script, ltp):
    if order == "BUY":
        quantity = int(100)
        target_price = int(ltp * 0.02)
        stoploss_price = int(ltp * 0.01)

        order = fyers.place_order(
            {"symbol": script, "qty": quantity, "type": "2", "side": "1", "productType": "BO", "limitPrice": "0",
             "stopPrice": "0", "disclosedQty": "0", "validity": "DAY", "offlineOrder": "False",
             "stopLoss": stoploss_price, "takeProfit": target_price})
        print(
            f"Buy Order Placed for {script}, at Price: {ltp} for Quantity: {quantity}, with order_id: {order['id']} at time: {getTime()}")
        print(open_position)

    else:
        quantity = int(100)
        target_price = int(ltp * 0.02)
        stoploss_price = int(ltp * 0.01)

        order = fyers.place_order(
            {"symbol": script, "qty": quantity, "type": "2", "side": "-1", "productType": "BO", "limitPrice": "0",
             "stopPrice": "0", "disclosedQty": "0", "validity": "DAY", "offlineOrder": "False",
             "stopLoss": stoploss_price, "takeProfit": target_price})
        print(
            f"Sell Order Placed for {script}, at Price: {ltp} for Quantity: {quantity}, with order_id: {order['id']} at time: {getTime()}")
        print(open_position)


def get_access_token():
    if not os.path.exists('access_token.txt'):
        session = accessToken.SessionModel(client_id=client_id, secret_key=secret_key, redirect_uri=redirect_url,
                                           response_type='code', grant_type='authorization_code')
        response = session.generate_authcode()
        print("login URL", response)
        auth_code = input("Enter auth code :")
        session.set_token(auth_code)
        access_token = session.generate_token()['access_token']
        with open('access_token.txt', 'w') as f:
            f.write(access_token)

    else:
        with open('access_token.txt', 'r') as f:
            access_token = f.read()
    return access_token


fyers = fyersModel.FyersModel(client_id=client_id, token=get_access_token(), log_path="/")

import pandas as pd
import datetime
import pytz
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


# dat = datetime.datetime.now().strftime("%Y-%m-%d")
# dat1 = datetime.date(2022, 1, 10).strftime("%Y-%m-%d")
# data = {"symbol": "NSE:SBIN-EQ", "resolution": "1", "date_format": "1", "range_from": dat1, "range_to": dat,
#        "cont_flag": "1"}
# x = fyers.history(data)
# df = pd.DataFrame.from_dict(x['candles'])
# cols = ['datetime','open','high','low','close','volume']
# df.columns = cols
# df['datetime'] = pd.to_datetime(df['datetime'],unit = "s")
# df['datetime'] = df['datetime'].dt.tz_localize('utc').dt.tz_convert('Asia/Kolkata')
# df['datetime'] = df['datetime'].dt.tz_localize(None)
# df = df.set_index('datetime')

def main():
    symbol = ["NSE:ICICIPRULI-EQ", "NSE:GLENMARK-EQ", "NSE:WIPRO-EQ", "NSE:SYNGENE-EQ", "NSE:DLF-EQ"]
    # symbol = ["MCX:CRUDEOIL22MARFUT", "MCX:GOLDM22MARFUT"]

    orderplacetime = int(9) * 60 + int(20)
    closingtime = int(13) * 60 + int(35)
    timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)
    print(f"Waiting for 9.20 AM , Time Now:{getTime()}")

    while timenow < orderplacetime:
        time.sleep(0.2)
        timenow = (datetime.datetime.now().hour * 60 + datetime.datetime.now().minute)
    print(f"Ready for trading, Time Now:{getTime()}")


if __name__ == "__main__":
    main()
# df.loc['2017-08-21']
