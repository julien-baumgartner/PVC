import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
import sys
import random
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
    def __init__(self, problem):
        self.problem = problem
        self.indices = [key for key, value in enumerate(problem)]

    def __iter__(self):
        for index in self.indices:
            yield self.problem[index]

    def mutation(self):
        i1 = 0
        i2 = 0
        while(i1 == i2):
            i1 = randint(0,len(self.indices)-1)
            i2 = randint(0,len(self.indices)-1)

        temp = self.indices[i1]
        self.indices[i1] = self.indices[i2]
        self.indices[i2] = temp

    def croisement(self, soluce2):
        i1 = 0
        i2 = 0

        #print(self.indices)
        #print(soluce2.indices)

        while(i1 == i2):
            i1 = randint(0,len(self.indices)-1)
            i2 = randint(i1,len(self.indices)-1)
        #print("i1:"+str(i1))
        #print("i2:"+str(i2))

        x2 = i1-1
        newIndices = [0 for i in range(len(self.indices))]
        for x1 in range(i1-1, i1 -1 - len(self.indices), -1):
            error = False
            #print(newIndices)
            for y in range(i1, i2+1):
                if(self.indices[x1] == soluce2.indices[y]):
                    error = True
            #print("x1:"+str(x1))
            if not error:
                newIndices[x2] = self.indices[x1]
                x2-=1

        for y in range(i1, i2 + 1):
            newIndices[y] = soluce2.indices[y]

        #print(newIndices)
        return newIndices


    def calculDistance(self):
        if(len(self.problem) != len(self.indices)):
            print("Les tableaux de villes et d'index ne font pas la même taille")
        else:
            distance = 0
            for i in self.indices:
                ville1 = self.problem[i]
                if(i+1 == len(self.problem)):
                    ville2 = self.problem[0]
                else:
                    ville2 = self.problem[i+1]

                newDistance = math.sqrt(abs(ville1.pos[0] - ville2.pos[0])*
                                        abs(ville1.pos[0] - ville2.pos[0]) +
                                        abs(ville1.pos[1] - ville2.pos[1])*
                                        abs(ville1.pos[1] - ville2.pos[1]))
                distance += newDistance
                print("new distance: " + str(newDistance))

            print("distance parcourue: " + str(distance))


def croisementRandom(soluces, n):
    newsoluces = []

    combinaison = set()
    while len(combinaison) < n:
        i1 = 0
        i2 = 0
        while(i1 == i2):
            i1 = randint(0,len(soluces)-1)
            i2 = randint(0,len(soluces)-1)

        combinaison.add((i1,i2))
    #print(combinaison)
    for (i1,i2) in combinaison:
        newsoluces.append(Solution(problem))

        newsoluces[-1].indices = soluces[i1].croisement(soluces[i2])

    return newsoluces
def croisementElitiste(soluces, n):
    newsoluces = []

    combinaison = set()
    while len(combinaison) < n:
        i1 = 0
        i2 = 0
        while(i1 == i2):
            i1 = randint(0,(len(soluces)+1)/2-1)
            i2 = randint(0,len(soluces)-1)

        combinaison.add((i1,i2))
    #print(combinaison)
    for (i1,i2) in combinaison:
        newsoluces.append(Solution(problem))

        newsoluces[-1].indices = soluces[i1].croisement(soluces[i2])

    return newsoluces


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

if __name__ == '__main__':

    #loadFile("data/pb005.txt")

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

    soluces = [ Solution(problem) for i in range(10)]


    while True:
        for soluce in soluces:
            soluce.mutation()

        soluces = croisementRandom(soluces, 10)
        event = pygame.event.wait()
        if event.type == KEYDOWN: break;

        screen.fill(font_color)
        pygame.draw.lines(screen,city_color,True,[city.pos for city in soluce])
        #print(soluce.indices)
        text = font.render("Un chemin, pas le meilleur!", True, font_color)
        textRect = text.get_rect()
        screen.blit(text, textRect)
        pygame.display.flip()
