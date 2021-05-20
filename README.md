# StockPrice_python_lineNotify
To Get The Real Time Stock Trade Price By Line Notify with Python Code


<a href="https://molly1024.medium.com/%E7%94%A8python%E5%AF%AB%E4%B8%80%E5%80%8Bline-notify-%E6%8E%A5%E6%94%B6%E5%8D%B3%E6%99%82%E8%82%A1%E5%83%B9%E9%80%9A%E7%9F%A5-use-python-to-get-the-real-time-stock-trade-price-by-line-notify-4d26deec85c4" target="_blank">Medium 圖文並茂版本 </a>


用python寫一個line notify，接收即時股價通知。Use Python To Get The Real Time Stock Trade Price By Line Notify.

寫一個python 連結line notify通知，籃後醬子就不用一直都利用上班叮盤啦～
（不過後來發現資料偶爾即時股價會缺漏，但基本的最高最低還是可以參考用）

做了幾天終於把bug弄完（之前卡在 1.回傳值只保留兩術後兩位 2.放上vscode後一直噴錯,結果是檔案名稱不能與套件名稱相同 3.如何讓他定期執行)

重0開始，有漏掉的步驟就.. 就算ㄌ
#### twstock
1. 下載python /  donwnload python  (Windows installer (64-bit) 記得path要勾) (建議用python3)
2. 有vscode https://code.visualstudio.com/download
3. 新增檔案 stock_linenotify.py  

開始寫code!

4. 安裝套件 pip install twstock requests lxml schedule time
（重點就這兩個 股價套件  twsotck / 自動執行套件 schedule / ）
兩個document都寫得很仔細，自己去看!

5. import 會用到的套件

```
import twstock
import requests
import schedule
import time
```

6. 先練習怎麼用 （我自己寫code會先切一小區塊小區塊，好比先用demo code看看有沒有問題，再繼續自己要抓的資料，不過前輩們寫code都是一條龍寫到底 然後就run起來XD）

```
stock = twstock.realtime.get('2330')
print(stock)
```

回傳資料：
```
{'timestamp': 1621477784.0, 'info': {'code': '2330', 'channel': '2330.tw', 'name': '台積電', 'fullname': '台灣積體電路製造股份有限公司', 'time': '2021-05-20 10:29:44'}, 'realtime': {'latest_trade_price': '562.0000', 'trade_volume': '9', 'accumulate_trade_volume': '11771', 'best_bid_price': ['562.0000', '561.0000', '560.0000', '559.0000', '558.0000'], 'best_bid_volume': ['176', '435', '1051', '283', '562'], 'best_ask_price': ['563.0000', '564.0000', '565.0000', '566.0000', '567.0000'], 'best_ask_volume': ['201', '484', '620', '112', '257'], 'open': '567.0000', 'high': '571.0000', 'low': '561.0000'}, 'success': True}
```

其中我要的就是 ['realtime']['low'] / ['latest_trade_price'] / ['high']
(目前最低 最高 即時股價)

籃後... 抓一抓就完成資料抓取ㄉ部份la
```
def get_two_float(f_str, n):
    a, b, c = f_str.partition('.')
    c = c[:n]
    return ".".join([a, c])
# 把回傳數字保留小數後兩位的function

stock2330 = twstock.realtime.get('2330')
low2330 = stock2330['realtime']['low']
high2330 = stock2330['realtime']['high']
ltr2330 = stock2330['realtime']['latest_trade_price']
msg2330=(f' \n GG 2330 \n {get_two_float(low2330, 2)} ||{get_two_float(high2330, 2)} \n 現價 {get_two_float(ltr2330, 2)} \n')
print(msg2330)
```

把這個資料 跟line notify連結，以及自動執行檔案的設定!

#### line notify /  requests
copy my code and change token

```
url = "https://notify-api.line.me/api/notify"
payload={'message':{msg2330}}
headers = {'Authorization': 'Bearer ' + 'LINE TOKEN'}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)
```
get token 登入 > 個人頁面
https://notify-bot.line.me/zh_TW/ 

點 發行權杖 點自己的帳號 就會有一串亂碼 複製起來
貼到上面的code
run code 就會收到資料啦



#### schedule / time
```
schedule.every(5).minutes.do(sendToLine) # 5分鐘跑一次schedule.every(20).seconds.do(sendToLine) # 20秒跑一次
while True:
    schedule.run_pending()
    time.sleep(1)
```


完成!




