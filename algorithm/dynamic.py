
import numpy as np
from algorithm.base import Algorithm


class Dynamic(Algorithm):

    def __init__(self, knapsack):
        assert type(knapsack) == dict

        self.profits = knapsack['profits']
        self.weights = knapsack['weights']
        self.n_items = len(knapsack['weights'])
        self.capacity = knapsack['capacity'][0]
        self.optimal = knapsack['optimal']
        self.picks = []
        self.check_inputs()

    @property
    def name(self):
        return 'Dynamic'


    def solve(self):
        table = np.zeros((self.n_items + 1, self.capacity + 1), dtype = np.float32)
        keep = np.zeros((self.n_items + 1, self.capacity + 1), dtype = np.float32)

        for i in range(1, self.n_items + 1):
            for w in range(0, self.capacity + 1):
                wi = self.weights[i - 1] # weight of current item
                vi = self.profits[i - 1] # value of current item
                if (wi <= w) and (vi + table[i - 1, w - wi] > table[i - 1, w]):
                    table[i, w] = vi + table[i - 1, w - wi]
                    keep[i, w] = 1
                else:
                    table[i, w] = table[i - 1, w]

        idx = []
        K = self.capacity

        for i in range(self.n_items, 0, -1):
            if keep[i, K] == 1:
                idx.append(i)
                K -= self.weights[i - 1]

        idx.sort()
        idx = [x - 1 for x in idx] # change to 0-index

        self.picks = [0] * self.n_items
        for wc in idx:
            self.picks[wc] = 1
        return self.picks

    def eval(self):
        assert len(self.picks) != 0
        return self.optimal == self.picks

    def check_inputs(self):
        # check variable type
        assert(isinstance(self.profits, list))
        assert(isinstance(self.weights, list))
        assert(isinstance(self.n_items, int))
        assert(isinstance(self.capacity, int))
        # check value type
        assert(all(isinstance(val, int) or isinstance(val, float) for val in self.profits))
        assert(all(isinstance(val, int) for val in self.weights))
        # check validity of value
        assert(all(val >= 0 for val in self.weights))
        assert(self.n_items > 0)
        assert(self.capacity > 0)
