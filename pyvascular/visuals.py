# Copyright (c) 2022  R. Tohid (@rtohid)
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
#!/usr/bin/env python3

from matplotlib import pyplot as plt

from pyvascular.network import Network


def plot_network(network: Network, save=None, file_name=None):

    nodes = network.nodes
    num_nodes = network.num_nodes

    plt.figure(1)
    plt.axes([0, 0, 2, 2])

    for i in range(num_nodes):
        node = network.nodes[i]
        x1 = node.coordinate.x
        y1 = node.coordinate.y
        for child in node.children:
            x2 = nodes[child].coordinate.x
            y2 = nodes[child].coordinate.y
            plt.plot([x1, x2], [y1, y2], color='blue', marker='o')
        plt.text(x1, y1 + 0.002, i, color='red')
    if save:
        if not file_name:
            file_name = f"network-{network.num_levels}-{network.num_dimensions}.jpg"
        plt.savefig(file_name, bbox_inches='tight')
    else:
        plt.show()
