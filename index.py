import twstock
import requests
import schedule
import time


def get_two_float(f_str, n):
    a, b, c = f_str.partition('.')
    c = c[:n]
    return ".".join([a, c])

def sendToLine():
    stock2330 = twstock.realtime.get('2330')
    low2330 = stock2330['realtime']['low']
    high2330 = stock2330['realtime']['high']
    ltr2330 = stock2330['realtime']['latest_trade_price']
    msg2330=(f' \n GG 2330 \n {get_two_float(low2330, 2)} ||{get_two_float(high2330, 2)} \n 現價 {get_two_float(ltr2330, 2)} \n')
    print(msg2330)

    url = "https://notify-api.line.me/api/notify"
    payload={'message':{msg2330}}
    headers = {'Authorization': 'Bearer ' + '--Line Token--'}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


schedule.every(5).minutes.do(sendToLine)

while True:
    schedule.run_pending()
    time.sleep(1)