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

# Wi-Fiの接続など必要な設定を行ってください



led = Pin("LED", machine.Pin.OUT)
ledState = 'LED State Unknown'
html = """<!DOCTYPE html>
<html>
<head>
    <title>Test</title>
    <style>
        .button {
            margin: 5px;
            padding: 10px;
        }
    </style>
</head>
<body>
    <h1>Todays count of production.</h1>
    <h1>%s</h1>
    <div>
        <button class="button" onclick="increaseNumber(1)">Machine 1</button>
        <span id="number1">%s</span>
    </div>
    <div>
        <button class="button" onclick="increaseNumber(2)">Machine 2</button>
        <span id="number2">%s</span>
    </div>
    <div>
        <button class="button" onclick="increaseNumber(3)">Machine 3</button>
        <span id="number3">%s</span>
    </div>

    <script>
        function increaseNumber(buttonNumber) {
            // 対応する数字要素のIDを取得
            var numberId = "number" + buttonNumber;

            // 数字を取得して増加させる
            var numberElement = document.getElementById(numberId);
            var currentNumber = parseInt(numberElement.innerHTML);
            var newNumber = currentNumber + 1;

            // 数字を更新
            numberElement.innerHTML = newNumber;
        }
    </script>
</body>
</html>
"""

timer = pio_timer(sm=1,freq=10000, pin=26)
ms = 10000 # カウントしたい秒数を代入
#     ms = 5000
timer.active()
timer.put(ms)
pin1 = Pin(26)

#自宅Wi-FiのSSIDとパスワードを入力
ssid = 'Buffalo-G-F5A0'
password = 'mck4wuvu7eypn'

access_token    = 'pwpqSJa9p5taVWtZJcmveowcSIeHD5nyghYqUPfSXF4'

net = Wifi(ssid, password)
status = net.status
# wlan = network.WLAN(network.STA_IF)
# wlan.active(True)
# wlan.connect(ssid, password)


    
# Define blinking function for onboard LED to indicate error codes    
def blink_onboard_led(num_blinks):
    led = machine.Pin('LED', machine.Pin.OUT)
    for i in range(num_blinks):
        led.on()
        utime.sleep(.2)
        led.off()
        utime.sleep(.2)
        
# Handle connection error
# Error meanings
# 0  Link Down
# 1  Link Join
# 2  Link NoIp
# 3  Link Up
# -1 Link Fail
# -2 Link NoNet
# -3 Link BadAuth        
#     
# wlan_status = net.wlan.status()
# blink_onboard_led(wlan_status)


date = ntp_date()
# print(date.date)


# 初期化
tl = tiny_line(access_token, debug=True)
# メッセージ送信
# tl.notify("Raspberry Pi Pico Wのボタンが押されました！")

# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

# print(date.date)
print('listening on', addr)
tl.notify("http://"+status[0])


"""
設備の生産数を検出する処理
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
        led_on = request.find('led=on')
        led_off = request.find('led=off')
        
        print( 'led on = ' + str(led_on))
        print( 'led off = ' + str(led_off))
        
        if led_on == 8:
            print("led on")
            cl.close()
            led.value(1)
        if led_off == 8:
            print("led off")
            led.value(0)
            
             
        
        ledState = "LED is OFF" if led.value() == 0 else "LED is ON" # a compact if-else statement
        
        # Create and send response
        stateis = ledState
        response = html % (date.date, M1, M2, M3)
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        time.sleep(1)
        
    except OSError as e:
        cl.close()
        print('connection closed')

    