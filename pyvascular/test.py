# Example run to get the blood flow rate solutions for each vessel
# for a network with 3 generations

import numpy as np
from pyvascular.network import Network
from pyvascular.conductance import assemble_matrix, assemble_rhs_vector, solve_flows

# create network and generate the vessels
network = Network(3, 2, 1)
network.generate()

# assemble the conductance array
conductance_array = assemble_matrix(network)

# assemble the RHS pressure vector
rhs_vector = assemble_rhs_vector(network)

# solve the linear system Ax=b
pressureVector = np.linalg.solve(conductance_array, rhs_vector)

# assemble the vessel conductance matrix and solve for flow rates
flow_array = solve_flows(network, pressureVector)

# print flow rates
print(flow_array)