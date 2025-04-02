import json

mac_addrs = None
with open("macaddr.json", "r") as f:
    print("XXXXX")
    mac_addrs = json.load(f)

print(mac_addrs)