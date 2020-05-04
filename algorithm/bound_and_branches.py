from collections import deque
import numpy as np
from datetime import datetime
from datetime import timedelta
from utils.simple_queue import SimpleQueue
from utils.simple_queue import Node
from algorithm.base import Algorithm
from ortools.linear_solver import pywraplp
import sys, os

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


class BranchAndBound(Algorithm):

    def __init__(self, knapsack):
        assert type(knapsack) == dict
        self.start_time = 0
        self.profits = knapsack['profits']
        self.weights = knapsack['weights']
        self.n_items = len(knapsack['weights'])
        self.bounds = [[0, 1]] * self.n_items
        self.capacity = knapsack['capacity'][0]
        self.optimal = knapsack['optimal']
        self.low_bound, self.fixed_weight, self.ans = 0, 0, 0
        self.picks = []
        self.check_inputs()

    @property
    def name(self):
        return 'Branch-And-Bound'

    def eval(self):
        assert len(self.picks) != 0
        return self.optimal == self.picks

    def solve(self):
        self.start_time = datetime.now()
        _, self.picks = self.branch_and_bound()
        if (_ == -1 and self.picks == -1):
            return -1
        return list(self.picks)
            

    def branch_and_bound(self):

        solver = pywraplp.Solver('simple_mip_program', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
        x_dict = np.array([solver.IntVar(self.bounds[i][0], self.bounds[i][1], f'x_{i}') for i in range(self.n_items)])
        solver.Add(solver.Sum([self.weights[i]*x_dict[i] for i in range(self.n_items)]) <= self.capacity)
        solver.Maximize(solver.Sum([self.profits[i]*x_dict[i] for i in range(self.n_items)]))
        status = solver.Solve()
        profit = solver.Objective().Value()
        
        end_time = datetime.now() - self.start_time
        if (end_time > timedelta(seconds=228)):
            return -1, -1
        
        if profit <= self.low_bound:
            return 0, 0
        
        X = np.array([x_d.solution_value() for x_d in x_dict])

        try:
            idx = np.where(X != X.round())[0][0]
        except IndexError:
            idx = -1
        
        if (idx != -1):
            self.bounds[idx] = [0, 0]
            new_profit, new_X = self.branch_and_bound()
            if (new_profit): 
                self.low_bound, self.ans = new_profit, new_X

            self.bounds[idx] = [1, 1]
            self.fixed_weight += self.weights[idx]
            if self.fixed_weight <= self.capacity:
                new_profit, new_X = self.branch_and_bound()
                if (new_profit): 
                    self.low_bound, self.ans = new_profit, new_X 

            self.bounds[idx] = [0, 1]
            self.fixed_weight -= self.weights[idx]
        else:
            self.low_bound = profit
            self.ans = X

        return self.low_bound, self.ans
        
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
