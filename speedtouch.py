#!/usr/bin/env python
"""
    speedtouch - A munin plugin for Thomson Speedtouch bandwith statistics

    Copyright (C) 2013 Manuel Vonthron

    Like Munin, this plugin is licensed under the GNU GPL v2 license
    http://www.opensource.org/licenses/GPL-2.0
"""

import sys
import urllib
import re
import contextlib

MODEM_URL = "http://speedtouch.lan/cgi/b/dsl/dt/?be=0&l0=1&l1=0"

convertDottedThousands = lambda x: x.replace('.', '').replace(',', '.')

def autoconf():
    """not supported right now"""
    pass

def config():
    print "graph_title Broadband statistics"
    print "graph_category Network"
    print "graph_vlabel Bandwidth"
    print "graph_args --base 1000 -l 0"

    print "up.label Up (kbps)"
    print "down.label Down (kbps)"

def main():
    """
    """
    def cleanup(content):
        return re.sub(r'(<!--.*?-->|<[^>]*>|\n)', ' ', content).strip()

    def bandwidth(text):
        """example: Bandwidth (Up/Down) [kbps/kbps]:856 / 13.801 """

        r = re.compile(r'Bandwidth \(Up\/Down\) \[.*\]\:\s*(-?\d+\.?\d*) \/ (-?\d+\.?\d*)')
        res = r.findall(content)

        if res:
            return map(convertDottedThousands, res[0])
        else:
            return None, None

    with contextlib.closing(urllib.urlopen(MODEM_URL)) as u:
        content = u.read()

    content = cleanup(content)
    up, down = bandwidth(content)

    print "up.value", up
    print "down.value", down

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "config":
            config()
        elif sys.argv[1] == "autoconf":
            autoconf()
    else:
        main()
