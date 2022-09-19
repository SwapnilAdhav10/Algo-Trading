# pip install fyers-apiv2
# pip install selenium
# pip install webdriver-manager

from fyers_api.Websocket import ws
from fyers_api import fyersModel
from fyers_api import accessToken
import datetime
import time
import document_file
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

log_path = document_file.log_path
client_id = document_file.client_id
secret_key = document_file.secret_key
redirect_url = document_file.redirect_url
response_type = document_file.response_type
grant_type = document_file.grant_type
username = document_file.username
password = document_file.password
pin1 = document_file.pin1
pin2 = document_file.pin2
pin3 = document_file.pin3
pin4 = document_file.pin4

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


def generate_access_token(auth_code, appId, secret_key):
    appSession = accessToken.SessionModel(client_id=appId, secret_key=secret_key, grant_type="authorization_code")
    appSession.set_token(auth_code)
    response = appSession.generate_token()["access_token"]
    return response


def generate_auth_code():
    url = f"https://api.fyers.in/api/v2/generate-authcode?client_id={client_id}&redirect_uri={redirect_url}&response_type=code&state=state&scope=&nonce="
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.get(url)
    time.sleep(8)
    driver.execute_script(f"document.querySelector('[id=fy_client_id]').value = '{username}'")
    driver.execute_script("document.querySelector('[id=clientIdSubmit]').click()")
    time.sleep(8)
    driver.execute_script(f"document.querySelector('[id=fy_client_pwd]').value = '{password}'")
    driver.execute_script("document.querySelector('[id=loginSubmit]').click()")
    time.sleep(8)
    driver.find_element_by_id("verify-pin-page").find_element_by_id("first").send_keys(pin1)
    driver.find_element_by_id("verify-pin-page").find_element_by_id("second").send_keys(pin2)
    driver.find_element_by_id("verify-pin-page").find_element_by_id("third").send_keys(pin3)
    driver.find_element_by_id("verify-pin-page").find_element_by_id("fourth").send_keys(pin4)
    driver.execute_script("document.querySelector('[id=verifyPinSubmit]').click()")
    time.sleep(8)
    newurl = driver.current_url
    auth_code = newurl[newurl.index('auth_code=') + 10:newurl.index('&state')]
    driver.quit()
    return auth_code


def main():
    global fyers

    auth_code = generate_auth_code()
    access_token = generate_access_token(auth_code, client_id, secret_key)
    fyers = fyersModel.FyersModel(token=access_token, log_path=log_path, client_id=client_id)
    fyers.token = access_token
    newtoken = f"{client_id}:{access_token}"
    data_type = "symbolData"

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

    fs = ws.FyersSocket(access_token=newtoken, run_background=False, log_path=log_path)
    fs.websocket_data = custom_message
    fs.subscribe(symbol=symbol, data_type=data_type)
    fs.keep_running()


if __name__ == "__main__":
    main()
