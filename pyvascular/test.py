# example script to run project sequentially
# updating to monitor time and memory usage

# if python generates ModuleNotFoundError, paste following in command line
# export PYTHONPATH="${PYTHONPATH}:/Users/notmax/Desktop/VascularFiles/pyvascular_test/pyvascular/"

from mpi4py import MPI
from scipy.sparse.linalg import spsolve
import tracemalloc

from pyvascular.network import Network
from pyvascular.conductance import assemble_matrix, assemble_rhs_vector, solve_flows

#--------------------- MAIN ---------------------#

# Begin Total Project Timing
total_time_start = MPI.Wtime()

# create network and generate the vessels
start_time = MPI.Wtime()
numLevels = 15
numDims = 2
print("Building Network: " + str(numLevels) + " Levels")
network = Network(numLevels, numDims, 1)
network.generate()
print("Number of Vessels in Network: " + str(network.get_num_vessels()))
end_time = MPI.Wtime()
print("Generate Network time: " + str(end_time-start_time))

# assemble the conductance array
start_time = MPI.Wtime()
#tracemalloc.start()
conductance_array = assemble_matrix(network)
#current, peak = tracemalloc.get_traced_memory()
#tracemalloc.stop()
#print(f"Current memory usage is {current / 10**3}KB; Peak was {peak / 10**3}KB; Diff = {(peak - current) / 10**3}KB")
#tracemalloc.stop()
end_time = MPI.Wtime()
print("Assemble Conductance Matrix time: " + str(end_time-start_time))

# assemble the RHS pressure vector
start_time = MPI.Wtime()
rhs_vector = assemble_rhs_vector(network)
end_time = MPI.Wtime()
print("Assemble RHS vector time: " + str(end_time-start_time))

# solve the linear system Ax=b
start_time = MPI.Wtime()
pressureVector = spsolve(conductance_array, rhs_vector)
end_time = MPI.Wtime()
print("Solve Pressures time: " + str(end_time-start_time))

# assemble the Poiseuille equations matrix and solve for flow rates
start_time = MPI.Wtime()
flow_array = solve_flows(network, pressureVector)
end_time = MPI.Wtime()
print("Solve Flow Rates time: " + str(end_time-start_time))
#print(flow_array)

# End Total Project Timing
total_time_end = MPI.Wtime()
print("Total Project Time:", (total_time_end-total_time_start))