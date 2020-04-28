import random
import numpy as np
from utils import tools
from more_itertools import locate
from algorithm.base import Algorithm


class Genetic(Algorithm):

    def __init__(self, knapsack):
        assert isinstance(knapsack, dict)
        self.knapsack = knapsack
        self.capacity = knapsack['capacity'][0]
        self.weights  = knapsack['weights']
        self.profits  = knapsack['profits']
        self.n        = len(knapsack['weights'])
        # genetic parameters
        self.n_epoch  = knapsack['n_epoch']
        self.eps      = knapsack['eps']
        self.chaos    = knapsack['chaos']
        self.n_chrom  = knapsack['n_chrom']
        self.verbose  = False

    @property
    def name(self):
        return 'Genetic'

    @staticmethod
    def generate(self, n, n_chrom):
        population = [random.choices([0,1], k=n)
                      for i in range(n_chrom)]
        return population

    def set_verbose(self):
        self.verbose = True

    def solve(self):
        population = self.generate(self.n, self.n_chrom)
        fit_lst    = self.get_fit(population, self.knapsack)
        epoch      = 0
        test = self.test(fit_lst, self.eps, self.n)
        while((not test) and  (epoch < self.n_epoch)):
            epoch += 1
            population = self.evolve(population, fit_lst, self.chaos)
            fit_lst    = self.get_fit(population, self.knapsack)
            test       = self.test(fit_lst, self.eps, self.n)
            if self.verbose:
                print('Epoch {} evolved. Test funct {}'.format(epoch, self.converged))
        self.epochs = epoch
        return self.selection(population, fit_lst, k=1)[0]

    @staticmethod
    def generate(n, n_chrom):
        population = [random.choices([0,1], k=n)
                      for i in range(n_chrom)]
        return population

    @staticmethod
    def get_fit(population, knapsack):
        fit_lst = []
        for chrom in population:
            ttl_weight, ttl_profit = tools.compute_knapsack(knapsack, chrom)
            while ttl_weight > knapsack['capacity'][0]:
                indexes = list(locate(chrom, lambda x: x == 1))
                indexes = random.choices(indexes, k=int(len(chrom)*0.15)+1)
                for ind in indexes:
                    chrom[ind] = 0
                ttl_weight, ttl_profit = tools.compute_knapsack(knapsack, chrom)
            fit_lst.append((ttl_weight, ttl_profit))
        return fit_lst


    def test(self, fit_lst, pconverge, n):
        profits = [p[1] for p in fit_lst]
        maximum = max(profits)
        max_n   = profits.count(maximum)
        self.converged = max_n / n
        if self.converged > pconverge:
            return True
        else:
            return False

    @staticmethod
    def evolve(population, fit_lst, chaos=5):

        n_chrom = len(population)

        generation = Genetic.selection(population,fit_lst)

        while(len(generation) < n_chrom):
            chrom_x, chrom_y = Genetic.roulette(population, fit_lst)
            child = Genetic.mutate(Genetic.crossover(chrom_x, chrom_y), chaos)
            generation.append(child)
        return generation

    @staticmethod
    def roulette(population, fit_lst):

        survive_chances = [c[1] for c in fit_lst]
        pair = random.choices(population,
                              weights=survive_chances,
                              k=2)
        return pair

    @staticmethod
    def mutate(chrom, chaos):
        for i, gene in enumerate(chrom):
            rnd = random.randint(1, 100)
            if rnd < chaos:
                chrom[i] = bool(gene) ^ 1
        return chrom

    @staticmethod
    def crossover(chrom_x, chrom_y):
        locus = random.randint(0, len(chrom_x)-1)
        return chrom_x[:locus] + chrom_y[locus:]

    @staticmethod
    def selection(population, fit_lst, k=2):
        sorted_fit = sorted(fit_lst, key=lambda x: x[1])[::-1]
        strong_chroms = []
        for i in range(k):
            strongest  =  fit_lst.index(sorted_fit[i])
            strong_chroms.append(population[strongest])
        return strong_chroms
