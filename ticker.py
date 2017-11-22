#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import curses
import json
import time
import sys
import getopt

currency = 'GBP'
my_coins = 0.0

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

        fMyValue = fPrice * my_coins
        sMyMalue = "{0:.2f}".format(fMyValue)

        if my_coins == 0.0:
            stdscr.addstr(sPrice)
        else:
            stdscr.addstr(sPrice + " " + sMyMalue)
                
        stdscr.refresh()

        time.sleep(60)

def getCurrencyList():
    r = requests.get('https://api.coindesk.com/v1/bpi/supported-currencies.json')

    return r.json()

if __name__ == "__main__":
    options, remainder = getopt.getopt(sys.argv[1:], 'c:hlm:', ['currency=','help','list','mycoins='])
    
    for opt, arg in options:
        if opt in ('-c', '--currency'):
            currency = arg
        
        if opt in ('-l', '--list'):
            for c in getCurrencyList():
                print(c['currency'] + ": " + c['country'])
            exit()
        
        if opt in ('-m' '--mycoins'):
            my_coins = float(arg)

        elif opt in ('-h', '--help'):
            print('example: ticker.py -c GBP')
            print(' -l or --list to list all available currencies')
            exit()

    curses.wrapper(main)
