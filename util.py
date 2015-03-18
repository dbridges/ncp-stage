#!/usr/bin/env python3

import datetime


def timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

def limit(val, min_val, max_val):
    if val < min_val:
        return min_val
    elif val > max_val:
        return max_val
    return val
