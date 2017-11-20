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

def getCurrencyList():
    r = requests.get('https://api.coindesk.com/v1/bpi/supported-currencies.json')

    return r.json()

if __name__ == "__main__":
    options, remainder = getopt.getopt(sys.argv[1:], 'c:hl', ['currency=','help','list'])
    
    for opt, arg in options:
        if opt in ('-c', '--currency'):
            currency = arg
        
        if opt in ('-l', '--list'):
            for c in getCurrencyList():
                print(c['currency'] + ": " + c['country'])
            exit()
        
        elif opt in ('-h', '--help'):
            print('example: ticker.py -c GBP')
            print(' -l or --list to list all available currencies')
            exit()

    curses.wrapper(main)
