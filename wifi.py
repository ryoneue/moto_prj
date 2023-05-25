import network


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

        self.check_connect_error()
        
    def check_connect_error(self):
        
        if wlan_status != 3:
            raise RuntimeError('Wi-Fi connection failed')
        else:
            print('Connected')
            status = self.wlan.ifconfig()
            print('ip = ' + status[0])
            self.status = status
