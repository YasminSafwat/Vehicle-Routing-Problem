from Depot import Depot
from Customer import Customer
from DifferentialEvolution import GeneticAlgorithm
from numpy import double

vehicles_no = ...
depots_no = ...
customers_no = ...
population_size = 10

if __name__ == "__main__":
    df = open('pr10.txt', 'r')
    data = df.readline().split()
    vehicles_no = int(data[0])
    customers_no = int(data[1])
    depots_no = int(data[2])

    customers_list = []
    for j in range(customers_no):
        info = df.readline().split()
        i = int(info[0])
        x = double(info[1])
        y = double(info[2])
        customers_list.append(Customer(i, x, y))

    depots_list = []
    for i in range(depots_no):
        info = df.readline().split()
        k = info[0]
        x = double(info[1])
        y = double(info[2])
        depots_list.append(Depot(k, x, y, vehicles_no))

    ga = GeneticAlgorithm(vehicles_no, depots_no, customers_no, population_size, 200)
    ga.run(depots_list, customers_list)
