#!/usr/bin/env python

import sys

from timewreport.parser import TimeWarriorParser

parser = TimeWarriorParser(sys.stdin)


for interval in parser.get_intervals():
    line = '"{}"'.format(interval.get_start())
    line += ',"{}"'.format(interval.get_end()) if not interval.is_open() else ''
    line += ',"{}"'.format(interval.get_duration().seconds)

    for tag in interval.get_tags():
        line += ',"{}"'.format(tag)

    print(line)
