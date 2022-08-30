import math
from random import sample
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
            return [[depot, depot]] * len(depot.vehicles)

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
        diff = no_of_vehicles - len(single_depot_chromosome)
        if diff > 0:
            while diff != 0:
                single_depot_chromosome.append([depot, depot])
                diff -= 1
        return single_depot_chromosome

    def generate_population(self, depots_list, offsprings=None):
        population = [[..., ...] for _ in range(self.population_size)]
        if offsprings is None:
            x = self.population_size
        else:
            x = self.population_size-len(offsprings)
            for idx, (key, value) in enumerate(offsprings):
                population[idx][0] = key
                population[idx][1] = value

        for i in range(self.population_size - 1, self.population_size - 1 - x, -1):
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
                len_v = len(vehicle_list)
                if len_v == 2:
                    continue
                for idx in range(len_v-1):
                    x2 = vehicle_list[idx+1].x_y_coordinates[0]
                    y2 = vehicle_list[idx+1].x_y_coordinates[1]
                    x1 = vehicle_list[idx].x_y_coordinates[0]
                    y1 = vehicle_list[idx].x_y_coordinates[1]
                    d += math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
        if d == 0:
            d = 0.000000000000000001
        return 1/d

    def selection(self, population):
        k_rand = 3
        best = 2
        iterations = self.population_size//best

        parents = []
        for i in range(iterations-1):
            rand_lst = sample(population, k=k_rand)
            slice = []
            for idx in range(k_rand-1):
                if rand_lst[idx][0] == rand_lst[idx+1][0]:
                    continue
                slice.extend(sorted([rand_lst[idx], rand_lst[idx+1]]))
            slice = slice[:best]
            for fitness in slice:
                for lst in rand_lst:
                    if lst[0] == fitness[0]:
                        parents.append([fitness[0], fitness[1]])
                        break
        return self.crossover(parents)

    def crossover(self, parents):
        len_p = len(parents)
        final_population = [[..., ...] for _ in range(len_p)]
        for idx_ch in range(0, len_p, 2):
            final_chosen_chromosome_1 = []
            final_chosen_chromosome_2 = []
            for idx_d in range(self.depots_no):
                final_depot_1 = []
                final_depot_2 = []
                for idx_v in range(self.vehicles_no):
                    # filter parents from depots
                    """print(idx_ch)
                    print(idx_d)
                    print(idx_v)"""
                    parent1 = parents[0][1][0][0][1:-1]
                    parent2 = parents[idx_ch + 1][1][idx_d][idx_v][1:-1]
                    len_p2 = len(parent2)
                    len_p1 = len(parent1)

                    # each offspring will have the length of the opposing parent
                    offspring1 = [0 for _ in range(len_p2)]
                    offspring2 = [0 for _ in range(len_p1)]

                    # determine starting index due to shorter parent
                    if len_p2 < len_p1:
                        slice2 = len_p2//3
                    else:
                        slice2 = len_p1//3

                    offspring1[slice2: slice2*2] = parent1[slice2: slice2*2]
                    offspring2[slice2: slice2*2] = parent2[slice2: slice2*2]

                    for idx in range(len_p1):
                        if slice2 <= idx < slice2*2:
                            continue
                        offspring2[idx] = parent1[idx]

                    for idx in range(len_p2):
                        if slice2 <= idx < slice2 * 2:
                            continue
                        offspring1[idx] = parent2[idx]

                    offspring1.insert(0, parents[idx_ch][1][idx_d][idx_v][0])
                    offspring1.append(parents[idx_ch][1][idx_d][idx_v][0])
                    offspring2.insert(0, parents[idx_ch][1][idx_d][idx_v][0])
                    offspring2.append(parents[idx_ch][1][idx_d][idx_v][0])

                    final_depot_1.append(offspring1)
                    final_depot_2.append(offspring2)
                final_chosen_chromosome_1.append(final_depot_1)
                final_chosen_chromosome_2.append(final_depot_2)
            final_population[idx_ch][0] = self.fitness_func(final_chosen_chromosome_1)
            final_population[idx_ch][1] = final_chosen_chromosome_1
            final_population[idx_ch+1][0] = self.fitness_func(final_chosen_chromosome_2)
            final_population[idx_ch+1][1] = final_chosen_chromosome_2

        return self.mutation(final_population)

    @staticmethod
    def mutation(population):
        for idx, (_, chromosome) in enumerate(population):
            for depot in chromosome:
                for route in depot:
                    slice2 = len(route)//3
                    route[slice2: slice2*2] = route[slice2*2: slice2: -1]

        return population

    def run(self, depots_list, customers_list):
        Utilities.grouping_depots_customers(depots_list, customers_list)
        population = self.generate_population(depots_list)
        Utilities.printing_func(population)
        offsprings = self.selection(population)
        old_max = None
        counter_to_stop = 0
        for i in range(1, self.generation_size):
            population = self.generate_population(depots_list, offsprings)
            offsprings = self.selection(population)
            max_fitness = max([population[idx][0] for idx in range(self.population_size)])
            if max_fitness == old_max:
                counter_to_stop += 1
                if counter_to_stop == 20:
                    break
            else:
                counter_to_stop = 0
            old_max = max_fitness
            print(f"Generation: {i + 1:4}\t-\t Highest Fitness: {max_fitness:5}")
