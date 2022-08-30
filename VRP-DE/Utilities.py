import math
from numpy import double


class Utilities:
    @staticmethod
    def grouping_depots_customers(depots, customers):
        for customer in customers:
            x2 = customer.x_y_coordinates[0]
            y2 = customer.x_y_coordinates[1]
            nearest_depot_distance = None
            wanted_depot = None
            for depot in depots:
                x1 = depot.x_y_coordinates[0]
                y1 = depot.x_y_coordinates[1]
                d = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
                if nearest_depot_distance is None or d < nearest_depot_distance:
                    nearest_depot_distance = d
                    wanted_depot = depot
            wanted_depot.assign_customers(customer)

    @staticmethod
    def printing_func(population):
        temp_lst = \
            [[chromosome[0], [[[dest.printing() for dest in vehicle] for vehicle in depot] for depot in chromosome[1]]]
             for chromosome in population]

        for idx in range(len(temp_lst)):
            print(f"Chromosome {idx+1}:")
            print()
            print(f"\tFitness: {population[idx][0]}")
            print(f"\tRoutes: ")

            j = 1
            for depot in temp_lst[idx][1]:
                for route in depot:
                    print(f"\t  Vehicle {j:<2} is assigned to: ",route)
                    j += 1

            x = "===================================================================================================="
            print()
            print(f"{x:^150}")
            print()

    @staticmethod
    def give_arbitrary_numbers(target, p1, p2, p3):
        lst = [target, p1, p2, p3]
        taken = []
        arbitrary_dict = dict()
        for p in lst:
            for depot in p:
                for route in depot:
                    d = 0
                    for idx in range(len(route)-1):
                        x2 = route[idx+1].x_y_coordinates[0]
                        y2 = route[idx+1].x_y_coordinates[1]
                        x1 = route[idx].x_y_coordinates[0]
                        y1 = route[idx].x_y_coordinates[1]
                        d += math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
                    while d in taken:
                        d += 1

                    arbitrary_dict[tuple(route)] = d
                    taken.append(d)
        return arbitrary_dict
