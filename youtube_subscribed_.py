#!/usr/bin/env python
"""
    youtube_subscribed - A munin plugin to count youtube subscriptions
    copy/move/symlink the script so it gets the name of the channel as youtube_subscribed_<channelname>

    Copyright (C) 2014 Manuel Vonthron

    Like Munin, this plugin is licensed under the GNU GPL v2 license
    http://www.opensource.org/licenses/GPL-2.0
"""

import sys
import urllib
import re
import contextlib

BASE_URL = "https://www.youtube.com/user/"
BASE_PLUGIN_NAME = "youtube_subscribed_"

convertDottedThousands = lambda x: x.replace('.', '').replace(',', '.')

def autoconf():
    """not supported right now"""
    pass

def config(channel):
    print "graph_title Broadband statistics"
    print "graph_category Other"
    print "graph_vlabel Subs for %s" % channel.title()
    print "graph_args --base 1000 -l 0"

    print "count.label Subscriptions"

def main(channel):
    """
    """

    def countSubscribed(text):
        """example: <span class="yt-subscription-button-subscriber-count-branded-horizontal subscribed" >80</span>"""
        r = re.compile(r'<span class=\"yt-subscription-button-subscriber-count-branded-horizontal subscribed\" >([1-9](?:\d{0,2})(?:,\d{3})*)</span>')
        res = r.findall(content)
        
        if res:
            return int(res[0].replace(',', ''))
        else:
            return None

    with contextlib.closing(urllib.urlopen(''.join([BASE_URL, channel, "/about"]))) as u:
        content = u.read()

    count = countSubscribed(content)
    print "count.value", count

if __name__ == "__main__":
    if not sys.argv[0].startswith(BASE_PLUGIN_NAME) or sys.argv[0].split('.')[0] == BASE_PLUGIN_NAME:
        print "Plugin must have name formatted like: \"%s_<username>[.py]\"" % BASE_PLUGIN_NAME
        sys.exit(1)
    
    channel = sys.argv[0].split('.')[0][len(BASE_PLUGIN_NAME):]
    
    if len(sys.argv) == 2:
        if sys.argv[1] == "config":
            config(channel)
        elif sys.argv[1] == "autoconf":
            autoconf()
    else:
        main(channel)
