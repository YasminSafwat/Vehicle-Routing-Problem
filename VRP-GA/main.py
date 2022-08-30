from ga import GeneticAlgorithm
from Depot import Depot
from Customer import Customer
from numpy import double


class Main:
    def __init__(self, depots, customers, v, d, c, p):
        self.vehicles_no = v
        self.depots_no = d
        self.customers_no = c
        self.population_size = p
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.depots_list = [Depot(alphabet[i], depots[i][0], depots[i][1], v) for i in range(d)]
        self.customers_list = [Customer(idx, x, y) for idx, (x, y) in enumerate(customers)]

    def run(self):
        ga = GeneticAlgorithm(self.vehicles_no, self.depots_no, self.customers_no, self.population_size, 200)
        ga.run(self.depots_list, self.customers_list)
