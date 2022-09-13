# This file contains all the IO functions to save data in HDF5 format
# file_path = '/Users/notmax/Desktop/VascularFiles/pyvascular_test/'

import os
import h5py
import numpy as np
from scipy.sparse.linalg import spsolve
from pyvascular.network import Network
from pyvascular.conductance import assemble_matrix, assemble_rhs_vector, solve_flows

# Function to warn user if file already exists in directory
#	This will prevent H5 errors in script, and stop unsaved data being overwritten
def delete_file_if_exists(file_path):
    if os.path.exists(file_path):
        i = 0
        while i < 2:
            inp = input(str(file_path) + " already exists. Would you like to rewrite? Y/N\n")
            if any(inp.lower() == f for f in ["yes", 'y', '1', 'ye']):
                os.remove(file_path)
                print("User confirmed file rewrite. Overwriting now.")
                break
            elif any(inp.lower() == f for f in ["no", 'n', '0']):
                print("User declined file overwrite")
                print("Please rename file and rerun script")
                print("TERMINATING PROGRAM")
                raise SystemExit(0)
            else:
                i += 1
                if i < 2:
                    print("User response must cornfirm or deny. Please enter your input again: ")
                else:
                    print("Invalid response")
                    raise SystemExit(0)           
    else:
        print(str(file_path) + " does not exist. File will be written now.")

# convert vessel to geometry row
#	each row of geom array contains the starting and ending x,y,z and the radius of a vessel
def ConvertVesselToGeometryRow(vessel, geomArray, index):
	geomArray[index][0] = vessel.start.x
	geomArray[index][1] = vessel.start.y
	geomArray[index][2] = vessel.start.z
	geomArray[index][3] = vessel.end.x
	geomArray[index][4] = vessel.end.y
	geomArray[index][5] = vessel.end.z
	geomArray[index][6] = vessel.radius
 
# convert vessel to node row
#	each row of nodeArray saves the start and end node of a vessel
def ConvertVesselToNodeArray(vessel, nodeArray, index):
	nodeArray[index][0] = vessel.nodes[0]
	nodeArray[index][1] = vessel.nodes[1]
 
# export vessel geometry and node data to h5 file
def export_vessel_data(network: Network, filename):
    # get network geometry and node data saved into respective arrays
    vessels = network.vessels
    numVessels = network.get_num_vessels()
    geomArray = np.zeros((numVessels, 7))
    nodeArray = np.zeros((numVessels, 2))
    for i in range(0, numVessels):
        ConvertVesselToGeometryRow(vessels[i], geomArray, i)
        ConvertVesselToNodeArray(vessels[i], nodeArray, i)
        
    # open h5 file and save information to groups
    f = h5py.File(filename, 'a')
    f.create_dataset("num_levels", (1,), data=network.num_levels)
    f.create_dataset("num_dimensions", (1,), data=network.num_dimensions)
    geom = f.create_group("GEOM_GROUP")
    geom.create_dataset("GEOM_ARRAY", (numVessels, 7), data=geomArray)
    geom.create_dataset("NODE_ARRAY", (numVessels, 2), data=nodeArray)
    f.close()
    
# function to export conductance matrix in CSR format
#	saves csr matrix data, indices, and indptr as individual datasets
#	that can be reconstructed in scipy csr format
def export_conductance(cond_matrix, filename):
    f = h5py.File(filename, 'a')
    cond = f.create_group("CONDUCTANCE_GROUP")
    cond.create_dataset("MTX_VALUES", data=cond_matrix.data)
    cond.create_dataset("MTX_INDPTR", data=cond_matrix.indptr)
    cond.create_dataset("MTX_INDICES", data=cond_matrix.indices)
    cond.attrs['SHAPE'] = cond_matrix.shape
    f.close()

# function to export RHS vector (boundary values)
def export_rhs_vector(rhs_vector, filename):
    f = h5py.File(filename, 'a')
    rhs = f.create_group("BOUNDARY_VALUES_GROUP")
    rhs.create_dataset("RHS_VECTOR", data=rhs_vector)
    f.close()

# function to export pressure solution vector
def export_pressures(pressure_vector, filename):
    f = h5py.File(filename, 'a')
    pressures = f.create_group("PRESSURES_GROUP")
    pressures.create_dataset("PRESSURE_SOLUTION_VECTOR", data=pressure_vector)
    f.close()

# function to export flow solution vector
def export_flows(flow_array, filename):
    f = h5py.File(filename, 'a')
    flows = f.create_group("FLOW_GROUP")
    flows.create_dataset("HEALTHY_FLOWS_ARRAY", data=flow_array)
    f.close()
    
    
# function to export all data to h5 file
def export_all(network, cond_matrix, rhs_vector, pressure_vector, flow_array, filename):
    delete_file_if_exists(filename)
    export_vessel_data(network, filename)
    export_conductance(cond_matrix, filename)
    export_rhs_vector(rhs_vector, filename)
    export_pressures(pressure_vector, filename)
    export_flows(flow_array, filename)