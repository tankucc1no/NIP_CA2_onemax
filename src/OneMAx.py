import random
import numpy as np

CHROMOSOME_LENGTH = 15
# for inside EA
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


def limited_crossover(chromosome_a, chromosome_b, cross_length=3):
    # Create children chromosomes
    chromosome_a, chromosome_b = chromosome_a.copy(), chromosome_b.copy()
    # Select random points on the chromosome and perform gene exchange according to the specified length
    stat_point = random.randint(0, len(chromosome_b) - cross_length - 1)
    # Exchange gene fragments
    chromosome_a[stat_point:stat_point + cross_length], chromosome_b[stat_point:stat_point + cross_length] = \
        chromosome_b[stat_point:stat_point + cross_length], chromosome_a[stat_point:stat_point + cross_length]
    return chromosome_a, chromosome_b


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
# def roulette_wheel_replacement(individual):
#     pop_fitness = population_fitness(pop_list)
#     chance_of_being_selected = (np.array(pop_fitness)/sum(pop_fitness)).tolist()
#     select_rate = random.random()
#     i = 0
#     while select_rate - chance_of_being_selected[i] > 0:
#         select_rate -= chance_of_being_selected[i]
#         i += 1
#     if fitness(individual) > fitness(pop_list[i]):
#         pop_list[i] = individual


# to find out the max fitness in the population
def get_population_max_fitness(population_list):
    return max(fitness(individual) for individual in population_list)


# for outside EA

def generate_parameters():
    tournament_size = []
    population = []
    CROSSOVER_LENGTHS = []
    MUTATION_SIZES = []
    for i in range(50):
        p = random.sample([50, 100, 200, 500], 1)[0]
        population.append(p)
        if p == 50:
            tournament_size.append(random.sample([10, 20], 1)[0])
        elif p == 100:
            tournament_size.append(random.sample([15, 50], 1)[0])
        else:
            tournament_size.append(random.sample([15, 50, 100], 1)[0])
        CROSSOVER_LENGTHS.append(random.sample(range(15), 1)[0])
        MUTATION_SIZES.append(random.sample(range(15), 1)[0])
    parameters = []
    for i in range(50):
        parameters.append([CROSSOVER_LENGTHS[i], MUTATION_SIZES[i], tournament_size[i], population[i]])
    return parameters


def parameters_tournament(parameters, mean, size=5):
    idx = random.sample(range(50), size)
    l = []
    for i in idx:
        l.append(mean[i])
    lst = np.array(l).argsort()[:2]
    idx1 = idx[lst[0]]
    idx2 = idx[lst[1]]
    return parameters[idx1].copy(), parameters[idx2].copy()


def parameters_crossover_index(parameter1, parameter2):
    point = random.randint(0, 3)
    parameter1[point:point + 1], parameter2[point:point + 1] = parameter2[point:point + 1], parameter1[point:point + 1]
    return parameter1, parameter2


def weakest_replacement(parameter, record_iter, parameters, mean, success_time):
    if record_iter > 1000 or success_time < 95:
        return parameters, mean
    else:
        min_idx = np.array(mean).argsort()[0]
        if record_iter > mean[min_idx]:
            mean[min_idx] = record_iter
            parameters[min_idx] = parameter
        return parameters, mean


def EA_in_EA():

    result = []  # Used to count results
    max_mean = []
    success_rate = []
    parameters = generate_parameters()
    # mean loops is used as fitness of combination of parameters.
    # Initialize fitness to 1 for all combinations of parameters.
    mean = [1] * 50

    # Outside EA
    for i in range(500):
        print(i)
        parameter1, parameter2 = parameters_tournament(parameters, mean)
        parameter1, parameter2 = parameters_crossover_index(parameter1, parameter2)
        CHROMOSOME_LENGTH = 15

        # generate parameters
        tournament_size = parameter1[2]
        CROSSOVER_LENGTH = parameter1[0]
        MUTATION_SIZE = parameter1[1]
        POP_SIZE = parameter1[3]

        # these two parameters will be used in inside EA to compute the success rate and mean of loops
        sum_record_iter = 0
        success_time = 0

        # inside EA
        # simulate 100 time ,calculate the probability of success
        for i in range(100):
            record_iter = 0

            # generation
            pop_list = generate(POP_SIZE)
            while True:

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

                # limited crossover
                child_list = []
                for i in range(0, len(parent_list)-1, 2):
                    child_list.extend(limited_crossover(parent_list[i], parent_list[i + 1], CROSSOVER_LENGTH))

                # # cancel crossover
                # child_list = parent_list

                # mutation
                mu_child_list = []
                for child in child_list:
                    mu_child_list.append(mutate(child, size=MUTATION_SIZE))

                # replacement
                for mu_child in mu_child_list:
                    replacement(pop_list, mu_child)

                # # roulette_wheel_replacement
                # for mu_child in mu_child_list:
                #     roulette_wheel_replacement(mu_child)

                # get_population_max_fitness
                max_population_fitness = get_population_max_fitness(pop_list)
                # print(max_population_fitness)

                if max_population_fitness == 15:
                    break
                else:
                    record_iter += 1
                if record_iter > 1500:
                    break


            # print(record_iter)
            sum_record_iter += record_iter
            if record_iter < 1000:
                success_time += 1

        weakest_replacement(parameter1, sum_record_iter/100, parameters, mean, success_time)
        # print(mean[np.array(mean).argsort()[-1]])
        # print(parameters[np.array(mean).argsort()[-1]])

        print(mean)
        print(parameters)
        max_mean.append(max(mean))

        # print(f"mean:{sum_record_iter / 100},success_pro{success_time / 100}")
        result.append([POP_SIZE, mean, parameters, max_mean])
        return result

