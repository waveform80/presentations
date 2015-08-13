#!/usr/bin/env python

from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )
str = type('')

import io
import os
import time
import datetime as dt
import locale
from collections import namedtuple, deque
from pprint import pprint

import pg8000
from chameleon import PageTemplate


class html(str):
    def __html__(self):
        return str(self)


locale.setlocale(locale.LC_ALL, '')

Stock = namedtuple('Stock', ('symbol', 'name', 'price', 'change', 'volume'))

pg8000.paramstyle = 'qmark'
conn = pg8000.connect(database='stocks', unix_sock='/var/run/postgresql/.s.PGSQL.5432')

with io.open('template.html', 'rb') as f:
    template = PageTemplate(f.read().decode('utf-8'))


def market_states():
    current_date = None
    state = {}
    cur = conn.cursor()
    cur.arraysize = 1000
    cur.execute("""
        SELECT date, symbol, name, adj_close, volume
        FROM market_view
        ORDER BY date, symbol
        """)
    while True:
        row = cur.fetchone()
        if row is None:
            break
        date, symbol, name, close, volume = row
        if date != current_date:
            if state:
                yield current_date, state
            current_date = date
        state[symbol] = Stock(symbol, name, close, None, volume)
    yield date, state


def back_fill(states):
    blank_stock = Stock(None, None, None, 0.0, 0)
    old_state = {}
    for date, new_state in states:
        filled_state = {
            symbol: Stock(
                s.symbol,
                s.name,
                old_price if s.price is None else s.price,
                (
                    s.price - old_price if s.price is not None and old_price is not None else
                    0.0 if s.price is None and old_price is not None else
                    None
                    ),
                s.volume or 0)
            for symbol, s in new_state.items()
            for old_price in (old_state.get(symbol, blank_stock).price,)
            }
        yield date, filled_state
        old_state = filled_state


def filter_blank(states):
    for date, state in states:
        if not all(s.price is None for s in state.values()):
            yield date, {
                    symbol: stock for symbol, stock in state.items()
                    if stock.price is not None
                    }


def main():
    for date, state in filter_blank(back_fill(market_states())):
        print('Writing state for {date:%Y-%m-%d}'.format(date=date))
        with io.open('market.html.new', 'wb') as f:
            f.write(template(
                date=date,
                state=state,
                sign=lambda n: (1 if n > 0 else -1) if n else 0,
                locale=locale).encode('utf-8'))
        os.rename('market.html.new', 'market.html')
        time.sleep(2)


if __name__ == '__main__':
    main()
