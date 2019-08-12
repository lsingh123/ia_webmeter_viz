#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 11:04:58 2019

@author: lavanyasingh
"""

def make_data(vals, x_key, y_key): 
    """ formats data into a dictionary with given keys """
    data_x = list(vals.keys())
    data_y = list(vals.values())
    data_human = [human_number(num) for num in data_y]
    data = {x_key: data_x, y_key: data_y, (y_key + "_human"):data_human}
    return data

# taken from Steve Sisney's crawlstat
def human_number(num, binary_size=False, suffix=''):
    '''
    returns a human readable number
    '''
    units = ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']
    boundary = 1000.0

    if binary_size:
        units = ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']
        boundary = 1024.0

    for unit in units:
        if abs(num) < boundary:
            return "%.0f%s%s" % (num, unit, suffix)
        num /= boundary

    return "%.1f%s%s" % (num, 'Yi', suffix)    