import random

class GA:
    def __init__(self, max_gen, n = 8, mutation_prob = 0.05, initial_population_size = 100):
        self.board_size = n
        self.mutation_probability = mutation_prob
        self.initial_population_size = initial_population_size
        self.max_gen = max_gen

    def display(self, arr):
        if self.board_size < 16:
            board = [[0 for x in range(self.board_size)] for y in range(self.board_size)]
            for i in range(len(arr)):
                board[arr[i]][i] = 1
            disp = ""
            for row in board:
                disp += str(row) +"\n"
            print("Board:\n" + disp)
        print("Vector representation: " + str(arr))

    #We define fitness as the 1-(total number of queens that are attacking between themselves/total number of queens),
    #so that fitness(x) is also a probabiity function and fitness(x) = 1 means x is a solution
    def fitness(self, arr):
        counter = 0
        #save i-q_i values
        minus = []
        for i in range(len(arr)):
            minus.append(i-arr[i])
        #count repeated values, that is, pairs of i,j with i - q_i = j - q_j
        values = dict((i,0) for i in minus)
        for i in minus:
            values[i] += 1
        for i in values.keys():
            if values[i] > 1:
                counter += values[i]

        #the same but for i+q_i
        plus = []
        for i in range(len(arr)):
            plus.append(i + arr[i])
        # count repeated values, that is, pairs of i,j with i + q_i = j + q_j
        values = dict((i, 0) for i in plus)
        for i in plus:
            values[i] += 1
        for i in values.keys():
            if values[i] > 1:
                counter += values[i]

        return 1-(counter/self.board_size)

    #based on aptitude selection, candidates with better fitness are more likely to be chosen
    def selection(self, generation, amount):
        fitness = [self.fitness(x) for x in generation]
        avg = sum(fitness)/len(fitness)
        parents = []
        for i in range(len(generation)):
            if fitness[i] > avg:
                parents.append(generation[i])
        x = amount - len(parents)
        if x > 0:
            fill = random.choices(generation, k=x)
            parents += fill

        return parents

    def generatePopulation(self, population_size):
        population = []
        for x in range(population_size):
            arrange = random.sample(range(self.board_size), self.board_size)
            population.append(arrange)

        return population

    def nextPopulation(self, actual_generation, mut_prob):
        parents = self.selection(actual_generation, int(self.initial_population_size/2))
        next_gen = parents.copy()
        for i in range(int(len(parents)/2)):
            #crossover
            parent1 = parents[2*i]
            parent2 = parents[2*i + 1]
            [child1, child2] = self.crossover(parent1, parent2)
            #mutation
            child1 = self.mutate(child1, mut_prob)
            child2 = self.mutate(child2, mut_prob)
            next_gen.append(child1)
            next_gen.append(child2)

        return next_gen

    def mutate(self, child, mut_prob):
        if random.uniform(0,1) > 1-mut_prob:
            places = random.sample(range(len(child)), 2)
            num = child[places[1]]
            child[places[1]] = child[places[0]]
            child[places[0]] = num
        return child

    def crossover(self, parent1, parent2):
        first_half = int(len(parent1)/2)+1
        child1 = []
        pos = []
        for i in range(len(parent1)):
            if parent1[i]<first_half:
                child1.append(parent1[i])
            else:
                child1.append("*")
                pos.append(i)
        child1_missing = [x for x in parent2 if x>= first_half]
        for i in child1_missing:
            child1[pos[0]] = i
            pos = pos[1:]

        child2 = []
        pos = []
        for i in range(len(parent2)):
            if parent2[i]<first_half:
                child2.append(parent2[i])
            else:
                child2.append("*")
                pos.append(i)
        child2_missing = [x for x in parent1 if x >= first_half]
        for i in child2_missing:
            child2[pos[0]] = i
            pos = pos[1:]

        return child1, child2

    def run_algo(self):
        actual_population = self.generatePopulation(self.initial_population_size)
        gen = 0
        self.display(actual_population[0])
        for i in range(self.max_gen):
            actual_population = self.nextPopulation(actual_population, self.mutation_probability)

        #here ends the algo, the next code is for output
        fitness = [self.fitness(x) for x in actual_population]
        avg = sum(fitness)/len(fitness)
        maxs = []
        max_fitness = fitness[0]
        for i in range(1, len(fitness)):
            if fitness[i] > max_fitness:
                max = fitness[i]

        sol_index = fitness.index(max_fitness)
        sol = actual_population[sol_index]
        self.display(sol)
        print("last generation size: "+ str(len(actual_population)))
        print("fitness of solution: "+str(self.fitness(sol)))
        return avg, max_fitness, sol



#TODO fix rapid growth of generation size

x = GA(20)
x.run_algo()
"""
x=GA(10)
for_testing = [7, 2, 0, 4, 1, 5, 6, 3]
x.display(for_testing)
print(x.fitness(for_testing))
"""