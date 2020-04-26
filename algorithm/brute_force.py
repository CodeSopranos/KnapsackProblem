import numpy as np
from algorithm.base import Algorithm
from itertools import combinations


class BruteForce(Algorithm):

    def __init__(self, knapsack):
        assert isinstance(knapsack, dict)
        self.capacity = knapsack['capacity'][0]
        self.weights  = knapsack['weights']
        self.profits  = knapsack['profits']
        self.n        = len(knapsack['weights'])


    @property
    def name(self):
        return 'BruteForce'


    def solve(self):
        options = list(zip(np.arange(self.n),
                               self.weights,
                               self.profits))
        optim_profit = None
        optim_set    = []
        for i in range(self.n):
            for comb in combinations(options, i + 1):
                weight = sum([opt[1] for opt in comb])
                profit = sum([opt[2] for opt in comb])
                if ((optim_profit is None or optim_profit < profit) and
                   (weight <= self.capacity)):
                    optim_profit = profit
                    optim_set    = [0] * self.n
                    for opt in comb:
                        optim_set[opt[0]] = 1
        return optim_set
