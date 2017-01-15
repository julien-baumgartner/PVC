import pygame
from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
import sys
import random
import math
from random import randint
import datetime
import argparse


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

    def mutation(self, ratio):
        nbMutation = (int)(len(self.indices)*ratio)
        if nbMutation == 0:
            nbMutation = 1
        for i in range(nbMutation):
            i1 = 0
            i2 = 0
            while(i1 == i2):
                i1 = randint(0,len(self.indices)-1)
                i2 = randint(0,len(self.indices)-1)


            newIndices = list(self.indices)
            temp = newIndices[i1]
            newIndices[i1] = newIndices[i2]
            newIndices[i2] = temp

        return newIndices

    def croisement(self, soluce2):
        i1 = 0
        i2 = 0

        while(i1 == i2):
            i1 = randint(0,len(self.indices)-1)
            i2 = randint(i1,len(self.indices)-1)

        x2 = i1-1
        newIndices = [0 for i in range(len(self.indices))]
        for x1 in range(i1-1, i1 -1 - len(self.indices), -1):
            error = False

            for y in range(i1, i2+1):
                if(self.indices[x1] == soluce2.indices[y]):
                    error = True

            if not error:
                newIndices[x2] = self.indices[x1]
                x2-=1

        for y in range(i1, i2 + 1):
            newIndices[y] = soluce2.indices[y]

        return newIndices


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

    for (i1,i2) in combinaison:
        newsoluces.append(Solution(problem))

        newsoluces[-1].indices = soluces[i1].croisement(soluces[i2])

    return newsoluces

def loadFile(file):
    # file = open(path, 'r')
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
    del problem[:]
    if(file):
        loadFile(file)
        if(gui):
            draw(problem)
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


    solutions = []
    nbSolutions = (int)(10000/len(problem))
    selection = (int)(nbSolutions / 3)

    for i in range(nbSolutions):
        solutions.append(Solution(problem))

    if(maxtime > 0):
        maxtime -= 0.2
        start = datetime.datetime.now()
        seconds = 0;

        while(seconds < maxtime):
            solutions = sorted(solutions, key=lambda solution: solution.calculDistance(), reverse=False)
            solutions = solutions[:selection]
            solutions.extend(croisementRandom(solutions, nbSolutions-selection))
            for i in range(nbSolutions):
                solutions.append(Solution(problem))
                solutions[-1].indices = solutions[i].mutation(seconds/maxtime)
            if(gui):
                screen.fill(font_color)
                pygame.draw.lines(screen,city_color,True,[city.pos for city in solutions[0]])
                #print(solutions[0].calculDistance())
                text = font.render("Un chemin, pas le meilleur!", True, font_color)
                textRect = text.get_rect()
                screen.blit(text, textRect)
                pygame.display.flip()
            seconds = (datetime.datetime.now() - start).total_seconds()

        bestSoluce = findBestSolution(solutions)
    else:
        nbIdenticalSolutions = 0
        oldBestDistance = -1
        while(nbIdenticalSolutions < 10):
        #for _ in range(10):
            # print(nbIdenticalSolutions)
            # print(oldBestDistance)
            solutions = sorted(solutions, key=lambda solution: solution.calculDistance(), reverse=False)
            solutions = solutions[:selection]
            solutions.extend(croisementRandom(solutions, nbSolutions-selection))
            for i in range(nbSolutions):
                solutions.append(Solution(problem))
                solutions[-1].indices = solutions[i].mutation(len(problem)/10+nbIdenticalSolutions*2)
            if(gui):
                screen.fill(font_color)
                pygame.draw.lines(screen,city_color,True,[city.pos for city in solutions[0]])
                #print(solutions[0].calculDistance())
                text = font.render("Un chemin, pas le meilleur!", True, font_color)
                textRect = text.get_rect()
                screen.blit(text, textRect)
                pygame.display.flip()
            if(oldBestDistance == -1 or solutions[0].calculDistance() < oldBestDistance ):
                nbIdenticalSolutions = 0
                oldBestDistance = solutions[0].calculDistance()
            else:
                nbIdenticalSolutions = nbIdenticalSolutions + 1

        bestSoluce = findBestSolution(solutions)
    if(gui):
        pygame.display.flip()

    listVilles = []
    for i in bestSoluce.indices:
        listVilles.append(problem[i].name)

    return bestSoluce.calculDistance(), listVilles

def sortSolutions(solutions):
    solutions = sorted(solutions, key=lambda soluce: soluce.calculDistance(), reverse = False)
    return solutions


def findBestSolution(solutions):
    solutions = sortSolutions(solutions)


    return solutions[0]


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--nogui", action="store_false", help="disable the gui")
    parser.add_argument("--maxtime", type=float, default=0.0, help="time max before return a solution")
    parser.add_argument("filename", nargs='?', default=None, type=argparse.FileType('r'), help="name of the file that contain the cities")
    args = parser.parse_args()

    nbSolutions = 300
    selection = 100
    problem = []
    cpt = 0

    if(args.nogui):
        pygame.init()
        window = pygame.display.set_mode((screen_x, screen_y))
        pygame.display.set_caption('Baumgartner-Vaucher')
        font = pygame.font.Font(None,30)
        screen = pygame.display.get_surface()
    #ga_solve(None, True, 10)
    ga_solve(args.filename, args.nogui, args.maxtime)
