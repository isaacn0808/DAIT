import pygame
from maze import Maze
from maze import dijkstraAnimate, getDijkstraPath
from GMaze import genAnimate
import maze
import GMaze
import colors
import fonts
import threading
from time import sleep
from jso import uploadData
pygame.init()
class RadioButton:
    CURVATURE = 0.05
    def __init__(self, rect, color1, color2, id, game):
        self.rect = rect
        self.color1 = color1
        self.color2 = color2
        self.id = id
        self.game = game

    def draw(self):
        if self.game.selectStates[self.id]:
            pygame.draw.rect(self.game.window, self.color2, self.rect, border_radius = int(self.rect.w * self.CURVATURE))
        else:
            pygame.draw.rect(self.game.window, self.color1, self.rect, border_radius = int(self.rect.w * self.CURVATURE))

class Button:
    CURVATURE = 0.05
    def __init__(self, rect, text, color1, color2, game):
        self.rect = rect
        self.color1 = color1
        self.color2 = color2
        self.game = game
        self.text = text
        self.pressed = False
    
    def draw(self):
        if self.pressed:
            pygame.draw.rect(self.game.window, self.color2, self.rect, border_radius = int(self.rect.w * self.CURVATURE))
        else:
            pygame.draw.rect(self.game.window, self.color1, self.rect, border_radius = int(self.rect.w * self.CURVATURE))
        text = fonts.barlow30.render(self.text, True, colors.white)
        textRect = text.get_rect(center = self.rect.center)
        self.game.window.blit(text, textRect)

        
