import network
import utime

class Wifi():
    def __init__(self, ssid, password):    
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(ssid, password)
        #         self.status = wlan.status()
                
        # Wait for connect or fail
        max_wait = 10
        while max_wait > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            max_wait -= 1
            print('waiting for connection...')
            utime.sleep(1)
       
        wlan_status = self.wlan.status()
        self.check_connect_error(wlan_status)
        
    def check_connect_error(self, wlan_status):
        
        if wlan_status != 3:
            raise RuntimeError('Wi-Fi connection failed')
        else:
            print('Connected')
            status = self.wlan.ifconfig()
            print('ip = ' + status[0])
            self.status = status

       
        

