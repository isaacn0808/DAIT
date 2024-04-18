import pygame
import fonts
import colors
from time import sleep

def runThruMenus(menuWindow):

    screen1 = True
    screen2 = False
    screen3 = False

    # screen 1 stuff
    titleText1 = fonts.jejuhal70.render("Welcome to GENI-E!", True, "white")
    titleText1Rect = pygame.Rect(280, 63, 820, 73)
    text1 = fonts.jejuhal30.render("Let's show you how to play the game:", True, "white")
    text1Rect = pygame.Rect(150, 197, 325, 76)
    text2 = fonts.jejuhal30.render("Your character's objective is to get this gold coin:", True, "white")
    text2Rect = pygame.Rect(220, 316, 528, 87)
    text3 = fonts.jejuhal30.render("However, your objective is to have fun.", True, "white")
    text3Rect = pygame.Rect(268, 516, 422, 81)
    button1Rect = pygame.Rect(1017, 594, 219, 91)
    button1Text = fonts.barlow30.render("Next", True, "white")
    button1TextRect = button1Text.get_rect()
    button1TextRect.center = button1Rect.center
    coin = pygame.image.load("images/goldcoin.jpg")
    coin = pygame.transform.scale(coin, (160, 160))

    # screen 2 stuff
    text4 = fonts.jejuhal30.render("You will be given a different maze each round:", True, colors.white)
    text4Rect = pygame.Rect(77, 31, 752, 92)
    text5 = fonts.jejuhal20.render("Each character that you select will be trained with a different AI model.", True, colors.white)
    text5Rect = pygame.Rect(550, 200, 600, 100)
    dashboard = pygame.image.load("images/dashboard.png")
    dashboard = pygame.transform.scale(dashboard, (300, 392))
    maze1 = pygame.image.load("images/maze.png")
    maze1 = pygame.transform.scale(maze1, (400, 400))
    button2Rect = pygame.Rect(1000, 594, 200, 100)
    button2Text = fonts.barlow30.render("Next", True, "white")
    button2TextRect = button2Text.get_rect()
    button2TextRect.center = button2Rect.center
    backButton2Rect = pygame.Rect(50, 620, 80, 80)
    backButton2Text = fonts.barlow30.render("Back", True, "white")
    backButton2TextRect = backButton2Text.get_rect()
    backButton2TextRect.center = backButton2Rect.center

    # screen 3 stuff
    text6 = fonts.jejuhal40.render("Play around and figure out what each character is good at!", True, colors.white)
    text6Rect = pygame.Rect(100, 100, 600, 100)
    text7 = fonts.jejuhal20.render("Later on you will be asked questions about the different AI algorithms...", True, colors.white)
    text7Rect = pygame.Rect(160, 200, 600, 100)
    text8 = fonts.jejuhal20.render("Tip: if it looks like it got stuck, hit Clear and keep playing!", True, colors.white)
    text8Rect = pygame.Rect(160, 240, 600, 100)
    text9 = fonts.jejuhal20.render("Once you feel like you are done, exit the window and go to the Google Forms loaded in the browser.", True, colors.white)
    text9Rect = pygame.Rect(180, 320, 600, 100)
    button3Rect = pygame.Rect(490, 385, 250, 250)
    button3Text = fonts.jejuhal70.render("Start!", True, colors.white)
    button3TextRect = button3Text.get_rect()
    button3TextRect.center = button3Rect.center
    backButton3Rect = pygame.Rect(50, 620, 80, 80)
    backButton3Text = fonts.barlow30.render("Back", True, "white")
    backButton3TextRect = backButton3Text.get_rect()
    backButton3TextRect.center = backButton3Rect.center



    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (screen1 and button1Rect.collidepoint(event.pos)) or (screen3 and backButton3Rect.collidepoint(event.pos)):
                   screen1 = False
                   screen2 = True
                   screen3 = False
                elif (screen2 and backButton2Rect.collidepoint(event.pos)):
                    screen1 = True
                    screen2 = False
                elif screen2 and button2Rect.collidepoint(event.pos):
                   screen2 = False
                   screen3 = True
                elif screen3 and button3Rect.collidepoint(event.pos):
                    screen3 = False
                    running = False
            
            if event.type == pygame.MOUSEBUTTONUP:
                pass
        menuWindow.fill(colors.darkBlue)
        if screen1:
            menuWindow.blit(titleText1, titleText1Rect)
            menuWindow.blit(text1, text1Rect)
            menuWindow.blit(text2, text2Rect)
            menuWindow.blit(text3, text3Rect)
            menuWindow.blit(coin, (1000, 316))
            pygame.draw.rect(menuWindow, colors.green, button1Rect, border_radius = 10)
            menuWindow.blit(button1Text, button1TextRect)
        if screen2: 
            menuWindow.blit(text4, text4Rect)
            menuWindow.blit(text5, text5Rect)
            menuWindow.blit(maze1, (100, 100))
            menuWindow.blit(dashboard, (575, 275))
            pygame.draw.rect(menuWindow, colors.green, button2Rect, border_radius = 10)
            menuWindow.blit(button2Text, button2TextRect)
            pygame.draw.rect(menuWindow, colors.red, backButton2Rect, border_radius = 8)
            menuWindow.blit(backButton2Text, backButton2TextRect)

        if screen3:
            menuWindow.blit(text6, text6Rect)
            menuWindow.blit(text7, text7Rect)
            menuWindow.blit(text8, text8Rect)
            menuWindow.blit(text9, text9Rect)
            pygame.draw.rect(menuWindow, colors.green, button3Rect, border_radius = 10)
            menuWindow.blit(button3Text, button3TextRect)
            pygame.draw.rect(menuWindow, colors.red, backButton3Rect, border_radius = 8)
            menuWindow.blit(backButton3Text, backButton3TextRect)
        pygame.display.flip()

    return