""" Network node """
import aioespnow  # ESPNow met async support
import asyncio    # python async
import binascii
# import espnow
import network    # standaard network library
import sys

from .node import Node


class SensorNode(Node):
    def __init__(self):
        super()
        
#if __name__ == "__main__":
me = SensorNode()
asyncio.run(me.start())