import sys
import re

TYPE_TERMINAL = 0
TYPE_AGENT    = 1

class Port() :
    def __init__(self, mac, ip, pnum = 1, ptype = TYPE_TERMINAL):
        self.pnum = pnum
        self.ip  = ip
        self.mac = mac
        self.ptype = ptype

        self.is_uplink = False

    def set_uplink(self, val) :
        self.is_uplink = val

    def set_pnum(self, val) :
        self.pnum = val

