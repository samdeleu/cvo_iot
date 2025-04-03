import json

addrs = None
with open("macs.json","r") as f:#laden json bestand
    addrs = json.load(f)

print("mac adressen:",addrs)