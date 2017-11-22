## ticker.py

A Bitcoin price ticker for the command line. Intended to be run inside a tmux pane.

Default is GBP. Use any currency supported by the coindesk api.

Updates every 60 seconds and plots a simple graph as it goes. You can resize the display while it's running but note that it will wait until the next price refresh before redrawing.

usage:

`python ticker.py -c USD`  

`-l` or `--list` to list all available currencies.  

`-m [number]` or `--mycoins=[number]` to display the value of your coins.
