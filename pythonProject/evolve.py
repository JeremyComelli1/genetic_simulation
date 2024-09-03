import random
import os
from subprocess import call
from random import randrange

class EvolvePool:
    def __init__(self, pop_size, target, genes=' abcdefghijklmnopqrstuvwxyz', advanced_fitness=False, mut_rate=0.1):
        self.pop_size = pop_size
        self.mut_rate = mut_rate
        self.target = target
        self.genes = genes
        self.advanced = advanced_fitness
        self.pop = self.initialize_random_population(self.pop_size, len(self.target), self.genes)

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
        return population

    # Gives a fitness score to each individual from a given population
    def compute_population_fitness(self, population, target):
        # Set fitness score for each individual
        for i in range(len(population)):
            population[i][0] = self.compute_individual_fitness(population[i], target)
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
        lowest_fitness = population[0][0]
        # If fitness hits 0, we found the best possible sequence, so that's what we return
        # TODO: needs improvement, as a perfect solution typically doesn't exist for most problems
        if lowest_fitness < 1:
            return [0, population[0][1]]
        else:

            print("Best guess: " + population[0][1] +" "+ " Fitness: " + str(lowest_fitness) + " " + self.get_progress(lowest_fitness))

        half = round(percentage * len(population))

        return population[0:half]

    # Mixes the gene of pop_base with the genes that achieved a better fitness overall
    @staticmethod
    def breed_populations(pop_base, pop_selected, crossover_point=0.5, random_mix=False):
        new_pop = list()
        for i in range(len(pop_base)):
            # Select a random individual from base pop, and a random individual from the population with best fitness
            random_base = pop_base[random.randrange(len(pop_base))]
            random_selected = pop_selected[randrange(len(pop_selected))]

            # Selects a point where the sequence is cut in 2
            crossover_index = random.randrange(len(random_base[1]) - 1)
            child_sequence = ""
            crossover_reached = False

            # For each letter in the sequence
            for j in range(len(random_base[1])):
                # Once the crossover is reached, swap the source of the genes
                if j == crossover_index:
                    crossover_reached = True
                if random_mix:
                    print("Not implemented yet")
                    exit(1)
                else:
                    # Append a letter from either the base parent or the selected parent
                    if not crossover_reached:
                        child_sequence += random_base[1][j]
                    else:
                        child_sequence += random_selected[1][j]

            # Append a child sequence to the new pop, set fitness to 0
            new_pop.append([0, child_sequence])
        return new_pop

    @staticmethod
    def mutate_population(pop_base, genes, mut_rate=0.1):
        mutations_count = 0
        # For every individual in current pop
        for i in range(len(pop_base)):
            # For every gene in current sequence
            for j in range(len(pop_base[i][1])):
                # Randomly mutate some genes
                if random.random() < mut_rate:
                    mutations_count += 1
                    extracted_gene = list(pop_base[i][1])
                    extracted_gene[j]  = genes[random.randrange(0, len(genes))]
                    pop_base[i][1] = ''.join(extracted_gene)
        return pop_base

    def evolve_pool(self):
        fitness = -1
        generations = 0
        result = ''
        population_current_iteration = self.pop
        print("Current generation: " + str(generations))
        while True:
            generations += 1
            # Pipeline: Calculate fitness -> kill off higher fitness individuals
            selected_population_current_iteration = self.natural_selection(self.compute_population_fitness(population_current_iteration, self.target))
            # If a single result is returned, we hit fitness = 0
            if len(selected_population_current_iteration) < 3:
                # Lowest fitness has been reached, output best candidate
                result = selected_population_current_iteration
                break
            else:
                # If solution is not reached, Pipeline continues: Breed population -> introduce random mutations, then go back to start
                population_current_iteration = self.mutate_population(self.breed_populations(population_current_iteration, selected_population_current_iteration), self.genes)

        print("Result found in "+ str(generations) +" generations.")
        print("Result is "+ str(result))
        return result, generations

    @staticmethod
    def get_progress(fitness):
        progress_bar = ""
        for i in (range(fitness)):
            progress_bar+="o"
        return progress_bar