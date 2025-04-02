from lib import simpleWifi_v2

print("Opening wifi")
wifi = simpleWifi_v2.Wifi()

wifi.open()
if wifi.get_status() > 0:
    print("connected")
    print(wifi.get_IPdata())
else:
    print("not connected")