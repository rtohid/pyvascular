

import numpy as np
from math import pi, exp

class Flow:
    
    def __init__(self, 
                 node1: int,
                 node2: int,
                 vessels: np.ndarray) -> None:
        self.node1 = node1
        self.node2 = node2
        self.vessels = vessels
        
    def get_conductance(self):
        
        def viscosity():
            diameter = 2 * self.vessels.radius * 1e3
            eta = 220 * exp(-1.3 * diameter) + 3.2 - 2.44 * exp(-0.06 * pow(diameter, .645))
            return 0.036 * eta
        
        mu = viscosity()
        #print(self.vessels.radius, self.vessels.length, mu)
        if mu == 0:
            return 0
        else:
            return pi * pow(self.vessels.radius, 4) / (8 * self.vessels.length * mu)
        
    def print_vessels(self):
        for v in self.vessels:
            print(v)