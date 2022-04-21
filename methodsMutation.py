# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 10:45:58 2022

@author: student410
"""
from abc import ABC, abstractmethod
import random
import copy


class BaseMutation(ABC):
    @abstractmethod
    def mutate(self, gen, r_min, r_max, indpb=0.01):
        pass
    
class SingleBitAbsoluteMutation(BaseMutation):
    """Инвертирует один любой из битов гена"""
    def mutate(self, gen, r_min, r_max, indpb=None):
        while True:
            tempGen = copy.deepcopy(gen)
            randomBit = random.randint(0, len(tempGen.binary)-1)
            mutatedBinaryList = list(tempGen.binary)
            if mutatedBinaryList[randomBit] == "1":
                mutatedBinaryList[randomBit] = "0"
            else:
                mutatedBinaryList[randomBit] = "1"
            tempGen.setBin("".join(mutatedBinaryList))
            # Ограничение мутации в среде (ограничение стреды)
            if ((tempGen.numerical > r_min) and (tempGen.numerical < r_max)):
                return tempGen
            
class InverisonBits(BaseMutation):
    """Инвертирует каждый бит в гене с вероятностью indpb"""
    def mutate(self, gen, r_min, r_max, indpb=0.01):
        while True:
            tempGen = copy.deepcopy(gen)
            tempBinaryGen = list(tempGen.binary)
            for indx in range(len(tempBinaryGen)):
                if random.random() < indpb:
                    tempBinaryGen[indx] = "0" if tempBinaryGen[indx] == "1" else "1"
            tempGen.setBin("".join(tempBinaryGen))
            if ((tempGen.numerical > r_min) and (tempGen.numerical < r_max)):
                return tempGen
        
class RandomBits(BaseMutation):
    """Случайным образом устанавливает каждый бит в гене с вероятностью indpb"""
    def mutate(self, gen, r_min, r_max, indpb=0.01):
        while True:
            tempGen = copy.deepcopy(gen)
            tempBinaryGen = list(tempGen.binary)
            
            for indx in range(len(tempBinaryGen)):
                if random.random() < indpb:
                    tempBinaryGen[indx] = str(random.randrange(0, 1))
                    
            tempGen.setBin("".join(tempBinaryGen))
            if ((tempGen.numerical > r_min) and (tempGen.numerical < r_max)):
                return tempGen
            
class FlipBit(BaseMutation):
    """Случайным образом меняет местами два бита"""
    def mutate(self, gen, r_min, r_max, indpb=None):
        while True:
            tempGen = copy.deepcopy(gen)
            tempBinaryGen = list(tempGen.binary)
            
            randomBitOne = random.randint(0, len(tempGen.binary)-1)
            randomBitTwo = random.randint(0, len(tempGen.binary)-1)
            
            tempValueBitOne = tempBinaryGen[randomBitOne]
            tempValueBitTwo = tempBinaryGen[randomBitTwo]
            
            tempBinaryGen[randomBitOne] = tempValueBitTwo
            tempBinaryGen[randomBitTwo] = tempValueBitOne
            
            tempGen.setBin("".join(tempBinaryGen))
            if ((tempGen.numerical > r_min) and (tempGen.numerical < r_max)):
                return tempGen















