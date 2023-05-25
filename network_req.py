from tiny_line import tiny_line
import urequests as requests
import network
import utime
import socket
from machine import Pin
import time
from wifi import Wifi
from pio_timer import pio_timer

led = Pin("LED", machine.Pin.OUT)
ledState = 'LED State Unknown'
html = """<!DOCTYPE html><html>
<head><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}
.buttonGreen { background-color: #4CAF50; border: 2px solid #000000;; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
.buttonRed { background-color: #D11D53; border: 2px solid #000000;; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
</style>
<meta http-equiv="refresh" content="5">
</head>
<body><center><h1>Raspberry Pi Pico W</h1></center><br><br>
<form><center>
<center> <button class="buttonGreen" name="led" value="on" type="submit">LED ON</button>
<br><br>
<center> <button class="buttonRed" name="led" value="off" type="submit">LED OFF</button>
</form>
<br><br>
<br><br>
<p>%s<p></body></html>
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
# wlan = network.WLAN(network.STA_IF)
# wlan.active(True)
# wlan.connect(ssid, password)

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if net.wlan.status() < 0 or net.wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    utime.sleep(1)
    
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
    
wlan_status = net.wlan.status()
blink_onboard_led(wlan_status)


if wlan_status != 3:
    raise RuntimeError('Wi-Fi connection failed')
else:
    print('Connected')
    status = net.wlan.ifconfig()
    print('ip = ' + status[0])


# 初期化
tl = tiny_line(access_token, debug=True)
# メッセージ送信
# tl.notify("Raspberry Pi Pico Wのボタンが押されました！")

# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)
tl.notify("http://"+status[0])

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
        response = html % str(count)
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        time.sleep(1)
        
    except OSError as e:
        cl.close()
        print('connection closed')

    