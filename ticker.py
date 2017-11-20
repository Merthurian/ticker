#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import curses
import json
import time
import sys
import getopt

currency = 'GBP'

def main(stdscr):
        
    curses.curs_set(0)

    while True:
        stdscr.clear()
        
        height,width = stdscr.getmaxyx()
        height -= 1

        url = 'https://api.coindesk.com/v1/bpi/currentprice/' + currency + '.json'
        
        r = requests.get(url)
        
        fPrice = float(r.json()['bpi'][currency]['rate'].replace(',',''))
        sPrice = "{0:.2f}".format(fPrice)

        stdscr.addstr(sPrice)
                
        stdscr.refresh()

        time.sleep(60)

if __name__ == "__main__":
    options, remainder = getopt.getopt(sys.argv[1:], 'c:h', ['currency=','help'])
    for opt, arg in options:
        if opt in ('-c', '--currency'):
            currency = arg
        elif opt == '--help':
            println('example: ticker.py -c GBP')
            exit()

    curses.wrapper(main)
