#! /usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict
import json
import urllib2
import webbrowser

import rumps

__appname__     = 'C1t1'
__author__      = 'Lucy Park'
__description__ = 'Retrieves cryptocurrency prices from Coineone.co.kr every one minute and displays them on the MacOSX menubar.'
__repository__  = 'http://github.com/e9t/c1t1'
__version__     = '0.1.0'
__year__        = '2017'


TICK_INTERVAL = 60  # interval to retrieve ticks (seconds)
COINS = OrderedDict([
    ('btc', {'icon': u'\u20BF'}),
    ('eth', {'icon': u'\u039E'}),
    ('etc', {'icon': u'\uA792'}),
    ('xrp', {'icon': u'X'}),
])
COINEX_URL = 'https://coinone.co.kr/exchange'
PRICES_API = 'https://api.coinone.co.kr/ticker/?format=json&currency'

coinex = 'Go to Coinone'
about = 'About %s v%s' % (__appname__, __version__)


class App(rumps.App):
    def __init__(self):
        super(App, self).__init__(__appname__)
        self.coin_menus = OrderedDict()
        for coin in COINS:
            self.coin_menus[coin] = rumps.MenuItem(coin)
        self.coin_menus['btc'].state = 1  # turn on bitcoin
        self.menu = self.coin_menus.values() + [coinex, about]
        self.update_prices()
        self.update_title()

    def update_prices(self):
        self.prices = json.loads(urllib2.urlopen(PRICES_API).read())

    def update_title(self):
        title = []
        for coin in COINS:
            if self.coin_menus[coin].state == 1:
                i = COINS[coin]['icon']
                p = '{:0,.0f}'.format(int(self.prices[coin]['last']))
                title.extend([i, p])
        self.title = ' '.join(title)

    @rumps.timer(TICK_INTERVAL)
    def update_all(self, sender):
        self.update_prices()
        self.update_title()

    @rumps.clicked('btc')
    def toggle_btc(self, sender):
        sender.state = not sender.state
        self.update_title()

    @rumps.clicked('eth')
    def toggle_eth(self, sender):
        sender.state = not sender.state
        self.update_title()

    @rumps.clicked('etc')
    def toggle_etc(self, sender):
        sender.state = not sender.state
        self.update_title()

    @rumps.clicked('xrp')
    def toggle_xrp(self, sender):
        sender.state = not sender.state
        self.update_title()

    @rumps.clicked(coinex)
    def goto_coinex(self, sender):
        webbrowser.open(COINEX_URL)

    @rumps.clicked(about)
    def show_about(self, sender):
        title = about
        message = '\n'.join([
            __description__,
            '',
            'Made by %s (%s).' % (__author__, __year__),
            __repository__,
        ])
        rumps.alert(title=title, message=message, ok=None, cancel=None)


if __name__ == '__main__':
    App().run()
