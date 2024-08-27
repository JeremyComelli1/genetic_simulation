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
        self.pop = self.natural_selection(self.pop)


    def get_pop(self):
        return self.pop

    # Initializes a base population with random genes
    # In current iteration, pop size has a fixed gene size
    def initialize_random_population(self, pop_size, target_size, possible_genes):
        print("== Generating base population of "+ str(pop_size) +" members ==")
        population = list()
        # For each individual in pop_size
        for i in range(pop_size):
            # Create a genetic sequence
            genes = []
            # For each symbol in the sequence
            for j in range(target_size):
                # Insert a random gene at every position
                gene = possible_genes[random.randrange(len(possible_genes))]
                genes.append(gene)
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
    def natural_selection(self, population, percentage=0.5):
        population.sort()
        half = round(percentage * len(population))

        return population[0:half]
