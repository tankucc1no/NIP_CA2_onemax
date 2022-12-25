import random
import numpy as np


# generation function
# param: gen_num means the number of solution
def generate(gen_num):
    population_list = []
    for i in range(gen_num):
        individual = np.random.randint(2, size=CHROMOSOME_LENGTH).tolist()
        population_list.append(individual)

    return population_list


def fitness(individual):
    return sum(individual)


def population_fitness(population):
    pop_fitness = []
    for i in population:
        pop_fitness.append(fitness(i))
    return pop_fitness


# tour_size can not larger than population_length
def tournament(tour_size, population_list):
    tour_list: list = []
    for i in range(tour_size):
        rd_num = random.randint(0, len(population_list) - 1)
        tour_list.append(population_list[rd_num])

    parent = max(tour_list, key=lambda individual: fitness(individual)).copy()

    return parent


# weakest tournament
def weakest_tournament(population_list):
    pop_fitness = population_fitness(population_list)
    idx = np.argsort(pop_fitness)
    return population_list[idx[0]]


def crossover(i1, i2):
    check_point = random.randint(0, len(i1) - 1)
    new_i1 = i1[0:check_point] + i2[check_point:]
    new_i2 = i2[0:check_point] + i1[check_point:]
    return [new_i1, new_i2]


def mutate(individual, size=1, pro=1):
    new_individual = individual.copy()
    for i in range(size):
        rd_pro = np.random.rand()
        if rd_pro < pro:
            rd_mut_point = random.randint(0, len(new_individual) - 1)
            new_individual[rd_mut_point] = 1 - new_individual[rd_mut_point]
        else:
            continue
    return new_individual


def replacement(population_list, individual):
    population_list.sort(key=lambda individual: fitness(individual))
    # replace the worst individual
    if fitness(individual) > fitness(population_list[0]):
        population_list[0] = individual


# roulette wheel replacement
def roulette_wheel_replacement(population_list, individual):
    pop_fitness = population_fitness(population_list)
    chance_of_being_selected = (np.array(pop_fitness)/sum(pop_fitness)).tolist()
    select_rate = random.random()
    i = 0
    while select_rate - chance_of_being_selected[i] > 0:
        select_rate -= chance_of_being_selected[i]
        i += 1
    population_list[i] = individual


# to find out the max fitness in the population
def get_population_max_fitness(population_list):
    return max(fitness(individual) for individual in population_list)


def limited_crossover(chromosome_a, chromosome_b, cross_length=3):
    # Create children chromosomes
    chromosome_a, chromosome_b = chromosome_a.copy(), chromosome_b.copy()
    # Select random points on the chromosome and perform gene exchange according to the specified length
    stat_point = random.randint(0, len(chromosome_b) - cross_length - 1)
    # Exchange gene fragments
    chromosome_a[stat_point:stat_point + cross_length], chromosome_b[stat_point:stat_point + cross_length] = \
        chromosome_b[stat_point:stat_point + cross_length], chromosome_a[stat_point:stat_point + cross_length]
    return chromosome_a, chromosome_b


if __name__ == '__main__':

    POP_SIZE = 100
    CHROMOSOME_LENGTH = 15
    sum_record_iter = 0
    success_time = 0
    # tournament_size should be even
    tournament_size = 4
    # simulate 100 time ,calculate the probability of success
    for i in range(100):
        record_iter = 0
        while True:
            # generation
            pop_list = generate(POP_SIZE)

            # # tournament -- pick parents
            # parent_list = []
            # for i in range(tournament_size):
            #     parent_list.append(tournament(3, pop_list))

            # weakest tournament
            parent_list = []
            for i in range(tournament_size):
                parent_list.append(weakest_tournament(pop_list))

            # # crossover
            # child_list = []
            # for i in range(0, len(parent_list), 2):
            #     child_list.extend(crossover(parent_list[i], parent_list[i + 1]))

            # # limited crossover
            # child_list = []
            # for i in range(0, len(parent_list), 2):
            #     child_list.extend(limited_crossover(parent_list[i], parent_list[i + 1], 10))

            # cancel crossover
            child_list = parent_list

            # mutation
            mu_child_list = []
            for child in child_list:
                mu_child_list.append(mutate(child, size=1))

            # # replacement
            # for mu_child in mu_child_list:
            #     replacement(pop_list, mu_child)

            # roulette_wheel_replacement
            for mu_child in mu_child_list:
                roulette_wheel_replacement(pop_list, mu_child)

            # get_population_max_fitness
            max_population_fitness = get_population_max_fitness(pop_list)

            if max_population_fitness == 15:
                break
            else:
                record_iter += 1

        print(record_iter)
        sum_record_iter += record_iter
        if record_iter < 1000:
            success_time += 1

    print(f"mean:{sum_record_iter / 100},success_pro{success_time / 100}")
