from collections import deque
import numpy as np
from utils.simple_queue import SimpleQueue
from utils.simple_queue import Node
from algorithm.base import Algorithm
import cplex
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
        xvar = [ 'x'+str(j) for j in range(1,self.n_items+1) ]
        types = 'B'*self.n_items
        ub = [1]*self.n_items
        lb = [0]*self.n_items

        try:
            with HiddenPrints():
                prob = cplex.Cplex()
                prob.objective.set_sense(prob.objective.sense.maximize)
                prob.variables.add(obj = self.profits, lb = lb, ub = ub, types = types, names = xvar )

                rows = [[ xvar, self.weights], [ xvar, [1]*self.n_items],]
                
                prob.linear_constraints.add(lin_expr = rows, senses = 'LL', rhs = [self.capacity, self.capacity,], names = ['r1','r2',] )
                prob.solve()

            # print("Solution value  = ", prob.solution.get_objective_value())
            xsol = prob.solution.get_values()
            self.picks = xsol
            return self.picks
        except CplexError as exc:
            print(exc)
            return -1

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
