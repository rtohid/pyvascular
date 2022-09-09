# Copyright (c) 2022  R. Tohid (@rtohid)
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

import numpy as np
from math import pi, cos, sin

from pyvascular.vessel import Vessel
from pyvascular.node import Coordinate

default_config = {
    "min_vessel_length": 0.055,
    "min_vessel_radius": 0.0025,
    "length_scaling_factor": 0.8,
    "initial_bifurcation_angle": 70,
    "bifurcation_scaling_factor": 0.6,
    "radius_scaling_factor": 0.793700525984100
}


# class to describe and build the vessel network
# methods create arteries and veins stored as Vessel class objects in vessels ndarray
# input parameters:
#           num_levels (generations), num_dimensions, num_ranks (if parallel), config (default unless specified)
class Network:

    # constructor: initializes attributes when object is created from class 
    def __init__(self,
                 num_levels: int,
                 num_dimensions: int,
                 num_ranks: int = 1,
                 config=default_config) -> None:
        self.num_ranks = num_ranks
        self.num_levels = num_levels
        self.num_dimensions = num_dimensions
        self.config = config
        self.set_properties()

    # method: generate arterial tree
    def generate_artery(self):

        # sub-method: generate the root artery (Vessel 0) at negative maximum x displacement
        def generate_root(x_projection, y_projection):
            x_extent = self.max_vessel_length
            bsf = self.config["bifurcation_scaling_factor"]
            iba = self.config["initial_bifurcation_angle"]
            lsf = self.config["length_scaling_factor"]
            for i in range(1, self.num_levels):

                bifurcation_angle = iba * pow(bsf, i)
                length_factor = pow(lsf, i)

                x_extent = x_extent + self.max_vessel_length * length_factor * cos(
                    pi * bifurcation_angle / 180)
                
            x_1 = -x_extent + x_projection
            y_1 = y_projection
            
            self.vessels[0] = Vessel(0, Coordinate(-x_extent,0,0), Coordinate(x_1, y_1, 0), self.max_vessel_length, self.max_vessel_radius)
            self.vessels[0].add_nodes([0, 1])

        # sub-method: fractally generates arterial bodies for each parent vessel, starting at root
        #               - each call creates 2 daughter vessels starting from parent vessel (from previous level)
        #               - body: structure containing all progeny vessels of root vessel
        #               - sub-body: structure consisting of the 2 daughter vessels of each parent
        def generate_body(level, x_projection, y_projection, length, radius):
            for node in range(pow(2, level - 1), pow(2, level)):  # parallel
                child1_idx = node * 2 - 1
                child2_idx = node * 2
                child1_x = self.vessels[node-1].end.x + x_projection
                child1_y = self.vessels[node-1].end.y + y_projection
                child2_x = self.vessels[node-1].end.x + x_projection
                child2_y = self.vessels[node-1].end.y - y_projection
                
                self.vessels[child1_idx] = Vessel(child1_idx, self.vessels[node-1].end, Coordinate(child1_x,child1_y,0), length, radius)
                self.vessels[child1_idx].add_nodes([node, child2_idx])
                self.vessels[child2_idx] = Vessel(child2_idx, self.vessels[node-1].end, Coordinate(child2_x,child2_y,0), length, radius)
                self.vessels[child2_idx].add_nodes([node, child2_idx+1])

        # generate root artery with specified projections
        generate_root(self.max_vessel_length, 0)

        # loop to calculate x and y projections for each artery sub-body, with scaled parameters
        # calls generate_body() method with
        for level in range(1, self.num_levels):
            lsf = self.config["length_scaling_factor"]
            iba = self.config["initial_bifurcation_angle"]
            bsf = self.config["bifurcation_scaling_factor"]
            rsf = self.config["radius_scaling_factor"]

            length = self.max_vessel_length * pow(lsf, level)
            radius = self.max_vessel_radius * pow(rsf, level)
            bifurcation_angle = iba * pow(bsf, level)
            x_projection = length * cos(pi * bifurcation_angle / 180)
            y_projection = length * sin(pi * bifurcation_angle / 180)
            generate_body(level, x_projection, y_projection, length, radius)

    # method: creates veinous tree of vascular network
    # repeats steps of generate_artery() for veinous side of network
    def generate_vein(self):

        # sub-method: generates root vein (vessel #(num_vessels-1)) at maximum displacement
        def generate_root(x_projection, y_projection):
            x_extent = self.max_vessel_length
            bsf = self.config["bifurcation_scaling_factor"]
            iba = self.config["initial_bifurcation_angle"]
            lsf = self.config["length_scaling_factor"]
            for i in range(1, self.num_levels):

                bifurcation_angle = iba * pow(bsf, i)
                length_factor = pow(lsf, i)

                x_extent = x_extent + self.max_vessel_length * length_factor * cos(
                    pi * bifurcation_angle / 180)
            
            sink_vessel_idx = self.num_nodes - 1
            self.vessels[self.num_vessels-1] = Vessel(self.num_vessels-1, Coordinate(x_extent, 0, 0), Coordinate(x_extent-x_projection, 0, 0), self.max_vessel_length, self.max_vessel_radius)
            self.vessels[self.num_vessels-1].add_nodes([sink_vessel_idx-1, sink_vessel_idx])

        # sub-method: generates veinous sub-bodies to make up vein body
        # repeats steps of arterial side, but building in reverse from the final vessel
        def generate_body(level, x_projection, y_projection, length, radius):
            for node in range(pow(2, level - 1), pow(2, level)):  # parallel
                node_idx = self.num_nodes - node - 1
                parent_index = self.num_vessels - node
                
                vessel1_idx = self.num_vessels - node * 2 - 1
                vessel2_idx = self.num_vessels - node * 2
                
                parent_x = self.vessels[parent_index].end.x - x_projection
                parent1_y = self.vessels[parent_index].end.y + y_projection
                parent2_y = self.vessels[parent_index].end.y - y_projection
                
                self.vessels[vessel1_idx] = Vessel(vessel1_idx, self.vessels[parent_index].end, Coordinate(parent_x,parent1_y,0), length, radius)
                self.vessels[vessel1_idx].add_nodes([(self.num_nodes-node*2-2), node_idx])
                self.vessels[vessel2_idx] = Vessel(vessel2_idx, self.vessels[parent_index].end, Coordinate(parent_x,parent2_y,0), length, radius)
                self.vessels[vessel2_idx].add_nodes([(self.num_nodes-node*2-1), node_idx])

        generate_root(self.max_vessel_length, 0)

        for level in range(1, self.num_levels):
            lsf = self.config["length_scaling_factor"]
            iba = self.config["initial_bifurcation_angle"]
            bsf = self.config["bifurcation_scaling_factor"]
            rsf = self.config["radius_scaling_factor"]

            length = self.max_vessel_length * pow(lsf, level)
            radius = self.max_vessel_radius * pow(rsf, level)
            bifurcation_angle = iba * pow(bsf, level)
            x_projection = length * cos(pi * bifurcation_angle / 180)
            y_projection = length * sin(pi * bifurcation_angle / 180)
            generate_body(level, x_projection, y_projection, length, radius)

    # method: generate entire vascular network
    def generate(self):
        self.generate_artery()
        self.generate_vein()

    # method: return total number of vessels in network
    def get_num_vessels(self):
        return pow(2, self.num_levels + 1) - 2

    # method: return total number of nodes in network
    def get_num_nodes(self):
        return 3 * pow(2, self.num_levels - 1)
    
    # method: return the volumetric flow rate for the last vessel (root vein)
    def get_output_flow_rate(self):
        output_flow_rate = pow(2, self.num_levels-1) * np.pi * pow(self.config["min_vessel_radius"], 2)
        return output_flow_rate
    
    # method: set network properties to variables that can be accessed by other methods
    def set_properties(self):
        self.num_nodes = self.get_num_nodes()
        self.num_vessels = self.get_num_vessels()
        self.vessels = np.ndarray(self.num_vessels, dtype=Vessel)

        self.max_vessel_radius = self.config["min_vessel_radius"] / pow(
            self.config["radius_scaling_factor"], self.num_levels - 1)
        self.max_vessel_length = self.config["min_vessel_length"] / pow(
            self.config["length_scaling_factor"], self.num_levels - 1)
        
    # method: set the configurations if not using default
    def set_config(self, config: dict):
        self.config = config
        self.set_properties()


# function: returns new set of configrations if not default
def make_configs(min_vessel_length=0.055,
                 min_vessel_radius=0.0025,
                 length_scaling_factor=0.8,
                 initial_bifurcation_angle=70,
                 bifurcation_scaling_factor=0.6,
                 radius_scaling_factor=0.793700525984100):
    return {
        "min_vessel_length": min_vessel_length,
        "min_vessel_radius": min_vessel_radius,
        "length_scaling_factor": length_scaling_factor,
        "initial_bifurcation_angle": initial_bifurcation_angle,
        "bifurcation_scaling_factor": bifurcation_scaling_factor,
        "radius_scaling_factor": radius_scaling_factor
    }
