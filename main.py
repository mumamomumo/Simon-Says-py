import pygame
from pygame.locals import *
import time
import random

pygame.init()

WID = 800
HEI = 800

WIN = pygame.display.set_mode((WID, HEI))
pygame.display.set_caption("Simon Says")
font = pygame.font.SysFont('Arial', 50)

colors = [
    'red',
    'blue',
    'green',
    'yellow'
]
order = []

green = pygame.Rect(0, 0, 300, 300)
red = pygame.Rect(500, 0, 300, 300)
blue = pygame.Rect(500, 500, 300, 300)
yellow = pygame.Rect(0, 500, 300, 300)


class Button:
    """Create clickOrderbutton, then blit the surface in the while loop"""

    def __init__(self, text: str,  pos: tuple, font: int, bg="gray"):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        self.clicked = False
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(
            self.x-5, self.y-5, self.size[0]+5, self.size[1]+5)

    def do(self):
        WIN.fill(0)
        self.clicked = True

    def show(self):
        if self.clicked == False:
            WIN.blit(self.surface, self.rect)

    def hide(self):
        self.text = False

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.do()


startButton = Button("Start", (WID//2, HEI//2), 50)


def draw():
    pygame.draw.rect(WIN, (50, 255, 50), green)
    pygame.draw.rect(WIN, (255, 50, 50), red)
    pygame.draw.rect(WIN, (50, 50, 255), blue)
    pygame.draw.rect(WIN, (255, 255, 51), yellow)


class mainMenu:
    def __init__(self):
        self.in_main = True
        self.startbutton = Button("Start", (400, 400), 50)
        self.i = 0

    def startButton(self, event):
        draw()
        WIN.fill((255, 255, 255), (400, 400, 50, 50))
        if self.startbutton.clicked == False:
            startButton.show()
            if self.in_main:
                self.startbutton.click(event)
            else:
                self.startbutton.clicked = False
        else:
            self.in_main = False


mainmenu = mainMenu()


clickOrder = []


def click(event):
    global clickOrder
    x, y = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if pygame.mouse.get_pressed()[0:1]:
            if green.collidepoint(x, y):
                clickOrder.append('green')
            elif red.collidepoint(x, y):
                clickOrder.append('red')
            elif blue.collidepoint(x, y):
                clickOrder.append('blue')
            elif yellow.collidepoint(x, y):
                clickOrder.append('yellow')


def light_green():
    pygame.draw.rect(WIN, (150, 255, 150), green)
    pygame.display.update()
    time.sleep(1)
    pygame.draw.rect(WIN, (50, 255, 50), green)
    pygame.display.update()
    time.sleep(1)


def light_red():
    pygame.draw.rect(WIN, (255, 150, 150), red)
    pygame.display.update()
    time.sleep(1)
    pygame.draw.rect(WIN, (255, 50, 50), red)
    pygame.display.update()
    time.sleep(1)


def light_blue():
    pygame.draw.rect(WIN, (150, 150, 255), blue)
    pygame.display.update()
    time.sleep(1)
    pygame.draw.rect(WIN, (50, 50, 255), blue)
    pygame.display.update()
    time.sleep(1)


def light_yellow():
    pygame.draw.rect(WIN, (255, 255, 150), yellow)
    pygame.display.update()
    time.sleep(1)
    pygame.draw.rect(WIN, (255, 255, 50), yellow)
    pygame.display.update()
    time.sleep(1)


def scoretext(score):
    text = font.render(f'Score: {score}', False, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (WID//2, HEI//2)
    WIN.blit(text, textRect)


def wrong():
    WIN.fill(0)

    text = font.render("Wrong color. Restarting game", True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (WID//2, HEI//5)
    WIN.blit(text, textRect)
    pygame.display.update()
    mainmenu.in_main = True
    mainmenu.startbutton.clicked = False
    time.sleep(3)
    WIN.fill(0)


def correct():
    WIN.blit(font.render("Correct", False, (255, 255, 255)), (100, 400))


def main():
    clock = pygame.time.Clock()
    run = 1
    gamestate = 'choose'
    score = 0
    global clickOrder
    global order
    while run:
        clock.tick(30)
        if not (mainmenu.in_main):
            # game

            if gamestate == 'choose':
                print('choose')
                order.append(random.choice(colors))
                gamestate = 'light'
                scoretext(score)
            elif gamestate == 'light':
                WIN.fill((0, 0, 0))
                print('light')
                draw()
                scoretext(score)
                pygame.display.update()
                time.sleep(2)

                for i in order:
                    eval(f'light_{i}()')
                gamestate = 'click'
            elif gamestate == 'click':
                WIN.fill((55, 150, 155))
                scoretext(score)
                if order[:len(clickOrder)] == clickOrderand len(clickOrder):
                    correct()
                elif len(clickOrder) > 0:
                    wrong()
                    gamestate = 'choose'
                    order = []
                    score = -1
                    clickOrder = []
                if order == clickOrder:
                    gamestate = 'choose'
                    score += 1
                    print('done')
                    clickOrder = []
            draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if not (mainmenu.in_main):
                if gamestate == 'click':
                    click(event)
            else:
                mainmenu.startButton(event)

        pygame.display.update()


if __name__ == "__main__":
    main()
    pygame.quit()
