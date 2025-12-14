'''
CSE 545 Final Project - nQueens

'''
import pygame
import random
import time
from random import randrange
from operator import itemgetter

def create_chessboard(n, queens=[]):
    chessboard = [['Q' if (col + row * n) in queens else col + row * n for col in range(n)] for row in range(n)]
    return chessboard

def draw_chessboard(screen, chessboard, queen_positions, square_size):
    for row in range(len(chessboard)):
        for col in range(len(chessboard[row])):
            x = col * square_size
            y = (len(chessboard) - 1 - row) * square_size
            color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0)
            pygame.draw.rect(screen, color, (x, y, square_size, square_size))

            ''' This is indicating position a.k.a starting from 0 bottom left '''
            font = pygame.font.Font(None, 36)
            # text = font.render(str(chessboard[row][col]), True, (0, 225, 144))
            # text_rect = text.get_rect(center=(x + square_size // 2, y + square_size // 2))
            # screen.blit(text, text_rect)

            text_generation = font.render("Generation: " + str(generation), True, (100, 255, 100))
            screen.blit(text_generation, (20, 20))

            # Draw circles for queens
            if chessboard[row][col] == 'Q':
                queen_radius = square_size // 4
                pygame.draw.circle(screen, (255, 0, 0), (x + square_size // 2, y + square_size // 2), queen_radius)

pygame.init()

# Get user input for the board size
board_size = int(input("Enter the board size (n = ?): "))

# Set up the window
window_size = 600
screen = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("n-Queens")

clock = pygame.time.Clock()

# GA parameters
running = True
generation = 0
generations = 100
gen_size = 200
expert_rate = 0.1

# def initial population
def create_population():
        solution = []
        while len(solution) < board_size:
            queen_position = randrange(0, board_size*board_size)
            if queen_position not in solution:
                solution.append(queen_position)
        return solution

# def select parents
def ChooseParent(currentGen, n, avgFitness):
    baseRate = 10 #10%, every solution has 10% chance to be chosen, regardless of fitness
    #value can be ajdusted to change behavior, though naturally should be between 0-100.
    #extreme values may cause undesirable behavior

    k = 3 #this variable increases importance of fitness. A fitness modifier will be obtained by
    #dividing generation avg fitness by candidate fitness. Val > 1 means good fitness and vice versa
    #This val is taken to the power of k and then applied to base rate. Thus, k exagerrates fitness by
    #increasing values > 1 and decreasing values < 1
    #Note: Values of k < 0 do nothing. k = 0 means fitness doesn't matter, 10% chance for all

    noChoice = True #is true as long as no parent is chosen

    while noChoice:
        for x in currentGen:
            candidateFitness = fitness(x, n)    #calcultes fitness of candidate in generation
            if candidateFitness == 0:  
                candidateFitness = 0.001 #set to insure no division by 0
            fitnessMod = avgFitness / candidateFitness
            #n / m > 1 if m < n. fitnessMod will be applied to base rate. Higher fitness, better chance

            if k == 1:
                fitnessMod = 1 #base rate * 1, fitness does nothing
            else:
                counter = 1
                while counter < k: #negative k values do nothing
                    fitnessMod = fitnessMod * fitnessMod
                    counter += 1

            chance = baseRate * fitnessMod  #calculates chance of fitness

            roll = random.randrange(0, 100)

            if roll <= chance:  #rolls to see if within calculated chance, if yes, chosen as parent
                noChoice = False
                return x
            
def ChooseSecondParent(currentGen, n, avgFitness, parent1):
    #almost identical to the first function, just has a small check to make sure two different
    #parents are chosen for crossover. There was previously no safeguard against this
    
    baseRate = 10 #10%, every solution has 10% chance to be chosen, regardless of fitness
    #value can be ajdusted to change behavior, though naturally should be between 0-100.
    #extreme values may cause undesirable behavior

    k = 3 #this variable increases importance of fitness. A fitness modifier will be obtained by
    #dividing generation avg fitness by candidate fitness. Val > 1 means good fitness and vice versa
    #This val is taken to the power of k and then applied to base rate. Thus, k exagerrates fitness by
    #increasing values > 1 and decreasing values < 1
    #Note: Values of k < 0 do nothing. k = 0 means fitness doesn't matter, 10% chance for all

    noChoice = True

    while noChoice:
        for x in currentGen:
            candidateFitness = fitness(x, n)
            if candidateFitness == 0:
                candidateFitness = 0.001
            fitnessMod = avgFitness / candidateFitness
            #n / m > 1 if m < n. fitnessMod will be applied to base rate. Higher fitness, better chance

            if k == 1:
                fitnessMod = 1 #base rate * 1, fitness does nothing
            else:
                counter = 1
                while counter < k: #negative k values do nothing
                    fitnessMod = fitnessMod * fitnessMod
                    counter += 1

            chance = baseRate * fitnessMod

            roll = random.randrange(0, 100)

            if roll <= chance and not (x == parent1):
                noChoice = False
                return x

# def fitness function
def fitness(solution_data, n):
    fitness_val = 0

    for x in solution_data:
        attack_locations = set() #empty set, will be populated by helper functions
        attack_locations = attack_locations.union(vertical(x, n))#return val of vertical attacks
        attack_locations = attack_locations.union(horizontal(x, n))#return val of horizontal attacks
        attack_locations = attack_locations.union(diagonal(x, n))#return val of diagonal attacks

        for pos in attack_locations:
            for y in solution_data:
                if y != x:
                    if y == pos:
                        fitness_val += 1

    return fitness_val

def vertical(position, n):
    comparison = position % n #comparison represents the very bottom position of the queens column
    max = n * n - 1

    return_set = set()

    while comparison <= max: #once comparison exceeds max, the next value that it would become is out of range of the board
        return_set.add(comparison)
        comparison += n #adding n to comparison yields the next position value

    return_set.remove(position) #arg position should not be returned (starting position of queen)

    return return_set

def horizontal(position, n):
    min = int(position / n) * n #first position value of positions row
    max = min + n #first position value of the 'next' row up

    return_set = set()

    while min < max:
        if min != position:
            return_set.add(min)
        min += 1

    return return_set

def diagonal(position, n):
    min = 0
    max = n * n - 1

    return_set = set()

    #NW = position + n - 1
    #NE = position + n + 1
    #SW = position - (n + 1)
    #SE = position - (n - 1)
    NW = NE = SW = SE = position

    while NW % n != 0 and NW < n * (n - 1):
        NW += n - 1
        return_set.add(NW)

    while SW % n != 0 and SW > (n - 1):
        SW -= (n + 1)
        return_set.add(SW)

    while NE % n != (n - 1) and NE < n * (n - 1):
        NE += n + 1
        return_set.add(NE)

    while SE % n != (n - 1) and SE > (n - 1):
        SE -= (n - 1)
        return_set.add(SE)


    return return_set

# def crossover function
def crossover(parent1, parent2):
    offspring = []
    midpoint = len(parent1) // 2
    offspring1 = parent1[:midpoint]
    offspring2 = parent1[midpoint:]
    remaining_elements1 = [element for element in parent2 if element not in offspring1]     #remove elements from parent2 that are already in offspring1
    random_integer1 = random.sample(remaining_elements1, len(parent1) - len(offspring1))
    remaining_elements2 = [element for element in parent2 if element not in offspring2]     #remove elements from parent2 that are already in offspring2
    random_integer2 = random.sample(remaining_elements2, len(parent2) - len(offspring2))
    for integer in random_integer1:
        if len(offspring1) < len(parent1) and integer not in offspring1: 
            offspring1.append(integer)
    for integer in random_integer2:
        if len(offspring2) < len(parent1) and integer not in offspring2: 
            offspring2.append(integer)
    offspring.append(offspring1)
    offspring.append(offspring2)
    return offspring

# def mutate function
def mutate(input, n):
    #takes solution to mutate as argument, along with board dimension 'n'
    #returns mutated solution
    
    #example use case:
    #exList = [3, 5, 8, 11, 13, 24, 47, 55]
    #exList = mutate(exList, 8)
    
    #this mutation replaces a random index/data point with a random, valid integer data point
    #you could loop the mutation if you want to change multiple values
    
    #randomly selects and index to mutate
    count = len(input)
    index = random.randrange(0, (count - 1))

    valid = False

    #makes sure the value is unique and not already in solution
    value = random.randrange(0, (n * n - 1))
    while not valid:
        valid = True
        for x in input:
            if x == value:
                valid = False
        if not valid:
            value = random.randrange(0, (n * n - 1))

    #swapps value with mutated value
    input[index] = value
    return input

#initial popoulation of solutions for current generation
current_generation = []
#creates a valid board config
for element in range(gen_size):
    current_generation.append(create_population())

# for i in current_generation:
#     print(i)

queen_positions = []
new_population = []
fifty_fitness = []
fifty_average = []

# Main game loop
square_size = window_size // board_size

start = time.time()
# for loop for generations
while running and generation < generations:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    '''
    WISDOM OF CROWDS
    '''
    # if generation > 0:
    #     expert_fitness_list = []
    #     expert_list = []
    #     num_experts = int(expert_rate * gen_size)
    #     for element in current_generation:
    #         expert_fitness = fitness(element, board_size)
    #         # print(f'individual {element} has fitness score of {expert_fitness}')
    #         expert_fitness_list.append(expert_fitness)
    #         expert_list.append(element)
    #     res = [list(x)[:num_experts] for x in zip(*sorted(zip(expert_fitness_list, expert_list), key = itemgetter(0)))]

    #     for i in range(gen_size):
    #         if i in res[1]:
    #             other_expert = random.choice(res[1])
    #             current_generation[i] = crossover(current_generation[i], current_generation[other_expert])
    #             current_generation[i] = mutate(current_generation[i], board_size)

    #tracks best fitness, best solution, and average fitness for current generation
    best_fitness = fitness(current_generation[0], board_size)
    best_solution = current_generation[0]
    average_fitness = 0

    #iterates through population to update the values (best sol, best fitnes)
    for element in current_generation:
        fitness_score = fitness(element, board_size)
        average_fitness += fitness_score
        if fitness_score < best_fitness:
            best_solution = element
            best_fitness = fitness_score

    average_fitness = average_fitness / len(current_generation) #calculated avg fitness of current generation

    #tracks and displays best solution every 25 generations
    if generation % 25 == 0:
        fifty_fitness.append(best_fitness)
        fifty_average.append(average_fitness)

    queen_positions = best_solution

    print(f'Generation: {generation}, best solution: {queen_positions}')

    #Selects parents and performs crossover
    while len(new_population) < gen_size:
        temp = ChooseParent(current_generation, board_size, average_fitness)
        offspring = crossover(temp, ChooseSecondParent(current_generation, board_size, average_fitness, temp))

        #has a 10% chance to introduce mutation into the offspring
        rand1 = random.randrange(1, 1000)
        rand2 = random.randrange(1, 1000)

        if rand1 <= 100:
            offspring[0] = mutate(offspring[0], board_size)
        
        if rand2 <= 100:
            offspring[1] = mutate(offspring[1], board_size)

        new_population.append(offspring[0])
        new_population.append(offspring[1])

    #updates current generation with new created population
    current_generation = new_population
    new_population = []

    generation += 1 #tracks generations

    # Create the chessboard with the queens
    chessboard = create_chessboard(board_size, queens = queen_positions)

    # Draw the chessboard with circles for queens
    draw_chessboard(screen, chessboard, queen_positions, square_size)

    pygame.display.flip()
    clock.tick(60)

for i in fifty_fitness:
    print(i)
for i in fifty_average:
    print(i)

end = time.time()
print(f'Total execution time: {end - start}')

user_input = input('Type q to quit: ')
if user_input == 'q':
    running = False

for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False

