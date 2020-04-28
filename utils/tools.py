import requests
import numpy as np
import pandas as pd
from datetime import datetime
from algorithm.base import Algorithm


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


def compute_knapsack(knapsack, optimal, verbose=False):

    ttl_weight = sum([item[0] * item[1] for item in zip(knapsack['weights'], optimal)])
    ttl_profit = sum([item[0] * item[1] for item in zip(knapsack['profits'], optimal)])

    if ttl_weight > knapsack['capacity'][0] and verbose:
        print('Total weight exceed knapsack capacity ({} > {})'.format(
               ttl_weight, knapsack['capacity'][0]))

    return ttl_weight, ttl_profit


def generate_stat(algorithms,
                  benchmarks,
                  alg_params,
                  n_observations=3,
                  **params):

    for algorithm, params in zip(algorithms, alg_params):
        test_knap = dict(benchmarks[1], **params)
        assert isinstance(algorithm(test_knap), Algorithm)

    info_dct    = {
                     'algorithm':     [],
                     'benchmark':     [],
                     'capacity':      [],
                     'preprocessing': [],
                     'execution':     [],
                     'observation':   [],
                     'optim_weight':  [],
                     'optim_profit':  [],
                   }
    for observation in range(n_observations):

        for key in benchmarks:

            knapsack = benchmarks[key]

            for algorithm, params in zip(algorithms, alg_params):

                knapsack = dict(knapsack, **params)

                start_time = datetime.now()
                alg = algorithm(knapsack)
                preprocess = datetime.now() - start_time

                start_time = datetime.now()
                optimal    = alg.solve()
                execution  = datetime.now() - start_time

                w, p = compute_knapsack(knapsack, optimal)


                info_dct['algorithm']     += [alg.name]
                info_dct['benchmark']     += [key]
                info_dct['capacity']      += [knapsack['capacity'][0]]
                info_dct['preprocessing'] += [preprocess.total_seconds()]
                info_dct['execution']     += [execution.total_seconds()]
                info_dct['observation']   += [observation]
                info_dct['optim_weight']  += [w]
                info_dct['optim_profit']  += [p]
    return pd.DataFrame.from_dict(info_dct)


def get_kdct(path, with_optimum=True):
    with open(path, 'r') as f:
        file = f.read()
        file = file.split('\n')
        # print(file[0])
        capacity = [int(file[0].split(' ')[1])]
        n        = int(file[0].split(' ')[0])
        if with_optimum:
            weights  = [int(x.split(' ')[1]) for x in file[1:-2]]
            profits  = [int(x.split(' ')[0]) for x in file[1:-2]]
            optimal  = [int(x) for x in file[-2].split(' ')]
        else:
            weights  = [int(x.split(' ')[1]) for x in file[1:]]
            profits  = [int(x.split(' ')[0]) for x in file[1:]]
            optimal  = []
        kdct = { 'capacity': capacity,
                 'n': n,
                 'weights': weights,
                 'profits': profits,
                 'optimal': optimal
               }
        return kdct
