#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import re
import os
import sys
from optparse import OptionParser, OptionValueError
from browser import get_browser

URLREGEX = r'''(?i)(?:http|ftp)s?://[]:/?#@!$&'()*+,;=A-z\d\-._~%[]*'''
URLSERVICE = '''http://tinyogg.com/add?url=%s&type=video&hidden=true'''
LOGFILE = os.path.expanduser('''~/.tinyogg''')
RESULT = '''http://tinyogg.com/watch/'''
RESULTREGEX = r'''href="/watch/(.*?)/"'''


def convert(originalurl, log=True):
    browser = get_browser()
    form = browser.get_forms("http://tinyogg.com")[0]
    form["url"] = originalurl
    form.submit()
    
    if RESULT in browser.get_url():
        return browser.get_url()

    match = re.search(RESULTREGEX, browser.get_html())
    if match:
        return RESULT + match.group(1)
    
    for match in re.finditer(URLREGEX, browser.get_html()):
        if RESULT in match.group():
            return match.group()


def main():
    # Instance the parser and define the usage message
    parser = OptionParser(usage="""
    %prog [-hwqv] urltoflashvideo""", version="%prog .1")

    # Define the options and the actions of each one
    parser.add_option("-v", "--verbose", action="count", dest="verbose",
        help="increase verbosity of the output")
    parser.add_option("-q", "--quiet", action="count", dest="quiet",
        help="decrease verbosity of the output")
    parser.add_option("-H", "--highquality", action="store_true", dest="hq",
        help="try to conver the higest quality avaiable version")
    parser.add_option("-w", "--wait", action="store_true", dest="wait",
        help="dont quit until the video was converted")

    # Define the default options
    parser.set_defaults(
        verbose=2,
        quiet=0,
        hq=False,
        wait=False,
    )

    # Process the options
    opts, args = parser.parse_args()

    if len(sys.argv) > 1:
        for url in sys.argv[1:]:
            print convert(url)
        return
    else:
        print "Se debe pasar las urls como argumento"
        return 1



if __name__ == "__main__":
    exit(main())
