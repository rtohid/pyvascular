
# WIP: test script to run pieces of project in parallel
# update to add timing and memory monitoring

import numpy as np
import scipy.sparse as ss
from scipy.sparse.linalg import spsolve
from mpi4py import MPI

from pyvascular.network import Network
from parallel_functions import assemble_triplet_parallel, determine_workloads
from pyvascular.conductance import assemble_matrix, assemble_rhs_vector, check_flows_are_correct, solve_flows

# MPI
comm = MPI.COMM_WORLD
mpiSize = comm.Get_size()
mpiRank = comm.Get_rank()

# STEP 1: generate vascular network
if mpiRank == 0:
    start_time = MPI.Wtime()
    network = Network(3, 2, 1)
    network.generate()
else:
    network = None


# STEP 2: assemble conductance matrix
if mpiRank == 0:
	conductance_array = assemble_matrix(network)


# STEP 3: assemble RHS vector
if mpiRank == 0:
	rhs_vector = assemble_rhs_vector(network)


# STEP 4: solve for pressures
if mpiRank == 0:
	pressureVector = spsolve(conductance_array, rhs_vector)
else:
    pressureVector = None

pressureVector = comm.bcast(pressureVector, root=0)



# STEP 5: assemble conductance triplet
network = comm.bcast(network, root=0)
# determine the workload of each rank
start, end = determine_workloads(network, mpiSize, mpiRank)

# call function and combine retreive output
triplet = assemble_triplet_parallel(network, start, end)
triplet = comm.gather(triplet, root=0)
if mpiRank == 0:
    triplet = np.concatenate(triplet)
    row = triplet[:,0].astype(int)
    col = triplet[:,1].astype(int)
    val = triplet[:,2]
    sparse_triplet = ss.csr_array((val, (row, col)))
    dense = sparse_triplet.todense()
else:
    #sparse_triplet = None
    dense = None
    
#sparse_triplet = comm.bcast(sparse_triplet, root=0)
dense = comm.bcast(dense, root=0)

if mpiRank == 0:
    dense_row = dense.shape[0]
    if dense_row >= mpiSize:
        split = np.array_split(dense, mpiSize, axis=0)
else:
    split = None
    
split = comm.scatter(split, root=0)
split = np.dot(split, pressureVector)
data = comm.gather(split, root=0)

if mpiRank == 0:
    result = np.concatenate(data)
    end_time = MPI.Wtime()
    #print(result)
    print("Total time:", (end_time-start_time))
