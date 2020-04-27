import numpy as np
from algorithm.base import Algorithm


class Greedy(Algorithm):

    def __init__(self, knapsack):
        assert isinstance(knapsack, dict)
        self.capacity = knapsack['capacity'][0]
        self.weights  = knapsack['weights']
        self.profits  = knapsack['profits']
        self.n        = len(knapsack['weights'])


    @property
    def name(self):
        return 'Greedy'


    def solve(self):

        value = [(x[0], x[2] / x[1]) for x in zip(np.arange(self.n),
                                                  self.weights,
                                                  self.profits)]
        value = sorted(value, key=lambda x: x[1], reverse=True)

        cur_weight = 0
        optim_set  = np.zeros(self.n, dtype=np.int64)

        for v in value:
            if cur_weight + self.weights[v[0]] <= self.capacity:
                optim_set[v[0]] = 1
                cur_weight += self.weights[v[0]]
            else:
                continue
        return optim_set.tolist()
