# -*- coding: utf-8 -*-
#****************************
# унимодальная тестовая фунция
"""
- 10 кроссоверингов
- Анимация 
- Тестовые функции
"""
import numpy as np
from numpy import arange
from numpy import meshgrid
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D


import random
import copy

from randcolor import rand_cmap

from methodsCrossingovers import OnePointCrossingover
from testsFunctions import Spherical
from methodsMutation import SingleBitAbsoluteMutation
from gen import Gen


# Методы инициации генов
class GenInits():
    # Способ инициации - рандомный
    @staticmethod
    def random(gens, r_min, r_max):
        for gen in gens:
            valueGen = random.uniform(r_min, r_max)
            gen.setFloat(valueGen)


# Мутации
class Mutations():
    # Инвертировать рандомный бит в гене
    @staticmethod 
    def mutateRandomSingleByte(gen, r_min, r_max):
        while True:
            randomBit = random.randint(0, len(gen.binary)-1)
            mutatedBinaryList = list(gen.binary)
            if mutatedBinaryList[randomBit] == "1":
                mutatedBinaryList[randomBit] = "0"
            else:
                mutatedBinaryList[randomBit] = "1"
            gen.setBin("".join(mutatedBinaryList))
            # Ограничение мутации в среде (ограничение стреды)
            if ((gen.numerical > r_min) and (gen.numerical < r_max)):
                return gen
        
# Кроссинговер
class Crossingovers():
    @staticmethod
    def onePointCrossover(hromo1, hromo2):
        genIDForCrossovering = random.randint(0, len(hromo1.gens)-1)
        genCrossover = hromo1.gens[genIDForCrossovering]
        
        # Точка скрещивания гена
        crossoverPoint = random.randint(0, len(genCrossover.binary)-1)
        
        # Часть для hrome1 разры по точки скрещивания гена
        clotchBeforeHromo1 = hromo1.gens[genIDForCrossovering].binary[:crossoverPoint]
        clotchAfterHromo1 = hromo1.gens[genIDForCrossovering].binary[crossoverPoint:]
        # Част для hrome2 разры по точки скрещивания гена
        clotchBeforeHromo2 = hromo2.gens[genIDForCrossovering].binary[:crossoverPoint]
        clotchAfterHromo2 = hromo2.gens[genIDForCrossovering].binary[crossoverPoint:]

        # Собираем ген потомка
        childrenHomoGen1 = Gen()
        childrenHomoGen1.setBin(clotchBeforeHromo1+clotchAfterHromo2)
        childrenHomoGen2 = Gen()
        childrenHomoGen2.setBin(clotchBeforeHromo2+clotchAfterHromo1)
        
        # Отпочковываем гены
        childrenHomo1 = copy.deepcopy(hromo1)
        childrenHomo2 = copy.deepcopy(hromo2)
        
        # Встраиваем новый ген
        childrenHomo1.gens[genIDForCrossovering] = childrenHomoGen1
        childrenHomo2.gens[genIDForCrossovering] = childrenHomoGen2
        
        return [childrenHomo1, childrenHomo2]


# Реализация хромосомы (Она же индивид)
class Hromosome():
    def __init__(self, settings):
        self.settings = settings
        # Гены в хромосоме (2 гена на x и y)
        self.gens = [Gen(), Gen()]
        # Выбор метода инициации (Случайными значениями)
        GenInits.random(self.gens,
                        self.settings.testFunction.getMinX(),
                        self.settings.testFunction.getMaxX())
        self.fitnessValue = None
        self.fitness()
        
    def fitness(self):
        # Помещаем хромосому в среду, и смотрим что она там выдала
        self.fitnessValue = self.settings.testFunction.calculateZ(
            self.gens[0].numerical,
            self.gens[1].numerical)

    def mutation(self):
        # Случайно выбрать любой из доступных генов (в данном случае для 2ух 50%)
        # И произвести мутации
        chanseChoiseGen = random.randint(0, len(self.gens)-1)
        gen = self.gens[chanseChoiseGen]
        mutatedGen = self.settings.mutations.mutate(gen,
                                                    self.settings.testFunction.getMinX(),
                                                    self.settings.testFunction.getMaxX())
        self.gens[chanseChoiseGen] = mutatedGen
    
    