class Game:
    def __init__(self, maze, uuid):
        self.window = pygame.display.set_mode((1280, 720))
        self.running = True
        self.playing = False
        self.BG_COLOR = colors.darkGray
        self.selectStates = [False, False, False]
        # add radiobuttons to the screen
        self.radiobuttons = []
        self.radiobuttons.append(RadioButton(pygame.Rect(400, 100, 50, 50), colors.white, colors.green, 0, self))
        self.radiobuttons.append(RadioButton(pygame.Rect(400, 300, 50, 50), colors.white, colors.green, 1, self))
        self.radiobuttons.append(RadioButton(pygame.Rect(400, 500, 50, 50), colors.white, colors.green, 2, self))

        # add buttons to the screen
        self.goButton = Button(pygame.Rect(210, 660, 100, 50), "Go!", colors.green, colors.darkGreen, self)
        self.clearButton = Button(pygame.Rect((330, 660, 90, 50)), "Clear", colors.red, colors.darkRed, self)

        # add text to the screen
        self.charText1 = fonts.barlow30.render("Navigator Nancy", True, colors.blond)
        self.charText2 = fonts.barlow30.render("The Deep Thinker", True, colors.blond)
        self.charText3 = fonts.barlow30.render("Genie-ous Georgie", True, colors.blond)
        self.charText1Rect = pygame.Rect(100, 100, 300, 100)
        self.charText2Rect = pygame.Rect(100, 300, 300, 100)
        self.charText3Rect = pygame.Rect(100, 500, 300, 100)
        # description texts
        self.descText1_1 = fonts.barlow20.render("Uses Dijkstra's algorithm, a simple way to navigate any", True, colors.white)
        self.descText1_2 = fonts.barlow20.render("maze, but often coming at the cost of time: every path", True, colors.white) 
        self.descText1_3 = fonts.barlow20.render("needs to be searched.", True, colors.white)
       
        self.descText2_1 = fonts.barlow20.render("Is really good at one specific maze. It has trained for", True, colors.white)
        self.descText2_2 = fonts.barlow20.render("this maze for hours, but that doesn't mean it is good at others.", True, colors.white)

        self.descText3_1 = fonts.barlow20.render("Georgie squirms like a worm, and can pass through walls. He uses", True, colors.white)
        self.descText3_2 = fonts.barlow20.render("an algorithm very similar to the natural process of evolution,", True, colors.white)
        self.descText3_3 = fonts.barlow20.render("the gen(i)etic algorithm, to (try to) find the path that passes", True, colors.white)
        self.descText3_4 = fonts.barlow20.render("through the least amount of walls.", True, colors.white)

        self.descText1Rect1 = pygame.Rect(5, 150, 300, 50)
        self.descText1Rect2 = pygame.Rect(5, 175, 300, 50)
        self.descText1Rect3 = pygame.Rect(5, 200, 300, 50)
        self.descText2Rect1 = pygame.Rect(5, 350, 300, 50)
        self.descText2Rect2 = pygame.Rect(5, 375, 300, 50)
        self.descText3Rect1 = pygame.Rect(5, 550, 300, 50)
        self.descText3Rect2 = pygame.Rect(5, 575, 300, 50)
        self.descText3Rect3 = pygame.Rect(5, 600, 300, 50)
        self.descText3Rect4 = pygame.Rect(5, 625, 300, 50)

        self.deepQWarningText = fonts.barlow20.render("Hey look! This is the maze that the Deep Thinker specializes at!", True, "orange")
        self.deepQWarningRect = pygame.Rect(5, 415, 300, 50)
        self.character = -1
        self.maze = maze
        self.mazeNum = 0
        self.mazeRect = pygame.Rect(560, 0, 720, 720)
        self.goldCoin = pygame.image.load("images/goldcoin.jpg")
        self.goldCoin = pygame.transform.scale(self.goldCoin, (20, 20))
        self.dijsktraLayer = pygame.Surface((720, 720), pygame.SRCALPHA)
        self.dijkstraBranchingLayer = pygame.Surface((720, 720), pygame.SRCALPHA)
        self.dijsktraLayer.fill((0, 0, 0, 0))
        self.dijkstraBranchingLayer.fill((0, 0, 0, 0))
        self.qLayer = pygame.Surface((1280, 720), pygame.SRCALPHA)

        self.genLayer = pygame.Surface((720, 720), pygame.SRCALPHA)
        self.genLayer.fill((0, 0, 0, 0))
        self.genMazeSize = 15

        self.uuid = uuid
        self.threads = []

        self.preMaze = Maze(20, 20)
        self.preMaze.generateRand()
        self.prePath = getDijkstraPath(self.preMaze.grid, (0, 0), (19, 19))
        self.preMazeShowed = False
        self.qMazeRunning = False

    def onSimulationPress(self):
        GMaze.running = False
        maze.running = False
        self.qMazeRunning = False
        self.dijsktraLayer.fill((0, 0, 0, 0))
        self.genLayer.fill((0, 0, 0, 0))
        if self.selectStates == [False, False, False]:
            return 
        for i in range(len(self.selectStates)):
            if self.selectStates[i]:
                self.character = i
        self.mazeNum += 1
        self.playing = True
        uploadData({"maze" : self.maze.asBits(), "selection" : self.character, "uuid" : self.uuid})
        if self.character == 0:
            maze.running = True
            self.clear()
            thread = threading.Thread(target = dijkstraAnimate, args=(self.maze.grid, pygame.Rect(0, 0, 720, 720), (0,0), (19,19), self.dijsktraLayer, self.dijkstraBranchingLayer))
            thread.start()
        elif self.character == 1:
            self.qMazeRunning = True
            self.clear()
            thread = threading.Thread(target = self.deepReinDemo)
            thread.start()
        elif self.character == 2:
            GMaze.running = True
            self.maze = Maze(self.genMazeSize, self.genMazeSize)
            self.clear()
            thread = threading.Thread(target = genAnimate, args=(self.maze, (0,0), (self.genMazeSize - 1, self.genMazeSize - 1), pygame.Rect(0, 0, 720, 720), self.genLayer))
            thread.start()

    def deepReinDemo(self):
        def coordScaling(x, y):
            xScaled = (x * self.mazeRect.w / len(self.maze.grid[0])) + self.mazeRect.x + 16
            yScaled = (y * self.mazeRect.h / len(self.maze.grid)) + self.mazeRect.y + 16
            return xScaled, yScaled
        if self.mazeNum == 3 or self.mazeNum == 7:
            for coord in self.prePath:

                if self.qMazeRunning:
                    xS, yS = coordScaling(coord[0], coord[1])
                    pygame.draw.rect(self.qLayer, "blue", pygame.Rect(xS, yS, 8, 8))
                    sleep(0.2)
        else:
            start = (0, 0)
            exploredPath = []
            dir = ((-1, 0), (1, 0), (0, -1), (0, 1))
            while start not in exploredPath:
                if not self.qMazeRunning:
                    break
                xS, yS = coordScaling(start[0], start[1])
                pygame.draw.rect(self.qLayer, "blue", pygame.Rect(xS, yS, 8, 8))
                sleep(0.2)
                for i, (dx, dy) in enumerate(dir):
                    if not self.maze.grid[start[1]][start[0]].walls[i] and not ((start[0] + dx, start[1] + dy) in exploredPath):
                        exploredPath.append(start)
                        start = (start[0] + dx, start[1] + dy)
                        break
            
                




    def launchThread(self, func):
        thread = threading.Thread(target = func)
        thread.start()
        self.threads.append(thread)
    # should handle every single event 
        
    def clear(self):
        self.maze.generateRand()
        self.dijsktraLayer.fill((0, 0, 0, 0))
        self.dijkstraBranchingLayer.fill((0, 0, 0, 0))
        self.genLayer.fill((0, 0, 0, 0))
        self.qLayer.fill((0, 0, 0, 0))
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.goButton.rect.collidepoint(event.pos):
                    self.goButton.pressed = True
                if self.clearButton.rect.collidepoint(event.pos):
                    self.clearButton.pressed = True
                for button in self.radiobuttons:
                    if button.rect.collidepoint(event.pos):
                        for i in range(len(self.selectStates)):
                            self.selectStates[i] = True if i == button.id else False
                        break
            if event.type == pygame.MOUSEBUTTONUP:
                if self.goButton.pressed:
                    self.goButton.pressed = False
                    self.onSimulationPress()
                if self.clearButton.pressed:
                    self.clearButton.pressed = False
                    self.maze = Maze(20, 20)
                    maze.running = False
                    GMaze.running = False
                    self.qMazeRunning = False
                    self.clear()
                    self.playing = False
            if event.type == pygame.QUIT:
                GMaze.running = False
                maze.running = False
                self.qMazeRunning = False
                sleep(0.25)
                self.running = False
                for thread in self.threads:
                    thread.exit()
                break
        if (self.mazeNum == 2 and not self.playing) or (self.mazeNum == 3 and self.playing) or (self.mazeNum == 6 and not self.playing) or (self.mazeNum == 7 and self.playing):
            self.maze = self.preMaze
    def draw(self):
        self.window.fill(self.BG_COLOR)
        for button in self.radiobuttons:
            button.draw()
        self.goButton.draw()
        self.clearButton.draw()
        self.maze.draw(self.window, pygame.Rect(560, 0, 720, 720), 0.1, colors.lightBlue)
        self.window.blit(self.dijsktraLayer, (560, 0))
        self.window.blit(self.dijkstraBranchingLayer, (560, 0))
        self.window.blit(self.genLayer, (560, 0))
        self.window.blit(self.qLayer, (0, 0))
        if not self.playing:
            self.window.blit(self.goldCoin, (1250, 690))
        self.window.blit(self.charText1, self.charText1Rect)
        self.window.blit(self.charText2, self.charText2Rect)
        self.window.blit(self.charText3, self.charText3Rect)


        self.window.blit(self.descText1_1, self.descText1Rect1)
        self.window.blit(self.descText1_2, self.descText1Rect2)
        self.window.blit(self.descText1_3, self.descText1Rect3)
        self.window.blit(self.descText2_1, self.descText2Rect1)
        self.window.blit(self.descText2_2, self.descText2Rect2)
        self.window.blit(self.descText3_1, self.descText3Rect1)
        self.window.blit(self.descText3_2, self.descText3Rect2)
        self.window.blit(self.descText3_3, self.descText3Rect3)
        self.window.blit(self.descText3_4, self.descText3Rect4)

        if (self.mazeNum == 2 or self.mazeNum == 6) and not self.playing:
            self.window.blit(self.deepQWarningText, self.deepQWarningRect)

    def runLoop(self):
        while self.running:
            self.handleEvents()
            self.draw()
            pygame.display.update()