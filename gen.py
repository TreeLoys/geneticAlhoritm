#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by treeloys at 06.04.22
"""
import struct

def bin2float(b):
    h = int(b, 2).to_bytes(8, byteorder="big")
    return struct.unpack('>d', h)[0]

def float2bin(f):
    [d] = struct.unpack(">Q", struct.pack(">d", f))
    return f'{d:064b}'

# Реализация гена
class Gen():
    def __init__(self):
        self.binary = None
        self.numerical = None

    def setFloat(self, floatNumber):
        self.binary = float2bin(floatNumber)
        self.numerical = floatNumber

    def setBin(self, binString):
        self.binary = binString
        self.numerical = bin2float(binString)