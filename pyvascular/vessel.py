# Copyright (c) 2022  R. Tohid (@rtohid)
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)


class Vessel:

    def __init__(self, idx: int, start: int, end: int, length: float) -> None:
        self.idx = idx
        self.lenght = length
        self.start = start
        self.end = end
        self.neighbors = list()

    def add_neighbor(self, indecies: list):
        self.neighbors.extend(indecies)
