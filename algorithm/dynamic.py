
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
        K = [[0 for x in range(self.capacity + 1)] for x in range(self.n_items + 1)]

        for i in range(self.n_items + 1):
            for w in range(self.capacity + 1):
                if i == 0 or w == 0:
                    K[i][w] = 0
                elif self.weights[i - 1] <= w:
                    K[i][w] = max(self.profits[i - 1] + K[i - 1][w - self.weights[i - 1]], K[i - 1][w])
                else:
                    K[i][w] = K[i - 1][w]

        items_set = []
        self.find_items_set(K, self.n_items, self.capacity, self.weights, items_set)
        self.picks = [0] * self.n_items
        for x in items_set:
            self.picks[x] = 1
        return self.picks

    def find_items_set(self, K, i, w, weights, items_set):
        if K[i][w] == 0:
            return

        if K[i - 1][w] == K[i][w]:
            self.find_items_set(K, i - 1, w, weights, items_set)
        else:
            self.find_items_set(K, i - 1, w - weights[i - 1], weights, items_set)
            items_set.append(i - 1)

        return items_set
    
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
