import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
import sys
import random
import math
from random import randint
import datetime


screen_x = 500
screen_y = 500
pygame.init()
window = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption('Baumgartner-Vaucher')
font = pygame.font.Font(None,30)
screen = pygame.display.get_surface()

city_color = [10,10,200] # blue
city_radius = 3

font_color = [255,255,255] # white

nbSolutions = 10

class City:
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos

    def __str__(self):
        return self.name + ": " + str(self.pos[0]) + ", " + str(self.pos[1])

    def __eq__(self, other):
        return self.name == other.name and self.pos == other.pos

class Solution:
    def __init__(self, problem, indices = None):
        self.problem = problem
        if(indices):
            self.indices = indices
        else:
            self.indices = [key for key, value in enumerate(problem)]
            random.shuffle(self.indices)

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


    def calculDistance(self):
        if(len(self.problem) != len(self.indices)):
            print("Les tableaux de villes et d'index ne font pas la même taille")
        else:
            distance = 0
            for i in range(len(self.indices)):
                ville1 = self.problem[self.indices[i]]
                if(i+1 == len(self.problem)):
                    ville2 = self.problem[self.indices[0]]
                else:
                    ville2 = self.problem[self.indices[i+1]]

                newDistance = math.sqrt(abs(ville1.pos[0] - ville2.pos[0])**2+
                                        abs(ville1.pos[1] - ville2.pos[1])**2)
                distance += newDistance

        return distance


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



def ga_solve(file=None, gui=True, maxtime=0):

    if(file):
        loadFile(file)
    else:
        draw(problem)

        collecting = True
        while collecting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN and event.key == K_RETURN:
                    collecting = False
                elif event.type == MOUSEBUTTONDOWN:
                    problem.append(City(cpt, pygame.mouse.get_pos()))
                    draw(problem)

    if(maxtime > 0):
        start = datetime.datetime.now()
        seconds = 0;
        solutions = []

        for i in range(nbSolutions):
            solutions.append(Solution(problem))

        #while(seconds < maxtime):
        #    seconds = (datetime.datetime.now() - start).total_seconds()


        bestSoluce = findBestSolution(solutions)
        print(bestSoluce.calculDistance())

        if(file==None):

            screen.fill(font_color)
            pygame.draw.lines(screen,city_color,True,[city.pos for city in bestSoluce])
            print(bestSoluce.indices)
            text = font.render("Un chemin, pas le meilleur!", True, font_color)
            textRect = text.get_rect()
            screen.blit(text, textRect)
            pygame.display.flip()

            while True:
                event = pygame.event.wait()
                if event.type == KEYDOWN: break;

def sortSolutions(solutions):
    solutions = sorted(solutions, key=lambda soluce: soluce.calculDistance(), reverse = False)
    return solutions


def findBestSolution(solutions):
    #distanceMin = 999999999
    #bestSolution = None
    #for soluce in solutions:
    #    distance = soluce.calculDistance()
    #    if(distance < distanceMin):
    #        distanceMin = distance
    #        bestSolution = soluce
    solutions = sortSolutions(solutions)


    return solutions[0]


if __name__ == '__main__':

    ga_solve(None, True, 3)
    #ga_solve("data/pb005.txt", True, 3)
