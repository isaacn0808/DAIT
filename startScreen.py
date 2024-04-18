import pygame
import fonts
import colors
from menus import runThruMenus




# 0 is left, 1 is right, 2 is top, 3 is bottom
def drawBoxAround(screen, rect, thickness, colorFunc = lambda x: (0, 0, 0)):
    rectLeft = (rect.left - thickness, rect.top - thickness, thickness, rect.h + 2 * thickness)
    rectRight = (rect.right, rect.top - thickness, thickness, rect.h + 2 * thickness)
    rectTop = (rect.left - thickness, rect.top - thickness, rect.w + 2 * thickness, thickness)
    rectBottom = (rect.left - thickness, rect.bottom, rect.w + 2 * thickness, thickness)
    pygame.draw.rect(screen, colorFunc(0), rectLeft)
    pygame.draw.rect(screen, colorFunc(1), rectRight)
    pygame.draw.rect(screen, colorFunc(2), rectTop)
    pygame.draw.rect(screen, colorFunc(3), rectBottom)

def start(screen):
    selectStates = [False, False, False]
    class RadioButton:
        CURVATURE = 0.05
        def __init__(self, rect, color1, color2, id):
            self.rect = rect
            self.color1 = color1
            self.color2 = color2
            self.id = id

        def draw(self):
            if selectStates[self.id]:
                pygame.draw.rect(screen, self.color2, self.rect, border_radius = int(self.rect.w * self.CURVATURE))
            else:
                pygame.draw.rect(screen, self.color1, self.rect, border_radius = int(self.rect.w * self.CURVATURE))
    pygame.init()
    running = True
    # text input bars
    inputRect1 = pygame.Rect(366, 236, 563, 40)
    inputRect2 = pygame.Rect(366, 339, 100, 40)
    activeBar = 0
    firstNameField = ""
    lastNameField = ""
    gradeField = ""
    rects = [inputRect1, inputRect2]
    fields = [firstNameField, lastNameField, gradeField]

    # text surfaces
    titleText = fonts.jejuhal70.render("Genie the Explorer", True, colors.blond)
    titleTextRect = pygame.Rect(352, 33, 771, 92)
    subtitleText = fonts.kulim30.render("A Reinforcement Learning AI minigame", True, colors.blond2)
    subtitleTextRect = pygame.Rect(404, 114, 575, 53)
    barTitleText1 = fonts.barlow30.render("First Name:", True, colors.lightBlue)
    barTitleText1Rect = pygame.Rect(167, 226, 173, 59)
    barTitleText2 = fonts.barlow30.render("Last Initial:", True, colors.lightBlue)
    barTitleText2Rect = pygame.Rect(168, 333, 143, 53)
    barTitleText3 = fonts.barlow30.render("Grade:", True, colors.lightBlue)
    barTitleText3Rect = pygame.Rect(168, 440, 80, 50)
    optionText1 = fonts.barlow30.render("6", True, "black")
    optionText2 = fonts.barlow30.render("7", True, "black")
    optionText3 = fonts.barlow30.render("8", True, "black")
    optionText1Rect = pygame.Rect((350, 447, 50, 50))
    optionText2Rect = pygame.Rect((500, 447, 50, 50))
    optionText3Rect = pygame.Rect((650, 447, 50, 50))
    loginText = fonts.barlow30.render("Login", True, "white")
    loginTextRect = pygame.Rect(604, 570, 99, 57)
    loginButtonRect = pygame.Rect(583, 551, 119, 77)
    loginButtonColor = colors.green
    loginPressed = False

    radiobuttons = []
    radiobuttons.append(RadioButton(pygame.Rect(380, 440, 50, 50), colors.gray, colors.green, 0))
    radiobuttons.append(RadioButton(pygame.Rect(530, 440, 50, 50), colors.gray, colors.green, 1))
    radiobuttons.append(RadioButton(pygame.Rect(680, 440, 50, 50), colors.gray, colors.green, 2))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if inputRect1.collidepoint(event.pos):
                    activeBar = 1
                elif inputRect2.collidepoint(event.pos):
                    activeBar = 2
                elif loginButtonRect.collidepoint(event.pos):
                    loginButtonColor = colors.darkGreen
                    loginPressed = True
                for button in radiobuttons:
                    if button.rect.collidepoint(event.pos):
                        activeBar = 0
                        for i in range(len(selectStates)):
                            selectStates[i] = True if i == button.id else False
                        break
            if event.type == pygame.MOUSEBUTTONUP:
                if loginPressed:
                    if selectStates == [False, False, False]:
                        pass
                    else:
                        for i in range(len(selectStates)):
                            if selectStates[i]:
                                fields[2] = str(i + 6)
                    loginPressed = False
                    loginButtonColor = colors.green
                    running = False
            if event.type == pygame.KEYDOWN:
                if (activeBar > 0):
                    if event.key == 8 and len(fields[activeBar - 1]) > 0:
                        fields[activeBar - 1] = fields[activeBar - 1][:-1]
                    elif event.key != 8:
                        try:
                            fields[activeBar - 1] += chr(event.key)
                        except ValueError:
                            continue
                
        # make background
        screen.fill(colors.bgBlue)
        # Add all text
        for button in radiobuttons:
            button.draw()
        screen.blit(titleText, titleTextRect)
        screen.blit(subtitleText, subtitleTextRect)
        screen.blit(barTitleText1, barTitleText1Rect)
        screen.blit(barTitleText2, barTitleText2Rect)
        screen.blit(barTitleText3, barTitleText3Rect)
        screen.blit(optionText1, optionText1Rect)
        screen.blit(optionText2, optionText2Rect)
        screen.blit(optionText3, optionText3Rect)
        # Add input bars
        pygame.draw.rect(screen, colors.gray, inputRect1)
        pygame.draw.rect(screen, colors.gray, inputRect2)
        if(activeBar > 0):
            drawBoxAround(screen, rects[activeBar - 1], 3)
        # Draw field text
        fieldText1 = fonts.barlow30.render(fields[0], True, (0, 0, 0))
        screen.blit(fieldText1, inputRect1)
        fieldText2 = fonts.barlow30.render(fields[1], True, (0, 0, 0))
        screen.blit(fieldText2, inputRect2)
        # Add login button 
        pygame.draw.rect(screen, loginButtonColor, loginButtonRect, border_radius = 10)
        screen.blit(loginText, loginTextRect)
        pygame.display.flip()
    return fields[0], fields[1], fields[2]