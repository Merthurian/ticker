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
refresh = 60.0

low = 0.0
high = 0.0

price_history = []

def mapValue(value, inMin, inMax, outMin, outMax):
    
    inSpan = inMax + 0.001 - inMin - 0.001
    outSpan = outMax - outMin

    valueScaled = float(value - inMin) / float(inSpan)

    return outMin + (valueScaled * outSpan)

def drawGraph(stdscr, width, height):

    price_history_draw = price_history[-width:]
    
    global low, high

    low = min(price_history_draw)
    high = max(price_history_draw)
  
    price_squashed = []

    for price in price_history_draw:
        price_squashed.append(mapValue(price, low, high, height-1, 2))
    
    price_squashed = price_squashed[-(width-1):]

    i = 0

    for price in price_squashed:
        stdscr.move(int(price), i)
        stdscr.addch('+')
        i = i + 1

def getPrice():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/' + currency + '.json'
    r = requests.get(url)
     
    fPrice = float(r.json()['bpi'][currency]['rate'].replace(',',''))
    price_history.append(fPrice)
        
    while len(price_history) > 1000:
        price_history.pop(0)

    return fPrice

def main(stdscr):
        
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()

    nextCheck = 0.0
    
    currency_symbols = {'USD' : '$',
            'GBP' : curses.ACS_STERLING}
    
    currency_symbol = curses.ACS_DIAMOND

    if currency in currency_symbols:
        currency_symbol = currency_symbols[currency]

    while True:
        stdscr.clear()
        
        height,width = stdscr.getmaxyx()
        height -= 1

        if nextCheck < time.time():
            fPrice = getPrice()
            nextCheck = time.time() + refresh

        sPrice = "{0:,.2f}".format(fPrice)
        fMyValue = fPrice * my_coins
        sMyValue = "{0:,.2f}".format(fMyValue)

        sLow = "{0:,.2f}".format(low)
        sHigh = "{0:,.2f}".format(high)

        stdscr.addch(currency_symbol)

        stdscr.addstr(sPrice)

        if my_coins != 0.0:
            stdscr.addstr(" - ")
            stdscr.addch(currency_symbols[currency])
            stdscr.addstr(sMyValue)
           
        drawGraph(stdscr, width, height)

        stdscr.move(1,0)
        stdscr.addch(currency_symbol)
        stdscr.addstr(sHigh)

        stdscr.move(height,0)
        stdscr.addch(currency_symbol)
        stdscr.addstr(sLow)

        stdscr.refresh()

        time.sleep(1)

def getCurrencyList():
    r = requests.get('https://api.coindesk.com/v1/bpi/supported-currencies.json')

    return r.json()

if __name__ == "__main__":
    options, remainder = getopt.getopt(sys.argv[1:], 'c:hlmt:', ['currency=','help','list','mycoins=','time'])
    
    for opt, arg in options:
        if opt in ('-c', '--currency'):
            currency = arg.upper()
        
        if opt in ('-l', '--list'):
            for c in getCurrencyList():
                print(c['currency'] + ": " + c['country'])
            exit()
       
	if opt in('-t', '--time'):
	    refresh = float(arg)
 
        if opt in ('-m' '--mycoins'):
            my_coins = float(arg)

        elif opt in ('-h', '--help'):
            print('example: ticker.py -c GBP')
            print(' -l or --list to list all available currencies')
            exit()

    curses.wrapper(main)