def result_test(tournament_size = 24, CROSSOVER_LENGTH = 2, MUTATION_SIZE = 2, POP_SIZE = 500):
    times = []
    # generate parameters
    tournament_size = 24
    CROSSOVER_LENGTH = 2
    MUTATION_SIZE = 2
    POP_SIZE = 500
    CHROMOSOME_LENGTH = 15
    # these two parameters will be used in inside EA to compute the success rate and mean of loops
    sum_record_iter = 0
    success_time = 0

    # inside EA
    # simulate 100 time ,calculate the probability of success
    for i in range(100):
        record_iter = 0

        # generation
        pop_list = generate(POP_SIZE)
        while True:

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

            # limited crossover
            child_list = []
            for i in range(0, len(parent_list)-1, 2):
                child_list.extend(limited_crossover(parent_list[i], parent_list[i + 1], CROSSOVER_LENGTH))

            # # cancel crossover
            # child_list = parent_list

            # mutation
            mu_child_list = []
            for child in child_list:
                mu_child_list.append(mutate(child, size=MUTATION_SIZE))

            # replacement
            for mu_child in mu_child_list:
                replacement(pop_list, mu_child)

            # # roulette_wheel_replacement
            # for mu_child in mu_child_list:
            #     roulette_wheel_replacement(mu_child)

            # get_population_max_fitness
            max_population_fitness = get_population_max_fitness(pop_list)
            # print(max_population_fitness)

            if max_population_fitness == 15:
                break
            else:
                record_iter += 1
            if record_iter > 1500:
                break

        times.append(record_iter)
        print(record_iter)
        sum_record_iter += record_iter
        if record_iter < 1000:
            success_time += 1
    print(f"mean:{sum_record_iter / 100},success_pro{success_time / 100}")
    return times


def small_scale():
    result = []
    # generate parameters
    for tournament_size in range(20, 26):
        for CROSSOVER_LENGTH in range(2, 3, 1):
            for MUTATION_SIZE in range(1, 7, 1):
                POP_SIZE = 500
                CHROMOSOME_LENGTH = 15
                # these two parameters will be used in inside EA to compute the success rate and mean of loops
                sum_record_iter = 0
                success_time = 0

                # inside EA
                # simulate 100 time ,calculate the probability of success
                for i in range(100):
                    record_iter = 0

                    # generation
                    pop_list = generate(POP_SIZE)
                    while True:

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

                        # limited crossover
                        child_list = []
                        for i in range(0, len(parent_list)-1, 2):
                            child_list.extend(limited_crossover(parent_list[i], parent_list[i + 1], CROSSOVER_LENGTH))

                        # # cancel crossover
                        # child_list = parent_list

                        # mutation
                        mu_child_list = []
                        for child in child_list:
                            mu_child_list.append(mutate(child, size=MUTATION_SIZE))

                        # replacement
                        for mu_child in mu_child_list:
                            replacement(pop_list, mu_child)

                        # # roulette_wheel_replacement
                        # for mu_child in mu_child_list:
                        #     roulette_wheel_replacement(mu_child)

                        # get_population_max_fitness
                        max_population_fitness = get_population_max_fitness(pop_list)
                        # print(max_population_fitness)

                        if max_population_fitness == 15:
                            break
                        else:
                            record_iter += 1
                        if record_iter > 1500:
                            break

                    print(record_iter)
                    sum_record_iter += record_iter
                    if record_iter < 1000:
                        success_time += 1
                if success_time >= 95:
                    result.append([tournament_size, CROSSOVER_LENGTH, MUTATION_SIZE, sum_record_iter / 100])
                print(f"mean:{sum_record_iter / 100},success_pro{success_time / 100}")
                return  result