# Популяция
class Population():
    def __init__(self, settings):
        self.settings = settings
        self.populationSize = settings.populationSize
        self.populationMutationSize = 4
        self.populationCrossoveringSize = 4
        self.populationHromosome = [Hromosome(settings) for x in range(self.populationSize)]
        self.bestFitness = None
        self.colorScatter = np.random.rand(3,).reshape(1, -1)
    
    def selection(self):
        # Элитарная селекция
        self.populationHromosome.sort(key=lambda x: x.fitnessValue)

    def era(self):
        # Сортировка (она же выбор по лучшим хромосомам)
        self.populationHromosome.sort(key=lambda x: x.fitnessValue)
        self.bestFitness = self.populationHromosome[0].fitnessValue
        
        
        print("BestFitness " + 
              " X: " + str(self.populationHromosome[0].gens[0].numerical) + 
              " Y: " + str(self.populationHromosome[0].gens[1].numerical) +
              " Z: " + str(self.populationHromosome[0].fitnessValue)
              )
        
        #print("BestFitnesBinaryX: " + self.populationHromosome[0].gens[0].binary)
        #print("BestFitnesBinaryY: " + self.populationHromosome[0].gens[1].binary)
        print("LastFitness " + 
              " X: " + str(self.populationHromosome[-1].gens[0].numerical) + 
              " Y: " + str(self.populationHromosome[-1].gens[1].numerical) +
              " Z: " + str(self.populationHromosome[-1].fitnessValue))
        
        
        ########### Мутация
        # Отпочковываем лучших представителей для мутации
        childrensForMutation = copy.deepcopy(self.populationHromosome[:self.populationMutationSize])
        # Выполняем мутации к отнаследованому поколению
        for h in childrensForMutation:
            h.mutation()
        
        
        ########## Кросоверинг
        # Отпочковываем лучших представителей для Кросоверинга
        parrentsForCrossovering = copy.deepcopy(self.populationHromosome[:self.populationCrossoveringSize])
        childrensForCrossovering = []
        for hi in range(0, len(parrentsForCrossovering), 2):
            hromo1 = parrentsForCrossovering[hi]
            hromo2 = parrentsForCrossovering[hi+1]
            crossingoveredChildrens = self.settings.crossovering.fit(hromo1, hromo2)
            childrensForCrossovering += crossingoveredChildrens
        
        # Помещаем в среду наши хромосомы
        childrens = childrensForMutation + childrensForCrossovering
        for h in childrens:
            h.fitness()
       
        # Добавляем их в общую популяцию, сортируем по элитарности, и самых бесполезных удаляем
        self.populationHromosome += childrens
        self.populationHromosome.sort(key=lambda x: x.fitnessValue)
        self.populationHromosome = self.populationHromosome[:-len(childrens)]
            
        #self.selection()
        # Добавить мутации
        # Добавить кросинговер

    def getTopHromoXYPoints(self, size=10):
        X = []
        Y = []
        F = []
        for i in range(len(self.populationHromosome)):
            X.append(self.populationHromosome[i].gens[0].numerical)
            Y.append(self.populationHromosome[i].gens[1].numerical)
            F.append(self.populationHromosome[i].fitnessValue)
        return {"x":X, "y":Y, "fitness":F}


# Миграция особей меж популяций
class Migration():
    def __init__(self):
        self.migrateEra = 4

    # миграция по топологии полной сети
    def migrate(self, era, populations):
        # Каждую 4ртую эпоху
        if (era % self.migrateEra) == 0:
            for population in populations:
                iPopulationToMigrate = random.randint(0, len(populations)-1)
                h = copy.deepcopy(population.populationHromosome[0])
                populations[iPopulationToMigrate].populationHromosome[-1] = h


