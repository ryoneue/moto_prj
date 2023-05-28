from tiny_line import tiny_line
import urequests as requests
import network
import utime
import socket
from machine import Pin
import time
from wifi import Wifi
#from pio_timer import pio_timer
from ntp_date import ntp_date
from machine import RTC
import json

def set_wifi_info(json_file="info.json"):
    #Wi-FiのSSIDとパスワードを読み込み
    with open(json_file) as f:
        info = json.load(f)
    ssid = info["ssid"]
    password = info["password"]
    access_token = info["access_token"]
    net = Wifi(ssid, password)
    status = net.status
    return net, status, access_token, ssid, password

# html読み込み
html = ""
with open("./moto.html", encoding='utf-8') as f:
    for line in f:
        html = html + line

net, status, access_token, _, _ = set_wifi_info(json_file="info.json")

# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

# 通知用Line設定
if not access_token==False or not access_token=="False": 
    tl = tiny_line(access_token, debug=True)
    print('listening on', addr)
    tl.notify("http://"+status[0])


"""
設備の生産数を検出する処理
M1 = get_data()
M2 = get_data()
M3 = get_data()
"""

M1 = 10000
M2 = 20000
M3 = 30000


count = 0
value = 0
# 以下ループ処理
# 変数M1,M2,M3を更新したWebページを作成する（もっと頻度を落としてもいいかも）
while True:
    try:
        date = ntp_date()
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print("request:")
        print(request)
        request = str(request)
        
        # %以下の変数がhtml内部に代入される
        response = html % (date.date, M1, M2, M3)
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        # 1秒ごとにページを作成しなおす
        time.sleep(1)
        
    except OSError as e:
        cl.close()
        print('connection closed')

    