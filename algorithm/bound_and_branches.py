from collections import deque
import numpy as np
from utils.simple_queue import SimpleQueue
from utils.simple_queue import Node
from algorithm.base import Algorithm


class BranchAndBound(Algorithm):

    def __init__(self, knapsack):
        assert type(knapsack) == dict

        self.weight_cost = list(zip(knapsack['weights'], knapsack['profits']))
        self.n_items = len(self.weight_cost)
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
        """Branch and bounds method for solving knapsack problem
        http://faculty.cns.uni.edu/~east/teaching/153/branch_bound/knapsack/overview_algorithm.html
        :param n_items: n_items of existing items
        :param capacity: the capacity of knapsack
        :param weight_cost: list of tuples like: [(weight, cost), (weight, cost), ...]
        :return: tuple like: (best cost, best combination list(contains 1 and 0))
        """
        priority_queue = SimpleQueue()

        #sort items in non-increasing order by benefit/cost
        ratios = [(index, item[1] / float(item[0])) for index, item in enumerate(self.weight_cost)]
        ratios = sorted(ratios, key=lambda x: x[1], reverse=True)

        best_so_far = Node(0, [], 0.0, 0.0, 0.0)
        a_node = Node(0, [], 0.0, 0.0, self.calculate_bound(best_so_far, ratios))
        priority_queue.push(a_node)

        while len(priority_queue) > 0:
            curr_node = priority_queue.pop()
            if curr_node.bound > best_so_far.cost:
                curr_node_index = ratios[curr_node.level][0]
                next_item_cost = self.weight_cost[curr_node_index][1]
                next_item_weight = self.weight_cost[curr_node_index][0]
                next_added = Node(
                    curr_node.level + 1,
                    curr_node.selected_items + [curr_node_index],
                    curr_node.cost + next_item_cost,
                    curr_node.weight + next_item_weight,
                    curr_node.bound
                )

                if next_added.weight <= self.capacity:
                    if next_added.cost > best_so_far.cost:
                        best_so_far = next_added

                    if next_added.bound > best_so_far.cost:
                        priority_queue.push(next_added)

                next_not_added = Node(curr_node.level + 1, curr_node.selected_items, curr_node.cost,
                                      curr_node.weight, curr_node.bound)
                next_not_added.bound = self.calculate_bound(next_not_added, ratios)
                if next_not_added.bound > best_so_far.cost:
                    priority_queue.push(next_not_added)

        self.picks = [0] * self.n_items
        for wc in best_so_far.selected_items:
            self.picks[wc] = 1
        return self.picks

    def calculate_bound(self, node, ratios):
        if node.weight >= self.capacity:
            return 0
        else:
            upper_bound = node.cost
            total_weight = node.weight
            current_level = node.level

            while current_level < self.n_items:
                current_index = ratios[current_level][0]

                if total_weight + self.weight_cost[current_index][0] > self.capacity:
                    cost = self.weight_cost[current_index][1]
                    weight = self.weight_cost[current_index][0]
                    upper_bound += (self.capacity - total_weight) * cost/weight
                    break

                upper_bound += self.weight_cost[current_index][1]
                total_weight += self.weight_cost[current_index][0]
                current_level += 1

            return upper_bound

    def check_inputs(self):
        # check variable type
        assert(isinstance(self.weight_cost, list))
        assert(isinstance(self.n_items, int))
        assert(isinstance(self.capacity, int))
        # check validity of value
        assert(self.n_items > 0)
        assert(self.capacity > 0)
