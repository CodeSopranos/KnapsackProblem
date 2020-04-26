import requests
import numpy as np
import pandas as pd


def get_knapsack(n='01') -> dict:

    bas_url = 'https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/p'

    c  = requests.get(bas_url+n+'_c.txt')
    w  = requests.get(bas_url+n+'_w.txt')
    p  = requests.get(bas_url+n+'_p.txt')
    s  = requests.get(bas_url+n+'_s.txt')

    kdct = {'capacity': c.text,
            'weights':  w.text,
            'profits':  p.text,
            'optimal':  s.text}
    kdct = {k: v.split('\n') for k, v in kdct.items()}
    kdct = {k: [int(x) for x in v if len(x)>0] for k, v in kdct.items()}
    print(n, 'is loaded!')
    
    return kdct


def get_profit(knapsack, optimal):

    ttl_weight = sum([item[0] * item[1] for item in zip(knapsack['weights'], optimal)])
    ttl_profit = sum([item[0] * item[1] for item in zip(knapsack['profits'], optimal)])

    if ttl_weight > knapsack['capacity'][0]:
        print('Total weight exceed knapsack capacity ({} > {})'.format(
               ttl_weight, knapsack['capacity'][0]))

    return ttl_profit
