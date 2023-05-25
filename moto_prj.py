from tiny_line import tiny_line
import urequests as requests
import network
import utime
import socket
from machine import Pin
import time
from wifi import Wifi
from pio_timer import pio_timer
from ntp_date import ntp_date
from machine import RTC
import json

# html読み込み
html = ""
with open("./moto.html", encoding='utf-8') as f:
    for line in f:
        html = html + line

timer = pio_timer(sm=1,freq=10000, pin=26)
ms = 10000 # カウントしたい秒数を代入
#     ms = 5000
timer.active()
timer.put(ms)
pin1 = Pin(26)

#自宅Wi-FiのSSIDとパスワードを読み込み
with open("info.json") as f:
    info = json.load(f)
ssid = info["ssid"]
password = info["password"]
access_token = info["access_token"]


net = Wifi(ssid, password)
status = net.status

date = ntp_date()


# 初期化
tl = tiny_line(access_token, debug=True)

# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

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
while True:
    try:
        check = pin1.value()!=value
        value = pin1.value()
        if check:
            count += 1
            timer.put(ms)
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print("request:")
        print(request)
        request = str(request)
        
#         ledState = "LED is OFF" if led.value() == 0 else "LED is ON" # a compact if-else statement
        
        # Create and send response
#         stateis = ledState
        response = html % (date.date, M1, M2, M3)
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        time.sleep(1)
        
    except OSError as e:
        cl.close()
        print('connection closed')

    