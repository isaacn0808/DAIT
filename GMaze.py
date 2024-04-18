import random
from maze import Maze
import pygame
from time import sleep
running = True
# Define the genetic algorithm parameters
def genAnimate(maze, startin, end, rect, screen):
    global running
    directions = {'up' : (0, -1), 'down' : (0, 1), 'left' : (-1, 0), 'right' : (1, 0)}
    def getPath(solution):
        path = []
        start = startin
        for action in solution:
            path.append(start)
            if action == 'up':
                start = (start[0], start[1] - 1)
            elif action == 'down':
                start = (start[0], start[1] + 1)  
            elif action == 'left':
                start = (start[0] - 1, start[1])
            elif action == 'right':
                start = (start[0] + 1, start[1])
            if start == end:
                path.append(start)
                break
        return path
    
    population_size = 1000
    mutation_rate = 0.01
    num_generations = 100
    pathLength = 100
    maze_map = maze
    maze_map.generateRand()
    goal = end
    # Generate population of random solutions
    def genPop(size):
        population = []
        for i in range(size):
            firstMove = random.choice(('down', 'right'))
            solution = [firstMove]
            length = 1
            start = startin
            if firstMove == 'down':
                start = (start[0], start[1] + 1)
            else:
                start = (start[0] + 1, start[1])
            while length < pathLength:
                action = random.choices(['up', 'down', 'left', 'right'], weights = [1, 3, 1, 3], k = 1)[0]
                if action == 'up' and solution[-1] != 'down' and start[1] > 0:
                    solution.append(action)
                    start = (start[0], start[1] - 1)
                    length += 1
                elif action == 'down' and solution[-1] != 'up' and start[1] < end[1]:
                    solution.append(action)
                    start = (start[0], start[1] + 1)  
                    length += 1
                elif action == 'left' and solution[-1] != 'right' and start[0] > 0:
                    solution.append(action)
                    start = (start[0] - 1, start[1])
                    length += 1
                elif action == 'right' and solution[-1] != 'left' and start[0] < end[0]:
                    solution.append(action)
                    start = (start[0] + 1, start[1])
                    length += 1
                if start == end:
                    break
            population.append(solution)
        return population
    # Define the fitness function
    def fitness(solution):
        # ends at start
        time = 0
        path = getPath(solution)
        start = startin
        for action in solution:
            time += 1        
            if action == 'up':
                if start[1] > 0:
                    start = (start[0], start[1] - 1)   
            elif action == 'down':
                if start[1] < len(maze_map.grid) - 1:
                    start = (start[0], start[1] + 1)   
            elif action == 'left':
                if start[0] > 0:
                    start = (start[0] - 1, start[1]) 
            elif action == 'right':
                if start[0] < len(maze_map.grid[0]) - 1:
                    start = (start[0] + 1, start[1])  
            if start == goal:
                penalty = 0
                for i, move in enumerate(solution[:time]):
                    try:
                        if move == 'up':
                            if maze_map.grid[path[i][1]][path[i][0]].walls[2]:
                                penalty += 3
                        elif move == "down":
                            if maze_map.grid[path[i][1]][path[i][0]].walls[3]:
                                penalty += 3
                        elif move == "left":
                            if maze_map.grid[path[i][1]][path[i][0]].walls[0]:
                                penalty += 3
                        elif move == "right":
                            if maze_map.grid[path[i][1]][path[i][0]].walls[1]:
                                penalty += 3
                        penalty += 0.1
                    except IndexError:
                        return -9999
                return -1 * penalty + (300 / time)
        return -9999


    # Define the selection function
    def selection(population, fitness_scores):
        sor = list(reversed(sorted(population, key=fitness)))
        total_fitness = sum(fitness(solution) for solution in population)
        probabilities = [fitness(solution)/total_fitness for solution in population]
        selected = []
        for i in range(10):
            selected.append(sor[i])
        for i in range(len(population) - 310):
            chosen = random.choices(population, weights=probabilities)[0]
            selected.append(chosen)
        newBatch = genPop(300)
        for i in range(300):
            selected.append(newBatch[i])
        return selected


    # Define the crossover function (single-point crossover)
    def crossover(parent1, parent2):
        crossover_point = random.randint(0, min(len(parent1)-1, len(parent2) - 1))
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    # Define the mutation function
    def mutation(solution):
        mutated_solution = solution.copy()
        solPath = getPath(solution)
        def kinkMutation(i):
            if i <= len(solution) - 1 and i <= len(solPath) - 1:
                if random.random() < 0.5:
                    if (solution[i] == "up" or solution[i] == "down" ) and solPath[i][0] > 0:
                        mutated_solution.insert(i, "left")
                        mutated_solution.insert(i + 2, "right")
                    elif (solution[i] == "left" or solution[i] == "right") and solPath[i][1] > 0:
                        mutated_solution.insert(i, "up")
                        mutated_solution.insert(i + 2, "down")
                else:
                    if (solution[i] == "up" or solution[i] == "down" ) and solPath[i][0] < len(maze_map.grid[0]):
                        mutated_solution.insert(i, "right")
                        mutated_solution.insert(i + 2, "left")
                    elif (solution[i] == "left" or solution[i] == "right") and solPath[i][1] < len(maze_map.grid):
                        mutated_solution.insert(i, "down")
                        mutated_solution.insert(i + 2, "up")

        for i in range(len(mutated_solution)):
            if random.random() < mutation_rate:
                kinkMutation(i)
        return mutated_solution

    def coordScaling(x, y):
        xScaled = (x * rect.w / len(maze_map.grid[0])) + rect.x + 20
        yScaled = (y * rect.h / len(maze_map.grid)) + rect.y + 20
        return xScaled, yScaled
    
    # Run the genetic algorithm
    bestSolutions = []
    population = genPop(population_size)
    print("Population generated")
    for _ in range(num_generations):
        if running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return
            # Evaluate fitness of each solution
            fitness_scores = [fitness(solution) for solution in population]
            
            # Select parents for reproduction
            parents = selection(population, fitness_scores)
            
            # Create offspring through crossover
            #offspring = parents.copy()

            offspring = parents[:10]

            for i in range(population_size//2):
                parent1 = random.choice(parents[10:])
                parent2 = random.choice(parents[10:])
                child1, child2 = crossover(parent1, parent2)
                child1, child2 = (parent1, parent2)
                offspring.append(child1)
                offspring.append(child2)
            
            # Introduce mutation
            offspring = parents[:10] + [mutation(solution) for solution in offspring[10:]]
            
            # Replace the old population with the new generation
            population = offspring
            
            # Check if a solution is found
            bestSolution = max(population, key=fitness)
            bestSolutions.append(bestSolution)
            print(fitness(bestSolution))
            best = getPath(bestSolution)
            tempLayer = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            tempLayer.fill((0, 0, 0, 0))
            for i, coord in enumerate(best):
                coordS = coordScaling(coord[0], coord[1])
                #nextCoord = coordScaling(best[i+1][0], best[i+1][1])
                pygame.draw.rect(tempLayer, "red", pygame.Rect(coordS[0], coordS[1], 20, 20))
            screen.fill((0, 0, 0, 0))
            screen.blit(tempLayer, (0, 0))
        else:
            break

    bestSolEver = max(bestSolutions, key=fitness)
    bestSol = getPath(bestSolEver)
    tempLayer = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    tempLayer.fill((0, 0, 0, 0))
    for i, coord in enumerate(bestSol):
        coordS = coordScaling(coord[0], coord[1])
        #nextCoord = coordScaling(best[i+1][0], best[i+1][1])
        pygame.draw.rect(tempLayer, "blue", pygame.Rect(coordS[0], coordS[1], 20, 20))
    while running:
        pass

    print("Best Solution Ever:", bestSolEver, fitness(bestSolEver))
    
    screen.fill((0, 0, 0, 0))
    
    return bestSolEver
if __name__ == "__main__":
    m = Maze(20, 20)
    scre = 0