import pygame
import random
import heapq
import fonts
from startScreen import drawBoxAround
from time import sleep
pygame.init()
running = True
class Cell:
    def __init__(self, visited, walls):
        self.visited = visited
        self.walls = walls
    def asBits(self):
        bits = ""
        for wall in self.walls:
            bits += str(int(wall))
        return bits

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Cell(False, [True, True, True, True]) for _ in range(width)] for _ in range(height)]
    
    # draws the maze
    def draw(self, screen, rect, thickness, bg):
        cellDim = (rect.w / self.width, rect.h / self.height)
        wallThickness = thickness * cellDim[0]
        def drawCell(x_i, y_i):
            cellRect = pygame.Rect(rect[0] + cellDim[0] * x_i, rect[1] + cellDim[1] * y_i, cellDim[0], cellDim[1])
            cellInnerRect = pygame.Rect(cellRect.x + wallThickness, cellRect.y + wallThickness, 
                                        cellRect.w - wallThickness, cellRect.h - wallThickness)
            if x_i == 0 and y_i == 0:
                pygame.draw.rect(screen, (bg[0] / 2, bg[1] / 2, bg[2] / 2), cellRect)
            else:       
                pygame.draw.rect(screen, bg, cellRect)
            drawBoxAround(screen, cellInnerRect, wallThickness, lambda edge: (0, 0, 0) if self.grid[y_i][x_i].walls[edge] else bg)
        for y in range(self.height):
            for x in range(self.width):
                drawCell(x, y)

    def generateRand(self):
        def getNeighbor(wall):
            if wall[2] == 0: return (wall[0] - 1, wall[1], 1)
            if wall[2] == 1: return (wall[0] + 1, wall[1], 0)
            if wall[2] == 2: return (wall[0], wall[1] - 1, 3)
            if wall[2] == 3: return (wall[0], wall[1] + 1, 2)
        def getWalls(x, y):
            wallList = []
            cell = self.grid[y][x]
            if x > 0 and cell.walls[0]: wallList.append((x, y, 0))
            if x < self.width - 1 and cell.walls[1]: wallList.append((x, y, 1))
            if y > 0 and cell.walls[2]: wallList.append((x, y, 2))
            if y < self.height - 1 and cell.walls[3]: wallList.append((x, y, 3))
            return wallList
        # Choose a random starting cell
        wallFrontier = []
        start_x, start_y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        self.grid[start_y][start_x].visited = True
        for w in getWalls(start_x, start_y):
            wallFrontier.append(w)
        while wallFrontier:
            # Choose a random wall from the frontier 
            i = random.randrange(len(wallFrontier))
            currX, currY, edge = wallFrontier[i]
            neighborX, neighborY, identEdge = getNeighbor(wallFrontier[i])
            if (neighborX >= 0 and neighborX < self.width and neighborY >= 0 and neighborY < self.height
                and not self.grid[neighborY][neighborX].visited):
                self.grid[currY][currX].walls[edge] = False
                self.grid[neighborY][neighborX].walls[identEdge] = False
                self.grid[neighborY][neighborX].visited = True
                for w in getWalls(neighborX, neighborY):
                    wallFrontier.append(w)
            wallFrontier.pop(i)
        #self.grid[0][0].walls[2] = False
       # self.grid[-1][-1].walls[3] = False
        return -1
    
    def asBits(self):
        bits = []
        for r in self.grid:
            rowBits = []
            for cell in r:
                rowBits.append(cell.asBits())
            bits.append(rowBits)
        return bits
    
    def makeFromBits(self, bits):
        for i in range(len(bits)):
            for j in range(len(bits[i])):
                for k, bit in enumerate(bits[i][j]):
                    self.grid[i][j].walls[k] = bool(int(bit))


def dijkstraAnimate(maze, rect, start, end, screen, screen2):
    global running
    def coordScaling(x, y):
        xScaled = (x * rect.w / len(maze[0])) + rect.x + 20
        yScaled = (y * rect.h / len(maze)) + rect.y + 20
        return xScaled, yScaled
    
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    rows, cols = len(maze), len(maze[0])
    distance = {start: 0}
    queue = [(0, start)]

    while queue:
        if running:
            dist, node = heapq.heappop(queue)
            text = fonts.barlow10.render(str(dist), True, "black")
            xS, yS = coordScaling(node[0], node[1])
            textRect = text.get_rect(center = (xS, yS))
            sleep(0.005)
            screen.blit(text, textRect)

            if node == end:
                break

            for i, (dx, dy) in enumerate(dir):
                x, y = node[0] + dx, node[1] + dy
                if 0 <= x < rows and 0 <= y < cols and not maze[node[1]][node[0]].walls[i]:
                    new_dist = dist + 1
                    if (x, y) not in distance or new_dist < distance[(x, y)]:
                        distance[(x, y)] = new_dist
                        xS, yS = coordScaling(node[0], node[1])
                        xS2, yS2 = coordScaling(x, y)
                    # pygame.draw.rect(screen2, (0, 255, 0), pygame.Rect(min(xS, xS2), min(yS, yS2), abs(xS2 - xS), abs(yS2 - yS)))
                    # pygame.display.flip()
                        heapq.heappush(queue, (new_dist, (x, y)))
        else:
            break
    if running:
        sleep(0.5)
        screen.fill((0, 0, 0, 0))
        path = []
        if end in distance:
            current = end
            while current != start:
                halted = True
                path.append(current)
                for i, (dx, dy) in enumerate(dir):
                    x, y = current[0] + dx, current[1] + dy
                    if (x, y) in distance and distance[(x, y)] == distance[current] - 1 and not maze[current[1]][current[0]].walls[i]:
                        current = (x, y)
                        halted = False
                        break
                if halted:
                    path.remove(current)
                    del distance[current]
            path.append(start)
            path.reverse()
    else: 
        pass
    
    for coord in path:
        if running:
            xS, yS = coordScaling(coord[0], coord[1])
            pygame.draw.rect(screen, "red", pygame.Rect(xS, yS, 5, 5))
            sleep(0.1)
        else:
            pass

    

    return distance, path

def getDijkstraPath(maze, start, end):
    dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    rows, cols = len(maze), len(maze[0])
    distance = {start: 0}
    queue = [(0, start)]

    while queue:
        dist, node = heapq.heappop(queue)

        if node == end:
            break

        for i, (dx, dy) in enumerate(dir):
            x, y = node[0] + dx, node[1] + dy
            if 0 <= x < rows and 0 <= y < cols and not maze[node[1]][node[0]].walls[i]:
                new_dist = dist + 1
                if (x, y) not in distance or new_dist < distance[(x, y)]:
                    distance[(x, y)] = new_dist
                    heapq.heappush(queue, (new_dist, (x, y)))
    path = []
    if end in distance:
        current = end
        while current != start:
            halted = True
            path.append(current)
            for i, (dx, dy) in enumerate(dir):
                x, y = current[0] + dx, current[1] + dy
                if (x, y) in distance and distance[(x, y)] == distance[current] - 1 and not maze[current[1]][current[0]].walls[i]:
                    current = (x, y)
                    halted = False
                    break
            if halted:
                path.remove(current)
                del distance[current]
        path.append(start)
        path.reverse()

    return path
