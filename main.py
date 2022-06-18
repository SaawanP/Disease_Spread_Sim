from random import randint, random
import math
import pygame
import time as clock
import numpy as np
from matplotlib import pyplot as plt


start = 0
addition = 184
interest = 0.06
x = 0
previous = 0
for y in range(370):
    x = addition + previous + previous*(interest/12)
    previous = x

print(x)


# constant
StartN = 750  # Population size (less dots means faster simulation)
deathChance = 0.6
birthchance = 0.5
infectChance = 0.3
infectRange = 10
infectLength = 75
simRepeats = 1
simLength = 10
simPause = 0.05  # Decrease value to increase speed
graphStepSize = 10
reinfect = False

dotSize = 5
size = width, height = 400, 300
RED = [255, 0, 0]
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
GREEN = [0, 255, 0]


class TasmanianInd:
    def __init__(self, num):
        self.xPos = randint(20, width - 20)
        self.yPos = randint(20, height - 20)
        self.xVel = self.NewVel()
        self.yVel = self.NewVel()
        self.infected = False
        self.infectColor = RED
        self.num = num
        self.infectionTime = -1
        self.timesInfected = 0
        self.incubateTime = -1
        self

    def NewVel(self):
        return randint(-3, 3)

    def Move(self):
        if random() < 0.90:
            self.xPos += self.xVel
            self.yPos += self.yVel
        else:
            self.xVel = self.NewVel()
            self.yVel = self.NewVel()
            self.xPos += self.xVel
            self.yPos += self.yVel
        if self.xPos >= width:
            self.xPos = width
            self.xVel = -1 * self.xVel
        if self.xPos <= 0:
            self.xPos = 0
            self.xVel = -1 * self.xVel
        if self.yPos >= height:
            self.yPos = height
            self.yVel = -1 * self.yVel
        if self.yPos <= 0:
            self.yPos = 0
            self.yVel = -1 * self.yVel

    def CheckMove(self, newX, newY):
        if newX in range(0, width + 1) and newY in range(0, height + 1):
            return True
        return False

    def Infect(self, initialTime):
        if not self.infected and self.InfectClose() and random() < (infectChance / 2 ** self.timesInfected):
            self.infected = True
            self.infectColor = BLACK
            Infected.append(self.num)
            self.infectionTime = initialTime

    def GetDist(self, x1, x2, y1, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def InfectClose(self):
        for infect in Infected:
            if self.GetDist(self.xPos, Population[infect].xPos, self.yPos, Population[infect].yPos) <= infectRange:
                return True
        return False

    def Heal(self, currentTime):
        if self.infectionTime != -1:
            if currentTime - self.infectionTime == infectLength:
                if random() <= deathChance:
                    self.infectColor = WHITE
                elif reinfect:
                    self.infectColor = RED
                    self.infected = False
                else:
                    self.infectColor = GREEN
                    self.infectionTime = -1
                Infected.pop(0)


# Set up playing area
pygame.init()
screen = pygame.display.set_mode(size)
screen.fill(WHITE)
LeaveSim = False

for repeat in range(simRepeats):
    # Set up initial population
    N = StartN
    Population = [TasmanianInd(i) for i in range(N)]
    startInfect = randint(0, N - 1)
    Population[startInfect].infected = True
    Population[startInfect].infectColor = BLACK
    Population[startInfect].infectionTime = 0
    Infected = [startInfect]
    storeData = np.array([N, 1, 0, 0])
    time = 1
    count = 0
    loop = True

    while loop:
        susceptibleData = 0
        infectedData = 0
        deadData = 0
        recoverData = 0
        count += 1

        for ind in Population:
            if ind.infectColor != WHITE:
                pygame.draw.circle(screen, ind.infectColor, [ind.xPos, ind.yPos], dotSize)
                ind.Heal(count)
                ind.Move()
                ind.Infect(count)

        pygame.display.update()
        if count % graphStepSize == 0:
            for ind in Population:
                if ind.infectColor == RED:
                    susceptibleData += 1
                elif ind.infectColor == BLACK:
                    infectedData += 1
                elif ind.infectColor == WHITE:
                    deadData += 1
                elif ind.infectColor == GREEN:
                    recoverData += 1
            storeData = np.dstack((storeData, [susceptibleData, infectedData, deadData, recoverData]))
            time += 1
        if time == simLength + 1:
            loop = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                LeaveSim = True
                loop = False
        if deadData > N/2:
            clock.sleep(simPause+deadData)
        screen.fill(WHITE)

    if LeaveSim:
        break

    if repeat == 0:
        totalData = storeData
    else:
        for row in range(4):
            for col in range(time):
                totalData[0][row][col] = (storeData[0][row][col] + totalData[0][row][col] * repeat) / (repeat + 1)

if not LeaveSim:
    times = np.arange(0, 365, float(365)/len(totalData[0][0]))
    plt.plot(times, totalData[0][0], 'r', label='Susceptible')
    plt.plot(times, totalData[0][1], 'k', label='Infected')
    plt.plot(times, totalData[0][2], 'b', label='Dead')
    if not reinfect and deathChance != 1:
        plt.plot(times, totalData[0][3], 'g', label='Recovered')
    plt.ylabel('Number of Tasmanian Devils')
    plt.xlabel('Time')
    plt.title('Tasmanian Devil Facial Tumor Disease')
    plt.legend(loc='upper center', frameon=False)
    plt.show()

pygame.quit()
