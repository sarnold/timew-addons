#!/usr/bin/env python3

import os
import sys
from datetime import timedelta
from typing import Dict

from timewreport.parser import TimeWarriorParser

# indicator format is extremely terse
CSV_OUTPUT = os.getenv('INDICATOR_FMT')

parser = TimeWarriorParser(sys.stdin)
totals: Dict[str, timedelta] = dict()


def strf_delta(td):
    '''
    String format a timedelta => (HH:MM:SS)
    '''
    h, r = divmod(int(td.total_seconds()), 60 * 60)
    m, s = divmod(r, 60)
    h, m, s = (str(x).zfill(2) for x in (h, m, s))
    return f"{h}:{m}:{s}"


for interval in parser.get_intervals():
    tracked = interval.get_duration()

    for tag in interval.get_tags():
        if tag in totals:
            totals[tag] += tracked
        else:
            totals[tag] = tracked

# Determine largest tag width.
max_width = len('Total')

for tag in totals:
    if len(tag) > max_width:
        max_width = len(tag)

if not CSV_OUTPUT:
    # Compose report header.
    print('Total by Tag')
    print('')

    # Compose table header.
    print('{:{width}} {:>10}'.format('Tag', 'Total', width=max_width))
    print('{} {}'.format('-' * max_width, '----------'))

# Compose table rows.
total_seconds = 0
td_total = timedelta(0)

for tag in sorted(totals):
    formatted = totals[tag].seconds
    total_seconds += totals[tag].seconds
    td_total += totals[tag]
    if not CSV_OUTPUT:
        print('{:{width}} {:10}'.format(tag, formatted, width=max_width))

if not CSV_OUTPUT:
    # Compose total.
    print('{} {}'.format(' ' * max_width, '----------'))
    print('{:{width}} {:10}'.format('Total', total_seconds, width=max_width))
else:
    # preserve this output format for timew-status-indicator, total in HH:MM::SS
    print(f'total;{strf_delta(td_total)}')
