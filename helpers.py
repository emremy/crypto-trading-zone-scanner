import os
import requests

def replace_coin_info(coin_name,interval):
    with open('./content/app', 'r') as file:
        filedata = file.read()
        filedata = filedata.replace('%COIN%', coin_name)
        filedata = filedata.replace('%INTERVAL%', interval)
        with open('./nuxt-tradingview/playground/app.vue', 'w') as nuxt_file:
            nuxt_file.write(filedata)

def check_trading_chart():
    if not os.path.exists('/nuxt-tradingview/'):
        response = requests.get('http://localhost:3000/')
        if response.status_code == 200:
            return True
    return False