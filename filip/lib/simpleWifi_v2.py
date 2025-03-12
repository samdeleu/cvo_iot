import wifi_data_v2
import network
import time
from machine import Pin
class Wifi:
    
    bConnected = False
    
    def __init__(self):
        """ activation WLAN interface"""
        self.net=None
        self.status=0
        self.wdata=wifi_data_v2.Data
        try:
            self.net=network.WLAN(network.STA_IF)
            self.net.active(True)
        except Exception as e:
            self.status = -1
            if self.wdata.debug:
                print(e)
    
    def open(self):
        """connect to SSID from wifi_data"""
        try:
            print(f"Opening a connection to the WIFI")
            for j in range(0,len(self.wdata.ssid)):
                print(f"Trying: -{j}:{self.wdata.ssid[j]}-")
                for t in range(0,self.wdata.times_try):
                    try:
                        print(" ...net.connect")
                        self.net.connect(self.wdata.ssid[j],self.wdata.pwd[j])
                        if self.net.isconnected():
                            print(" ...net.isconnected == True")
                            self.status = 1
                            Wifi.bConnected = True
                            return True
                        print(" ...net.isconnected == False")
                        time.sleep_ms(100)
                    except:
                        time.sleep(100)
            self.status = -1
            return False
        except Exception as e:
            print(f"Exception: {e}")
            self.status = -1
            if self.wdata.debug:
                print(e)
            return False
        
    def open_static(self,ip,subnet,gateway,dns):
        print("Setting static IP address")
        self.net.ifconfig((ip,subnet,gateway,dns))
        """connect to SSID from wifi_data"""
        try:
            for j in range(0,len(self.wdata.ssid)):
                for t in range(0,self.wdata.times_try):
                    try:
                        self.net.connect(self.wdata.ssid[j],self.wdata.pwd[j])
                        if self.net.isconnected():
                            self.status = 1
                            Wifi.bConnected = True
                            return True
                        time.sleep_ms(100)
                    except:
                        time.sleep_ms(100)
            self.status = -1
            return False
        except Exception as e:
            print("Error Connection")
            self.status = -1
            if self.wdata.debug:
                print(e)
            return False

    def close(self):
        """disconnect"""
        self.net.disconnect()
        self.status = 0
        Wifi.bConnected = False
    
    def get_status(self):
        """gives status by blinking LED
        status NOK: 10 short flash
        status OK: Long on - short off - long on"""
        led_board=Pin(2,Pin.OUT)
        if self.status <= 0:
            for t in range(0,10):
                led_board.value(1)
                time.sleep_ms(100)
                led_board.value(0)
                time.sleep_ms(100)
        else:
            led_board.value(1)
            time.sleep_ms(1000)
            led_board.value(0)
            time.sleep_ms(2000)
            led_board.value(1)
            time.sleep_ms(1000)
            led_board.value(0)
        return self.status
    
    def checkWifiConnect(self):
        """Check if the ESP is still connected to the network
        if not, try to reconnect"""
        if self.get_IPdata() == "" or self.get_IPdata()[0]=="0.0.0.0":
            self.status=0
            self.open()
            self.get_status()

    def get_IPdata(self):
        """Get IP data"""
        if self.status>0:
            return self.net.ifconfig()
        else:
            return ""
