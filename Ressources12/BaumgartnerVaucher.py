import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
import sys
import math
from random import randint

screen_x = 500
screen_y = 500

city_color = [10,10,200] # blue
city_radius = 3

font_color = [255,255,255] # white

class City:
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos

    def __str__(self):
        return self.name + ": " + str(self.pos[0]) + ", " + str(self.pos[1])

    def __eq__(self, other):
        return self.name == other.name and self.pos == other.pos

class Solution:
    def __init__(self):
        pass


problem = []
cpt = 0
collecting = True

def loadFile(path):
    file = open(path, 'r')
    for line in file:
        words = line.split()
        problem.append(City(words[0], (int(words[1]), int(words[2]))))

def draw(cities):
    screen.fill(font_color)
    for city in cities:
        pygame.draw.circle(screen,city_color,city.pos,city_radius)
    text = font.render("Nombre: %i" % len(cities), True, font_color)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()


def calculDistance(problem, index):
    if(len(problem) != len(index)):
        print("Les tableaux de villes et d'index ne font pas la même taille")
    else:
        distance = 0
        for i in index:
            ville1 = problem[i]
            if(i+1 == len(problem)):
                ville2 = problem[0]
            else:
                ville2 = problem[i+1]

            newDistance = math.sqrt(abs(ville1.pos[0] - ville2.pos[0])*abs(ville1.pos[0] - ville2.pos[0]) + abs(ville1.pos[1] - ville2.pos[1])*abs(ville1.pos[1] - ville2.pos[1]))
            distance += newDistance
            print("new distance: " + str(newDistance))

        print("distance parcourue: " + str(distance))

def mutate(index):

    print("avant")
    for i in index:
        print(str(i))

    i1 = 0
    i2 = 0
    while(i1 == i2):
        i1 = randint(0,len(index)-1)
        i2 = randint(0,len(index)-1)


    print("i1: " + str(i1))
    print("i2: " + str(i2))

    temp = index[i1]
    index[i1] = index[i2]
    index[i2] = temp


    print("après")
    for i in index:
        print(str(i))

    return index


if __name__ == '__main__':

    loadFile("data/pb005.txt")

    for city in problem:
        print(city)

    pygame.init()
    window = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption('Baumgartner-Vaucher')
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None,30)

    draw(problem)

    while collecting:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_RETURN:
                collecting = False
            elif event.type == MOUSEBUTTONDOWN:
                problem.append(City(cpt, pygame.mouse.get_pos()))
                cpt += 1
                draw(problem)


    screen.fill(font_color)
    pygame.draw.lines(screen,city_color,True,[city.pos for city in problem])
    text = font.render("Un chemin, pas le meilleur!", True, font_color)
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()


    index = []
    for i in range(len(problem)):
        index.append(i)

    calculDistance(problem, index)

    mutate(index)


    while True:
        event = pygame.event.wait()
        if event.type == KEYDOWN: break
