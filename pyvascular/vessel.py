# Copyright (c) 2022  R. Tohid (@rtohid)
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from os import linesep
class Vessel:

    def __init__(self, idx: int, start: int, end: int, length: float, radius: float) -> None:
        self.idx = idx
        self.length = length
        self.start = start
        self.end = end
        self.radius = radius
        self.neighbors = list()
        self.nodes = list()

    def add_neighbor(self, indecies: list):
        self.neighbors.extend(indecies)
        
    def add_nodes(self, indecies: list):
        self.nodes.extend(indecies)
        
    def __str__(self):
        text = f"Vessel {self.idx}:" + linesep
        text = text + f"Start: {self.start}" + linesep
        text = text + f"End: {self.end}" + linesep
        text = text + f"Nodes: {self.nodes}" + linesep
        text = text + f"Length: {self.length}" + linesep
        text = text + f"Radius: {self.radius}" + linesep
        return text
