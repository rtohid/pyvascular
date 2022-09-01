
# test script to assemble conductance matrix in parallel using MPI

from mpi4py import MPI
import numpy as np
from pyvascular.network import Network

comm = MPI.COMM_WORLD
mpiSize = comm.Get_size()
mpiRank = comm.Get_rank()

network = Network(3, 2, 1)
network.generate()
vessels = network.vessels
numVessels = network.get_num_vessels()

# determine the workload of each rank
workloads = [ numVessels // mpiSize for i in range(mpiSize) ]
for i in range( numVessels % mpiSize ):
    workloads[i] += 1
my_start = 0
for i in range( mpiRank ):
    my_start += workloads[i]
my_end = my_start + workloads[mpiRank]

#print("Rank, start, end: ", mpiRank, my_start, my_end)
#print("Rank:", mpiRank, "num per node: ", (my_end-my_start))

# if mpiRank == 0:
#     out_0 = np.zeros((numVessels))
#     out_0[0] = 1
#     out_end = np.zeros((numVessels))
#     out_end[-1] = -3
#     out_end[-2] = 3
#     print(out_0)
#     print(out_end)
# out = np.zeros(((my_end-my_start), numVessels))

triplet = np.empty([1, 3])
for i in range(my_start, my_end):
    start_node = vessels[i].nodes[0]
    end_node = vessels[i].nodes[1]
    #print("i = ",i, ", rank = ",mpiRank)
    #print("Rank:", mpiRank, "sn, en", start_node, end_node)
    #triplet = np.append(triplet, [start_node, end_node, 'cond.'])
    triplet = np.append(triplet, [i, start_node, 'cond.'])
    triplet = np.append(triplet, [i, end_node, 'cond.'])
 
triplet.resize(2*(my_end-my_start)+1, 3)  
triplet = np.delete(triplet, 0, 0)
 
 
triplet = comm.gather(triplet, root=0)  
if mpiRank==0:
    triplet = np.concatenate(triplet)
    print(triplet)