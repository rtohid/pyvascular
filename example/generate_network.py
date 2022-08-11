# Copyright (c) 2022  R. Tohid (@rtohid)
#
# Distributed under the Boost Software License, Version 1.0. (See accompanying
# file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from pyvascular.network import Network
from pyvascular.visuals import plot_network

vascular_network = Network(6, 2, 1)
vascular_network.generate()

plot_network(vascular_network, save=1)
