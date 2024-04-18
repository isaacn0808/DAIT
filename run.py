from startScreen import start
from menus import runThruMenus
from game import Game
from maze import Maze
from jso import uploadData
import time
import random
import pygame
pygame.init()
startTime = time.time()
window = pygame.display.set_mode((1280, 720))
first, last, grade = start(window)
uuid = random.randint(1, 1000000)
formattedLogin = {"uuid" : uuid, "name" : first, "initial" : last, "grade" : grade, "mazes" : [], "selections" : [], "time" : 0} 
uploadData(formattedLogin)
runThruMenus(window)
m = Maze(20, 20)
m.generateRand()
g = Game(m, uuid)
g.runLoop()

endTime = time.time()
timeTaken = endTime - startTime
uploadData({"time" : timeTaken, "uuid" : uuid})