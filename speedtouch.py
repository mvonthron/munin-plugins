#!/usr/bin/env python

import sys
import urllib
import re
import contextlib

MODEM_URL = "http://speedtouch.lan/cgi/b/dsl/dt/?be=0&l0=1&l1=0"

def autoconf():
    """not supported right now"""
    pass

def config():
    print "graph_title Broadband statistics"
    print "graph_category Network"

def main():
    """
    """
    def cleanup(content):
        return re.sub(r'(<!--.*?-->|<[^>]*>|\n)', ' ', content).strip()

    def bandwidth(text):
        """example: Bandwidth (Up/Down) [kbps/kbps]:856 / 13.801 """

        r = re.compile(r'Bandwidth \(Up\/Down\) \[.*\]\:\s*(-?\d+\.?\d*) \/ (-?\d+\.?\d*)')
        res = r.findall(content)
        print res

        if res:
            return res[0]
        else:
            return None, None

    with contextlib.closing(urllib.urlopen(MODEM_URL)) as u:
        content = u.read()

    content = cleanup(content)
    down, up = bandwidth(content)
    print down, up

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "config":
            config()
        elif sys.argv[1] == "autoconf":
            autoconf()
    else:
        main()
