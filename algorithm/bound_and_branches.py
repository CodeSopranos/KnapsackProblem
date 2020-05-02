from collections import deque
import numpy as np
from utils.simple_queue import SimpleQueue
from utils.simple_queue import Node
from algorithm.base import Algorithm
import cplex
from ortools.linear_solver import pywraplp
from cplex import Cplex
from cplex.exceptions import CplexError
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

        self.profits = knapsack['profits']
        self.weights = knapsack['weights']
        self.n_items = len(knapsack['weights'])
        self.capacity = knapsack['capacity'][0]
        self.optimal = knapsack['optimal']
        self.picks = []
        self.check_inputs()

    @property
    def name(self):
        return 'Branch-And-Bound'

    def eval(self):
        assert len(self.picks) != 0
        return self.optimal == self.picks

    def solve(self):
        # initialize the integer programming model with the open source CBC solver
        solver = pywraplp.Solver('simple_mip_program', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

        # Declare binary variable x for each item from 1 to n
        x_dict = []
        for i in range(self.n_items):
            x_dict.append(solver.IntVar(0, 1, f'x_{i}'))
        # Add constraint on total weight of items selected cannot exceed   weight threshold
        solver.Add(solver.Sum([self.weights[i]*x_dict[i] for i in range(self.n_items)]) <= self.capacity)
        # Maximize total utility score
        solver.Maximize(solver.Sum([self.profits[i]*x_dict[i] for i in range(self.n_items)]))
        # Solve!
        status = solver.Solve()
        self.picks = [0] * self.n_items

        for i in range(self.n_items):
            self.picks[i] = x_dict[i].solution_value()
            
        # Uncomment the section below to print solution details
        # if status == pywraplp.Solver.OPTIMAL:
        #    print("OPTIMAL")
        #    print('Solution:')
        #    print('Objective value =', solver.Objective().Value())
        #    print('Problem solved in %f milliseconds' % solver.wall_time())
        #    for i in x_dict:
        #        print(f'{x_dict[i]} = {x_dict[i].solution_value()}')
        return self.picks

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
