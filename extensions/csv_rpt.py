#!/usr/bin/env python3

import sys

from timewreport.parser import TimeWarriorParser

SEP = ';'
parser = TimeWarriorParser(sys.stdin)


for interval in parser.get_intervals():
    line = '"{}"'.format(interval.get_start())
    line += '{}"{}"'.format(SEP, interval.get_end()) if not interval.is_open() else ''
    line += '{}"{}"'.format(SEP, interval.get_duration().seconds)

    for tag in interval.get_tags():
        line += '{}"{}"'.format(SEP, tag)

    print(line)
