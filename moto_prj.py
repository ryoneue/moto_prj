from tiny_line import tiny_line
# import threading


import socket
# from machine import Pin
import time

#from pio_timer import pio_timer

# from machine import RTC
import json
import sys

# from flask import Flask, render_template

debug = False

if "MicroPython" in sys.version:
    import urequests as requests
    from wifi import Wifi
    from ntp_date import ntp_date
    date = ntp_date()
else:
    import requests as requests
    from datetime import datetime
    import threading
    from http.server import HTTPServer, SimpleHTTPRequestHandler

    

class moto_prj:
    def __init__(self):
        self.head = """HTTP/1.1 200 OK Content-Type: text/html

"""
    def set_wifi_info(self,json_file="info.json"):
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
        self.net = net
        self.status = status
        self.access_token = access_token
        
        # return net, status, access_token, ssid, password

    def setting(self):
        if "MicroPython" in sys.version:
            date = ntp_date()
            if (not self.access_token==False or not self.access_token=="False"):
                self.setting_line()            
        else:
            date = datetime.now()
        self.date = date





    def load_html(self, debug=False):
        # html読み込み
        if debug:
            file = "./moto_dbg.html"
        else:
            file = "./moto.html"

        html = ""
        with open(file, encoding='utf-8') as f:
            for line in f:
                html = html + line
        self.html = html


    def open_socket(self):
        # Open socket

        if "MicroPython" in sys.version:
            self.set_wifi_info(json_file="info.json")
            print("status:", type(self.status[0]))    
            addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

        else:

            addr = socket.getaddrinfo('0.0.0.0', 8000)[0][-1]
            print(addr)
            self.status = "False"
            self.access_token = "False"
            # status = ['http://127.0.0.1:8001/']
        
#         self.status = status
#         self.access_token = access_token
        self.addr = addr

        self.s = socket.socket()
        self.s.bind(addr)
        self.s.listen(1)
        
        

    def setting_line(self):
        # 通知用Line設定
        
        tl = tiny_line(self.access_token, debug=True)
        print('listening on', self.addr)
        tl.notify("http://"+self.status[0])

    def detect_count(self):
        """
        設備の生産数を検出する処理
        M1 = get_data()
        M2 = get_data()
        M3 = get_data()
        """

        self.M1 = 10000
        self.M2 = 20000
        self.M3 = 30000


        count = 0
        value = 0        

    def main_loop(self):
        # 以下ループ処理
        # 変数M1,M2,M3を更新したWebページを作成する（もっと頻度を落としてもいいかも）
        while True:
            try:
                # now = date.now
                # cl, addr = s.accept()
                cl, addr = self.s.accept()
                print('client connected from', addr)
                request = cl.recv(1024).decode('utf-8')
                print("request:")
                print(request)
                # request = str(request)
                
                # %以下の変数がhtml内部に代入される
                response = self.html % (self.date, self.M1, self.M2, self.M3)
        #         if not "MicroPython" in sys.version:
                response = self.head + response
                cl.sendall(response.encode('utf-8'))        
                # cl.send(response)
                # 1秒ごとにページを作成しなおす
                time.sleep(1)
                cl.close()

                
            except OSError as e:
                cl.close()
                print('connection closed')



func = moto_prj()

func.set_wifi_info(json_file="info.json")
func.load_html(debug=debug)
func.open_socket()
func.setting()
# func.setting_line()

func.detect_count()
func.main_loop()







    
