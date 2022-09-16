# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 13:54:32 2022

@author: neera
"""

from fyers_api import fyersModel
from fyers_api import accessToken
import login
import os

client_id = '8S56FEB6JI-100'
secret_key = 'BGOWTLDD3I'
redirect_url = 'http://127.0.0.1:5000/login'


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

def historical_bydate(symbol, sd, ed, interval=1):
    data = {"symbol": symbol, "resolution": "5", "date_format": "1", "range_from": str(sd), "range_to": str(ed),
            "cont_flag": "1"}
    nx = fyers.history(data)
    cols = ['datetime', 'open', 'high', 'low', 'close', 'volume']
    df = pd.DataFrame.from_dict(nx['candles'])
    df.columns = cols
    df['datetime'] = pd.to_datetime(df['datetime'], unit="s")
    df['datetime'] = df['datetime'].dt.tz_localize('utc').dt.tz_convert('Asia/Kolkata')
    df['datetime'] = df['datetime'].dt.tz_localize(None)
    df = df.set_index('datetime')
    return df


#dat = datetime.datetime.now().strftime("%Y-%m-%d")
#dat1 = datetime.date(2022, 1, 10).strftime("%Y-%m-%d")
#data = {"symbol": "NSE:SBIN-EQ", "resolution": "1", "date_format": "1", "range_from": dat1, "range_to": dat,
#        "cont_flag": "1"}
#x = fyers.history(data)
#df = pd.DataFrame.from_dict(x['candles'])
#cols = ['datetime','open','high','low','close','volume']
#df.columns = cols
#df['datetime'] = pd.to_datetime(df['datetime'],unit = "s")
#df['datetime'] = df['datetime'].dt.tz_localize('utc').dt.tz_convert('Asia/Kolkata')
#df['datetime'] = df['datetime'].dt.tz_localize(None)
#df = df.set_index('datetime')

sd = datetime.date(2017, 7, 3)
enddate = datetime.datetime.now().date()
df = pd.DataFrame()

n = abs((sd - enddate).days)
ab = None

while ab == None:
    sd = (enddate - datetime.timedelta(days=n))
    ed = (sd + datetime.timedelta(days=99 if n > 100 else n)).strftime("%Y-%m-%d")
    sd = sd.strftime("%Y-%m-%d")
    dx = historical_bydate("NSE:ADANIPORTS-EQ", sd, ed)
    df = df.append(dx)
    n = n - 100 if n > 100 else n - n
    print(n)
    if n == 0:
        ab = "done"

df.to_csv(r"D:\projects\adaniports.csv")

# df.loc['2017-08-21']
