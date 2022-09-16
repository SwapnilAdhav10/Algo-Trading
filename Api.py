from fyers_api import fyersModel
from fyers_api import accessToken
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






fyers = fyersModel.FyersModel(client_id=client_id, token=get_access_token(), log_path="D:\projects")

print(fyers.get_profile())

data = {"symbol":"NSE:SBIN-EQ","resolution":"D","date_format":"1","range_from":"2022-09-01","range_to":"2022-09-10","cont_flag":"1"}
is_async = True
print(fyers.history(data))
