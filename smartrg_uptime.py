#!/usr/bin/env python
"""
    smartrg_uptime - A munin plugin for SmartRG router uptime (in hours because crappy system right now...)

    Copyright (C) 2014 Manuel Vonthron

    Like Munin, this plugin is licensed under the GNU GPL v2 license
    http://www.opensource.org/licenses/GPL-2.0
"""

import sys
import requests
import re

MODEM_URL = "http://192.168.1.1/admin/info.html"
login = ""
passwd = ""


def autoconf():
    """not supported right now"""
    pass

def config():
    print "graph_title Broadband uptime"
    print "graph_category Network"
    print "graph_vlabel Uptime"
    print "graph_args --base 1000 -l 0"

    print "uptime.label Uptime (hours)"

def main():
    """
    """
    def cleanup(content):
        return re.sub(r'(<!--.*?-->|<[^>]*>|\n)', ' ', content).strip()

    def bandwidth(text):
        """example: Rate (Kbps):  16192  7431"""
        r = re.compile("Uptime:<\/td>[\\n\\r\s]*<td>(\d*)D\s+(\d*)H.*<\/td>")
        res = r.findall(text)

        if res:
            return int(res[0][0])*24 + int(res[0][1])
        else:
            return None

    page = requests.get(MODEM_URL, auth=(login, passwd))
    if not page.ok:
        print page.reason
        return None
    #content = cleanup(page.text)
    uptime = bandwidth(page.text)

    print "uptime.value", uptime

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "config":
            config()
        elif sys.argv[1] == "autoconf":
            autoconf()
    else:
        main()
