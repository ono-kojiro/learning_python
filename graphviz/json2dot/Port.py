import sys
import re

class Port() :
    TYPE_TERMINAL = 0
    TYPE_AGENT    = 1

    def __init__(self, mac, ip, pnum=None, ptype = TYPE_TERMINAL):
        self.pnum = pnum
        self.ip  = ip
        self.mac = mac
        self.ptype = ptype

        if pnum is None :
            self.tag   = "dummy"
            self.label = ""
        else :
            self.tag   = "port{0}".format(pnum)
            self.label = "{0}".format(pnum)

        self.is_uplink = False

    def set_uplink(self, val) :
        self.is_uplink = val

    def set_pnum(self, val) :
        self.pnum = val

