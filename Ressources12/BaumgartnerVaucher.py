import pygame

class City:
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos

    def __str__(self):
        return self.name + ": " + str(self.pos[0]) + ", " + str(self.pos[1])

    def __eq__(self, other):
        return self.name == other.name and self.pos == other.pos



problem = []

def loadFile(path):
    file = open(path, 'r')
    for line in file:
        words = line.split()
        problem.append(City(words[0], (words[1], words[2])))


if __name__ == '__main__':

    loadFile("data/pb005.txt")

    for city in problem:
        print(city)

    if(problem[0] == problem[0]):
        print("ok")

    if(problem[0] == problem[1]):
        print("pas ok")
