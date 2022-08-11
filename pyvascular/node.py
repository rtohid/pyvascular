# Copyright (c) 2022  R. Tohid (@rtohid)
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from os import linesep

class Coordinate:

    def __init__(self, x, y, z=0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return str((self.x, self.y, self.z))


class Node:

    def __init__(self, idx, coordinate) -> None:
        self.idx = idx
        self.coordinate = coordinate
        self.parents = list()
        self.children = list()
        self.vessels = list()

    def add_parent(self, idx):
        self.parents = idx + self.parents

    def add_child(self, idx):
        self.children = self.children + idx

    def add_in_vessel(self, idx):
        self.vessels = idx + self.vessels

    def add_out_vessel(self, idx):
        self.vessels = self.vessels + idx

    def __str__(self):
        text = f"Node {self.idx}:" + linesep
        text = text + f"Coordinate: {self.coordinate}" + linesep
        text = text + f"Parents: {self.parents}" + linesep
        text = text + f"Children: {self.children}" + linesep
        text = text + f"Vessels: {self.vessels}" + linesep
        return text