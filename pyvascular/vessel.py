# Copyright (c) 2022  R. Tohid (@rtohid)
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from os import linesep
from math import pi, exp

# class to describe Vessel data
# takes input parameters for each vessel:
#       index, start coordinate, end coordinate, length, and radius 
class Vessel:

    # constructor: initializes attributes when object is created from class 
    def __init__(self, idx: int, start: int, end: int, length: float, radius: float) -> None:
        self.idx = idx
        self.length = length
        self.start = start
        self.end = end
        self.radius = radius
        self.neighbors = list()
        self.nodes = list()
        
    # method: add connected vessels to list
    def add_neighbor(self, indecies: list):
        self.neighbors.extend(indecies)
        
    # method: add start and end node to list
    def add_nodes(self, indecies: list):
        self.nodes.extend(indecies)
       
    # method: return the conductance of the vessel 
    def get_conductance(self):
        def viscosity():
            diameter = 2 * self.radius * 1e3
            eta = 220 * exp(-1.3 * diameter) + 3.2 - 2.44 * exp(-0.06 * pow(diameter, .645))
            return 0.036 * eta
        mu = viscosity()
        if mu == 0:
            return 0
        else:
            return pi * pow(self.radius, 4) / (8 * self.length * mu)
     
    # descriptor: represents class objects as a string
    # to be used as checkpoint verification    
    def __str__(self):
        text = f"Vessel {self.idx}:" + linesep
        text = text + f"Start: {self.start}" + linesep
        text = text + f"End: {self.end}" + linesep
        text = text + f"Nodes: {self.nodes}" + linesep
        text = text + f"Length: {self.length}" + linesep
        text = text + f"Radius: {self.radius}" + linesep
        return text
