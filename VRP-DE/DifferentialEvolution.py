import math
from random import sample, uniform
from Utilities import Utilities


class GeneticAlgorithm:
    def __init__(self, vehicles_no, depots_no, customers_no, population_size, generation_size):
        self.vehicles_no = vehicles_no
        self.depots_no = depots_no
        self.customers_no = customers_no
        self.population_size = population_size
        self.generation_size = generation_size

    @staticmethod
    def generate_chromosome(depot):
        if len(depot.customers_list) == 0:
            return f"No assigned route for depot {depot.id} vehicles",

        single_depot_chromosome = []

        d_vehicles = depot.vehicles
        temp_customer_list = depot.customers_list.copy()
        len_temp = len(temp_customer_list)
        no_of_vehicles = len(d_vehicles)

        for vehicle in d_vehicles:
            vehicle.clear_route()

        shuffled_list = sample(temp_customer_list, k=len_temp)
        slice_q = math.ceil(len_temp / no_of_vehicles)

        i = 0
        j = 0
        while i <= len_temp and j < no_of_vehicles:
            slice2 = shuffled_list[i:i+slice_q]
            for k in slice2:
                d_vehicles[j].assigned_route.insert(-1, k)
            single_depot_chromosome.append(d_vehicles[j].assigned_route)
            i += slice_q
            j += 1

        return single_depot_chromosome

    def generate_population(self, depots_list, parents=None):
        population = [[..., ...] for _ in range(self.population_size)]
        if parents is None:
            x = self.population_size
        else:
            x = self.population_size-len(parents)
            for key, value in parents.items():
                population[key] = value

        for i in range(x):
            all_depots_chromosome = []
            for depot in depots_list:
                all_depots_chromosome.append(self.generate_chromosome(depot))
            chromosome_fitness = self.fitness_func(all_depots_chromosome)
            population[i][1] = all_depots_chromosome
            population[i][0] = chromosome_fitness

        return population

    @staticmethod
    def fitness_func(chromosome):
        d = 0
        for depot in chromosome:
            for vehicle_list in depot:
                for idx in range(len(vehicle_list)-1):
                    x2 = vehicle_list[idx+1].x_y_coordinates[0]
                    y2 = vehicle_list[idx+1].x_y_coordinates[1]
                    x1 = vehicle_list[idx].x_y_coordinates[0]
                    y1 = vehicle_list[idx].x_y_coordinates[1]
                    d += math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
        return 1/d

    def mutation(self, parents):
        final_population = [[..., ...] for _ in range(self.population_size)]
        f = 0.8
        for idx, chromosome in enumerate(parents):
            final_chosen_chromosome = []
            temp_parents = parents.copy()
            target = chromosome[1]
            temp_parents.remove(chromosome)
            p1, p2, p3 = tuple(sample(temp_parents, k=3))
            p1, p2, p3 = p1[1], p2[1], p3[1]
            arbitrary_dict = Utilities.give_arbitrary_numbers(target, p1, p2, p3)
            for depot_idx in range(self.depots_no):
                final_depot = []
                for vehicles_idx in range(self.vehicles_no):
                    p1a = arbitrary_dict.get(tuple(p1[depot_idx][vehicles_idx]))
                    p2a = arbitrary_dict.get(tuple(p2[depot_idx][vehicles_idx]))
                    p3a = arbitrary_dict.get(tuple(p3[depot_idx][vehicles_idx]))
                    targeta = arbitrary_dict.get(tuple(target[depot_idx][vehicles_idx]))
                    mutant_vector = p3a + f * (p1a - p2a)
                    survivor = self.crossover(targeta, mutant_vector)
                    if survivor in arbitrary_dict.values():
                        for key, value in arbitrary_dict.items():
                            if value == survivor:
                                final_depot.append(list(key))
                                break
                    else:
                        target_route = target[depot_idx][vehicles_idx]
                        len_target_route = len(target_route)
                        survivor_depot = target_route[0]
                        survivor_route = [survivor_depot]
                        survivor_route.extend(sample(target_route[1:len_target_route-1], k = len_target_route-2))
                        survivor_route.append(survivor_depot)
                        final_depot.append(list(self.DE_selection(survivor_route, target_route)))

                final_chosen_chromosome.append(final_depot)
            final_population[idx][0] = self.fitness_func(final_chosen_chromosome)
            final_population[idx][1] = final_chosen_chromosome
        return final_population

    @staticmethod
    def crossover(target, mutant):
        CR = 0.9
        if round(uniform(0.0, 1.0), 1) > CR:
            survivor = target
        else:
            survivor = mutant
        return survivor

    @staticmethod
    def DE_selection(survivor, targeta):
        fitnesses = []
        lst = [survivor, targeta]
        for idx, item in enumerate(lst):
            d = 0
            for i in range(len(item) - 1):
                x2 = item[idx + 1].x_y_coordinates[0]
                y2 = item[idx + 1].x_y_coordinates[1]
                x1 = item[idx].x_y_coordinates[0]
                y1 = item[idx].x_y_coordinates[1]
                d += math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
            fitnesses.append(1/d)
        if fitnesses[0] <= fitnesses[1]:
            final_survivor = survivor
        else:
            final_survivor = targeta
        return final_survivor

    def run(self, depots_list, customers_list):
        Utilities.grouping_depots_customers(depots_list, customers_list)
        population = self.generate_population(depots_list)
        Utilities.printing_func(population)
        old_max = None
        counter_to_stop = 0
        for i in range(1, self.generation_size):
            population = self.mutation(population)
            max_fitness = max([population[idx][0] for idx in range(self.population_size)])
            if max_fitness == old_max:
                counter_to_stop += 1
                if counter_to_stop == 20:
                    break
            else:
                counter_to_stop = 0
            old_max = max_fitness
            print(f"Generation: {i+1:4}\t-\t Highest Fitness: {max_fitness:5}")
