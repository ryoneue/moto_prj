from tiny_line import tiny_line


import socket
# from machine import Pin
import time

#from pio_timer import pio_timer

# from machine import RTC
import json
import sys

if "MicroPython" in sys.version:
    import urequests as requests
    from wifi import Wifi
    from ntp_date import ntp_date
    date = ntp_date()
else:
    import requests as requests
    from datetime import datetime as date

    
head = """
HTTP/1.1 200 OK
Content-Type: text/html

"""
def set_wifi_info(json_file="info.json"):
    #Wi-FiのSSIDとパスワードを読み込み
    with open(json_file) as f:
        info = json.load(f)
    ssid = info["ssid"]
    password = info["password"]
    access_token = info["access_token"]
    if "MicroPython" in sys.version:
        net = Wifi(ssid, password)
        status = net.status
        print("status: ",status)
    else:
        net = False
        status = False
        
    return net, status, access_token, ssid, password


# html読み込み
html = ""
with open("./moto.html", encoding='utf-8') as f:
    for line in f:
        html = html + line



# Open socket
net, status, access_token, _, _ = set_wifi_info(json_file="info.json")
if "MicroPython" in sys.version:
    print("status:", type(status[0]))    
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
else:
    host = 'localhost'
    host = '0.0.0.0'
    port = 8001    
    addr = (host, port)
    # addr = socket.getaddrinfo('0.0.0.0', 8001)[0][-1]
    print(addr)
    # status = ['http://127.0.0.1:8001/']
s = socket.socket()
s.bind(addr)
s.listen(1)

# 通知用Line設定
if "MicroPython" in sys.version and (not access_token==False or not access_token=="False"): 
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
        now = date.now
        # cl, addr = s.accept()
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024).decode('utf-8')
        print("request:")
        print(request)
        # request = str(request)
        
        # %以下の変数がhtml内部に代入される
        response = html % (date, M1, M2, M3)
        if not "MicroPython" in sys.version:
            response = head + response
        cl.sendall(response.encode('utf-8'))        
        # cl.send(response)
        cl.close()
        # 1秒ごとにページを作成しなおす
        time.sleep(1)
        
    except OSError as e:
        cl.close()
        print('connection closed')

    