class Evolution():
    def __init__(self, settings):
        self.settings = settings
        self.iteration = settings.iteration
        self.populations = [Population(settings) for x in range(settings.underpopulationSize)]
        self.bestHromoByStep = []
        self.fig = None
        self.bestFitness = []
        self.migration = Migration()

        
    def plotIt(self, era, bestFitness):
        figure = pyplot.figure(figsize=(8, 8))
        ax = figure.add_subplot(111)
        ax.plot(era, bestFitness)
        # axis.plot_wireframe(x, y, results)
        #pyplot.show()
        
    def run(self):
        era = []
        for i in range(self.iteration):
            self.bestFitness.append([])
            self.bestHromoByStep.append([])
            era.append([])
            self.migration.migrate(i, self.populations)
            for iPopulation, population in enumerate(self.populations):
                print("#####################")
                print(f"Underpopulation: {iPopulation}")
                print(f"Evolution era: {i}")
                population.era()
                era[i].append(iPopulation)
                self.bestFitness[i].append(population.bestFitness)
                self.bestHromoByStep[i].append(population.getTopHromoXYPoints(100))

        # self.plotIt(era, bestFitness)
        # self.plotIt(era[:10], bestFitness[:10])
        self.getBestHromoPoint()

    def drawInitArea(self):
        # Построения графика
        xaxis = arange(self.settings.testFunction.getMinX(),
                       self.settings.testFunction.getMaxX(), 0.1)
        yaxis = arange(self.settings.testFunction.getMinY(),
                       self.settings.testFunction.getMaxY(), 0.1)
        x, y = meshgrid(xaxis, yaxis)
        results = self.settings.testFunction.calculateZ(x, y)
        figure = pyplot.figure(figsize=(8, 7))
        axis = figure.gca(projection='3d')

        axis.plot_surface(x, y, results, cmap='jet')
        # axis.plot_wireframe(x, y, results)
        #pyplot.show()
        return figure

    def drawHromoByStep(self, step):
        # Построение 2D вида
        pyplot.cla()
        if self.fig:
            pyplot.close(self.fig)
        self.fig = pyplot.figure(figsize=(8, 7))
        left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
        ax = self.fig.add_axes([left, bottom, width, height])
        ax.set_title("2D Пространство")

        xaxis = arange(self.settings.testFunction.getMinX(),
                       self.settings.testFunction.getMaxX(), 0.1)
        yaxis = arange(self.settings.testFunction.getMinY(),
                       self.settings.testFunction.getMaxY(), 0.1)
        x, y = meshgrid(xaxis, yaxis)
        results = self.settings.testFunction.calculateZ(x, y)
        if self.settings.testFunction.getLevels() > 0:
            cp = pyplot.contourf(x, y, results, levels=np.linspace(0,
                                                                   self.settings.testFunction.getLevels(),
                                                                   50))
        else:
            cp = pyplot.contourf(x, y, results, levels=np.linspace(self.settings.testFunction.getLevels(),
                                                                   0,
                                                                   50))
        pyplot.colorbar(cp)

        # Построение различных популяций
        if step < len(self.bestHromoByStep):
            for i,  population in enumerate(self.bestHromoByStep[step]):
                pyplot.scatter(population["x"], population["y"],
                               s=1, c=self.populations[i].colorScatter
                               )
        return self.fig

    def getBestHromoPoint(self):
        bestHromos = []
        for i, p in enumerate(self.populations):
            for ph in p.populationHromosome:
                h = {
                        "underpopoulation": i,
                        "X":ph.gens[0].numerical,
                        "Y":ph.gens[1].numerical,
                        "fitness":ph.fitnessValue
                    }
                bestHromos.append(h)
        bestHromos.sort(key=lambda x: x["fitness"])
        print(f"Лучшая хромосома. Результат: {bestHromos[0]['fitness']} Популяция: {bestHromos[0]['underpopoulation']+1} X: {bestHromos[0]['X']} Y: {bestHromos[0]['Y']}")
        return bestHromos


if __name__ == "__main__":
    class Settings():
        def __init__(self):
            self.testFunction = Spherical()
            self.crossovering = OnePointCrossingover()
            self.mutations = SingleBitAbsoluteMutation()
            self.populationSize = 100
            self.iteration = 80
            self.underpopulationSize = 3
    s = Settings()
    e = Evolution(s)
    e.run()
