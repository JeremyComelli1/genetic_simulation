import random
from random import randrange

class EvolvePool:
    def __init__(self, pop_size, target, genes=' abcdefghijklmnopqrstuvwxyz', advanced_fitness=False, mut_rate=0.1):
        self.pop_size = pop_size
        self.mut_rate = mut_rate
        self.target = target
        self.genes = genes
        self.advanced = advanced_fitness
        self.pop = self.initialize_random_population(self.pop_size, len(self.target), self.genes)



        # remove from init
        self.compute_population_fitness(self.pop, self.target)
        fit_pop = self.natural_selection(self.pop)
        self.breed_populations(self.pop, fit_pop)


    def get_pop(self):
        return self.pop

    # Initializes a base population with random genes
    # In current iteration, pop size has a fixed gene size
    @staticmethod
    def initialize_random_population(pop_size, target_size, possible_genes):
        print("== Generating base population of "+ str(pop_size) +" members ==")
        population = list()
        # For each individual in pop_size
        for i in range(pop_size):
            # Create a genetic sequence
            genes = ""
            # For each symbol in the sequence
            for j in range(target_size):
                # Insert a random gene at every position
                gene = possible_genes[random.randrange(len(possible_genes))]
                genes += gene
            individual = [0, genes]
            population.append(individual)
        print("First Generation successfully generated")
        return population

    # Gives a fitness score to each individual from a given population
    def compute_population_fitness(self, population, target):
        print("Computing fitness...")
        # Set fitness score for each individual
        for i in range(len(population)):
            population[i][0] = self.compute_individual_fitness(population[i], target)
        # Sort by smallest fitness
        return population

    def compute_individual_fitness(self, individual, target):
        print("== Computing fitness ==")
        # Fitness starts at 0, if it increments it's bad
        fitness_score = 0

        # For each letter in target
        for j in (range(len(target))):
            # If current letter doesn't match the corresponding letter in individual's sequence
            if target[j] is not individual[1][j]:
                # 2 fitness solutions are available, I want to find out which one is best
                if self.advanced:
                    # according to the position in genes, calculate a fitness value based on the distance between indexes (greater distance = greater fitness
                    fitness_score += abs(self.genes.index(target[j]) - self.genes.index(target[j]))
                else:
                    # simple fitness: everytime a gene doesn't match, increase fitness by 1
                    fitness_score +=1
        return fitness_score

    # Returns percentage % of the top of the individual candidates
    @staticmethod
    def natural_selection(population, percentage=0.5):
        population.sort()
        half = round(percentage * len(population))

        return population[0:half]

    # Mixes the gene of pop_base with the genes that achieved a better fitness overall
    @staticmethod
    def breed_populations(pop_base, pop_selected, crossover_point=0.5, random_mix=False):
        new_pop = list()
        for i in range(len(pop_base)):
            # Select next individual from base pop, and a random one from the evolved population
            individual_base = pop_base[i]
            random_selected = pop_selected[randrange(len(pop_selected))]

            # Selects a point where the sequence is cut in 2
            crossover_index = round(len(individual_base[1]) * crossover_point)
            # Coin toss to select whether we start collecting genes from the base parent or the selected parent
            base = bool(round(random.random()))

            child_sequence = ""

            # For each letter in the sequence
            for j in range(len(individual_base[1])):
                if random_mix:
                    print("Not implemented yet")
                else:
                    # Append a letter from either the base parent or the selected parent
                    if base:
                        child_sequence += individual_base[1][j]
                    else:
                        child_sequence += random_selected[1][j]
                # Once the crossover is reached, swap the source of the genes
                if j == crossover_index:
                    base = not base
            # Append a child sequence to the new pop, set fitness to 0
            new_pop.append([0, child_sequence])
        return new_pop

    def mutate_population(self, pop_base, genes, mut_rate=0.1):
        # For every individual in current pop
        for i in range(len(pop_base)):
            # For every gene in current sequence
            for j in range(len(pop_base[i][1])):
                # Randomly mutate some genes
                if random.random() < mut_rate:
                    pop_base[i][1][j]  = genes[random.randrange(0, len(genes))]
        return pop_base