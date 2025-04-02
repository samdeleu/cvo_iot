from lib import simpleWifi_v2

print("Opening wifi")
wifi = simpleWifi_v2.Wifi()

wifi.open_static("192.168.0.10","255.255.255.0","192.168.0.1","195.130.131.5")
if wifi.get_status() > 0:
    print("connected")
    print(wifi.get_IPdata())
else:
    print("not connected")