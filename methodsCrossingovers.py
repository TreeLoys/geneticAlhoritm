#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by treeloys at 06.04.22
"""

from abc import ABC, abstractmethod
import random
import copy

from gen import Gen

class BaseCrossingover(ABC):
    @abstractmethod
    def fit(self, hromo1, hromo2):
        pass


class OnePointCrossingover(BaseCrossingover):
    def fit(self, hromo1, hromo2):
        genIDForCrossovering = random.randint(0, len(hromo1.gens) - 1)
        genCrossover = hromo1.gens[genIDForCrossovering]

        # Точка скрещивания гена
        crossoverPoint = random.randint(0, len(genCrossover.binary) - 1)

        # Часть для hrome1 разры по точки скрещивания гена
        clotchBeforeHromo1 = hromo1.gens[genIDForCrossovering].binary[:crossoverPoint]
        clotchAfterHromo1 = hromo1.gens[genIDForCrossovering].binary[crossoverPoint:]
        # Част для hrome2 разры по точки скрещивания гена
        clotchBeforeHromo2 = hromo2.gens[genIDForCrossovering].binary[:crossoverPoint]
        clotchAfterHromo2 = hromo2.gens[genIDForCrossovering].binary[crossoverPoint:]

        # Собираем ген потомка
        childrenHomoGen1 = Gen()
        childrenHomoGen1.setBin(clotchBeforeHromo1 + clotchAfterHromo2)
        childrenHomoGen2 = Gen()
        childrenHomoGen2.setBin(clotchBeforeHromo2 + clotchAfterHromo1)

        # Отпочковываем гены
        childrenHomo1 = copy.deepcopy(hromo1)
        childrenHomo2 = copy.deepcopy(hromo2)

        # Встраиваем новый ген
        childrenHomo1.gens[genIDForCrossovering] = childrenHomoGen1
        childrenHomo2.gens[genIDForCrossovering] = childrenHomoGen2

        return [childrenHomo1, childrenHomo2]


class TwoPointCrossingover(BaseCrossingover):
    def fit(self, hromo1, hromo2):
        genIDForCrossovering = random.randint(0, len(hromo1.gens) - 1)
        genCrossover = hromo1.gens[genIDForCrossovering]

        # 2 Точки скрещивания гена
        crossoverPointOne = random.randint(0, len(genCrossover.binary) - 1)
        crossoverPointTwo = random.randint(0, len(genCrossover.binary) - 1)
        
        # Для нормализации позиции точек
        if (crossoverPointOne > crossoverPointTwo):
            c = crossoverPointTwo
            crossoverPointTwo = crossoverPointOne
            crossoverPointOne = c
            
        # Часть для hrome1 разры по точки скрещивания гена
        clotchCycleForHromo1 = hromo1.gens[genIDForCrossovering].binary[crossoverPointOne:crossoverPointTwo]
        clotchCycleForHromo2 = hromo2.gens[genIDForCrossovering].binary[crossoverPointOne:crossoverPointTwo]
        
        # Отпочковываем гены
        childrenHomo1 = copy.deepcopy(hromo1)
        childrenHomo2 = copy.deepcopy(hromo2)

        # Встраиваем двухточечный участок
        tmpGen = list(childrenHomo1.gens[genIDForCrossovering].binary)
        tmpGen[crossoverPointOne:crossoverPointTwo] = list(clotchCycleForHromo2)
        childrenHomo1.gens[genIDForCrossovering].setBin("".join(tmpGen))
        
        tmpGen = list(childrenHomo2.gens[genIDForCrossovering].binary)
        tmpGen[crossoverPointOne:crossoverPointTwo] = list(clotchCycleForHromo1)
        childrenHomo2.gens[genIDForCrossovering].setBin("".join(tmpGen))

        return [childrenHomo1, childrenHomo2]
        
        
class GenCrossovering(BaseCrossingover):
    def fit(self, hromo1, hromo2):
        genIDForCrossovering = random.randint(0, len(hromo1.gens) - 1)
        genHromo1 = copy.deepcopy(hromo1.gens[genIDForCrossovering])
        genHromo2 = copy.deepcopy(hromo2.gens[genIDForCrossovering])
        
        # Отпочковываем гены
        childrenHomo1 = copy.deepcopy(hromo1)
        childrenHomo2 = copy.deepcopy(hromo2)
        
        # Меняем гены местами
        childrenHomo2.gens[genIDForCrossovering] = genHromo1
        childrenHomo1.gens[genIDForCrossovering] = genHromo2

        return [childrenHomo1, childrenHomo2]
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        