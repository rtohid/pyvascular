# Copyright (c) 2022  R. Tohid (@rtohid)
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

import numpy as np

from math import pi, cos, sin
from pyvascular.vessel import Vessel
from pyvascular.node import Node, Coordinate

default_config = {
    "min_vessel_length": 0.055,
    "min_vessel_radius": 0.0025,
    "length_scaling_factor": 0.8,
    "initial_bifurcation_angle": 70,
    "bifurcation_scaling_factor": 0.6,
    "radius_scaling_factor": 0.793700525984100
}


class Network:

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
        #self.boundary_conditions = list()

    def generate_artery(self):

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
                
            self.nodes[0] = Node(0, Coordinate(-x_extent, 0, 0))
            self.nodes[0].add_child([1])
            self.nodes[0].add_out_vessel([0])
            x_1 = self.nodes[0].coordinate.x + x_projection
            y_1 = self.nodes[0].coordinate.y + y_projection
            self.nodes[1] = Node(1, Coordinate(x_1, y_1, 0))
            self.nodes[1].add_parent([0])
            self.nodes[1].add_in_vessel([0])
            
            self.vessels[0] = Vessel(0, Coordinate(-x_extent,0,0), Coordinate(x_1, y_1, 0), self.max_vessel_length, self.max_vessel_radius)
            self.vessels[0].add_nodes([0, 1])

        def generate_body(level, x_projection, y_projection, length, radius):
            for node in range(pow(2, level - 1), pow(2, level)):  # parallel
                child1_idx = node * 2
                child1_x = self.nodes[node].coordinate.x + x_projection
                child1_y = self.nodes[node].coordinate.y + y_projection
                self.nodes[child1_idx] = Node(
                    child1_idx, Coordinate(child1_x, child1_y, 0))
                self.nodes[child1_idx].add_parent([node])

                child2_idx = child1_idx + 1
                child2_x = self.nodes[node].coordinate.x + x_projection
                child2_y = self.nodes[node].coordinate.y - y_projection
                self.nodes[child2_idx] = Node(
                    child2_idx, Coordinate(child2_x, child2_y, 0))
                self.nodes[child2_idx].add_parent([node])

                self.nodes[node].add_child([child1_idx, child2_idx])

                vessel_1 = node * 2 - 1
                vessel_2 = node * 2

                self.nodes[node].add_out_vessel([vessel_1, vessel_2])
                self.nodes[child1_idx].add_in_vessel([vessel_1])
                self.nodes[child2_idx].add_in_vessel([vessel_2])
                
                self.vessels[vessel_1] = Vessel(vessel_1, self.nodes[node].coordinate, Coordinate(child1_x,child1_y,0), length, radius)
                self.vessels[vessel_1].add_nodes([node, child1_idx])
                self.vessels[vessel_2] = Vessel(vessel_2, self.nodes[node].coordinate, Coordinate(child2_x,child2_y,0), length, radius)
                self.vessels[vessel_2].add_nodes([node, child2_idx])

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

    def generate_vein(self):

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
            #x_extent = x_extent * 2
            sink_node_idx = self.num_nodes - 1


            self.nodes[sink_node_idx] = Node(sink_node_idx,
                                             Coordinate(x_extent, 0, 0))
            self.nodes[sink_node_idx].add_parent([sink_node_idx - 1])

            self.nodes[sink_node_idx].add_in_vessel([self.num_vessels - 1])

            x = self.nodes[sink_node_idx].coordinate.x - x_projection
            y = self.nodes[sink_node_idx].coordinate.y + y_projection
            self.nodes[sink_node_idx - 1] = Node(sink_node_idx - 1,
                                                 Coordinate(x, y, 0))
            self.nodes[sink_node_idx - 1].add_child([sink_node_idx])
            self.nodes[sink_node_idx - 1].add_out_vessel(
                [self.num_vessels - 1])
            
            self.vessels[self.num_vessels-1] = Vessel(self.num_vessels-1, Coordinate(x_extent, 0, 0), Coordinate(x, y, 0), self.max_vessel_length, self.max_vessel_radius)
            self.vessels[self.num_vessels-1].add_nodes([sink_node_idx - 1, sink_node_idx])

        def generate_body(level, x_projection, y_projection, length, radius):
            for node in range(pow(2, level - 1), pow(2, level)):  # parallel
                node_idx = self.num_nodes - node - 1

                parent1_idx = self.num_nodes - node * 2 - 2
                parent1_x = self.nodes[node_idx].coordinate.x - x_projection
                parent1_y = self.nodes[node_idx].coordinate.y + y_projection
                self.nodes[parent1_idx] = Node(
                    parent1_idx, Coordinate(parent1_x, parent1_y, 0))
                self.nodes[parent1_idx].add_child([node_idx])

                parent2_idx = self.num_nodes - node * 2 - 1
                parent2_x = self.nodes[node_idx].coordinate.x - x_projection
                parent2_y = self.nodes[node_idx].coordinate.y - y_projection
                self.nodes[parent2_idx] = Node(
                    parent2_idx, Coordinate(parent2_x, parent2_y, 0))
                self.nodes[parent2_idx].add_child([node_idx])

                self.nodes[node_idx].add_parent([parent1_idx, parent2_idx])

                vessel_1 = self.num_vessels - node * 2 - 1
                vessel_2 = self.num_vessels - node * 2

                self.nodes[node_idx].add_in_vessel([vessel_1, vessel_2])
                self.nodes[parent1_idx].add_out_vessel([vessel_1])
                self.nodes[parent2_idx].add_out_vessel([vessel_2])
                
                self.vessels[vessel_1] = Vessel(vessel_1, self.nodes[node_idx].coordinate, Coordinate(parent1_x,parent1_y,0), length, radius)
                self.vessels[vessel_1].add_nodes([parent1_idx, node_idx])
                self.vessels[vessel_2] = Vessel(vessel_2, self.nodes[node_idx].coordinate, Coordinate(parent2_x,parent2_y,0), length, radius)
                self.vessels[vessel_2].add_nodes([parent2_idx, node_idx])


        def generate_border():
            for node in range(pow(2, self.num_levels - 2),
                              pow(2, self.num_levels - 1)):  # parallel
                node_idx = self.num_nodes - node - 1

                parent1_idx = self.num_nodes - node * 2 - 2
                self.nodes[parent1_idx].add_child([node_idx])

                parent2_idx = self.num_nodes - node * 2 - 1
                self.nodes[parent2_idx].add_child([node_idx])

                self.nodes[node_idx].add_parent([parent1_idx, parent2_idx])
                vessel_1 = self.num_vessels - node * 2 - 1
                vessel_2 = self.num_vessels - node * 2

                self.nodes[node_idx].add_in_vessel([vessel_1, vessel_2])
                self.nodes[parent1_idx].add_out_vessel([vessel_1])
                self.nodes[parent2_idx].add_out_vessel([vessel_2])

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

        generate_border()

    def generate(self):
        self.generate_artery()
        self.generate_vein()

    def get_num_vessels(self):
        return pow(2, self.num_levels + 1) - 2

    def get_num_nodes(self):
        return 3 * pow(2, self.num_levels - 1)
    
    # def add_boundary_conditions(self, indecies: list):
    #     self.boundary_conditions.extend(indecies)
    
    def get_output_flow_rate(self):
        output_flow_rate = pow(2, self.num_levels-1) * np.pi * pow(self.config["min_vessel_radius"], 2)
        return output_flow_rate
    
    def set_properties(self):
        self.num_nodes = self.get_num_nodes()
        self.num_vessels = self.get_num_vessels()
        self.vessels = np.ndarray(self.num_vessels, dtype=Vessel)
        self.nodes = np.ndarray(self.num_nodes, dtype=Node)

        self.max_vessel_radius = self.config["min_vessel_radius"] / pow(
            self.config["radius_scaling_factor"], self.num_levels - 1)
        self.max_vessel_length = self.config["min_vessel_length"] / pow(
            self.config["length_scaling_factor"], self.num_levels - 1)
        
    def set_config(self, config: dict):
        self.config = config
        self.set_properties()


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
