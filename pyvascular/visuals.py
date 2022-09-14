# Copyright (c) 2022  R. Tohid (@rtohid)
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#!/usr/bin/env python3

from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d

from pyvascular.network import Network


def plot_network2D(network: Network, save=None, file_name=None):
    num_vessels = network.get_num_vessels()

    plt.figure(1)
    #plt.axes([0, 0, 2, 2])

    for i in range(num_vessels):
        vessel = network.vessels[i]
        x1 = vessel.start.x
        y1 = vessel.start.y
        x2 = vessel.end.x
        y2 = vessel.end.y
        plt.plot([x1, x2], [y1, y2], color='blue')
        #plt.text(x1, y1 + 0.002, i, color='red')
    if save:
        if not file_name:
            file_name = f"network-{network.num_levels}-{network.num_dimensions}.jpg"
        plt.savefig(file_name, bbox_inches='tight')
    else:
        plt.show()
        
 
def plot_network3D(network: Network, save=None, file_name=None):
    num_vessels = network.get_num_vessels()

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    for i in range(num_vessels):
        vessel = network.vessels[i]
        x1 = vessel.start.x
        y1 = vessel.start.y
        z1 = vessel.start.z
        x2 = vessel.end.x
        y2 = vessel.end.y
        z2 = vessel.end.z
        ax.plot3D([x1,x2], [y1,y2], [z1,z2], color='blue')
    if save:
        if not file_name:
            file_name = f"network-{network.num_levels}-{network.num_dimensions}.jpg"
        plt.savefig(file_name, bbox_inches='tight')
    else:
        plt.show()
  
        
def plot_network(network: Network, save=None, file_name=None):
    if network.num_dimensions == 2:
        plot_network2D(network, save, file_name)
    elif network.num_dimensions == 3:
        plot_network3D(network, save, file_name)
    else:
        print("ERROR: Network must be 2 or 3 dimensions")
