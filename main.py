
#"Space Frame - Nodal Loads 1.py"
#----------------------------------------------
# A First Course in the Finite Element Method, 4th Edition
# Daryl L. Logan
# Example 5.8
# Units for this model are kips and inches

# Import 'FEModel3D' and 'Visualization' from 'PyNite'
from pickle import FLOAT
from PyNite import FEModel3D
from PyNite import Visualization




# Create a new model
frame = FEModel3D()

# Define the nodes
frame.add_node('N1', 0, 0, 0)
frame.add_node('N2', -100, 0, 0)
frame.add_node('N3', 0, 0, -100)
frame.add_node('N4', 0, -100, 0)

meshPoints=[[0, 0, 0],[ -100, 0, 0],[0, 0, -100],[ 0, -100, 0]]
meshnode=['N1','N2','N3','N4']

# Define the supports
frame.def_support('N2', True, True, True, True, True, True)
frame.def_support('N3', True, True, True, True, True, True)
frame.def_support('N4', True, True, True, True, True, True)

# Create members (all members will have the same properties in this example)
J = 50
Iy = 100
Iz = 100
A = 10

# Define a material
E = 30000
G = 10000
nu = 0.3
rho = 2.836e-4
frame.add_material('Steel', E, G, nu, rho)

frame.add_member('M1', 'N2', 'N1', 'Steel', Iy, Iz, J, A)
frame.add_member('M2', 'N3', 'N1', 'Steel', Iy, Iz, J, A)
frame.add_member('M3', 'N4', 'N1', 'Steel', Iy, Iz, J, A)

# Add nodal loads
frame.add_node_load('N1', 'FY', -50)
frame.add_node_load('N1', 'MX', -1000)
#----------------------------------------------
# node,member array....

SortedPoints=meshPoints
SortedPoints.sort(key=lambda meshPoints: meshPoints[2]) 
#distincted = list(set(meshPoints[2]))
distincted = list(dict.fromkeys(meshPoints[2]))

SortedPointsFloor=SortedPoints
w=0
for x in SortedPoints[2]:
    for y in distincted:
        if x==y :
            w=w+1
            SortedPointsFloor[2]=w



for f2 in distincted:
    Mesh2D=""
    for q in SortedPointsFloor:
        if f2== q:
             Mesh2D.append(q[0],q[1])


#"demo.py"
#------------------------------------------
    from meshpy.tet import MeshInfo, build

    mesh_info = MeshInfo()
    mesh_info.set_points(
      [
        (0, 0, 0),
        (2, 0, 0),
        (2, 2, 0),
        (0, 2, 0),
        (0, 0, 12),
        (2, 0, 12),
        (2, 2, 12),
        (0, 2, 12),
       ]
    )
#-------------------------------
    mesh_info.set_points=Mesh2D
#-------------------------------
    mesh_info.set_facets(
     [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [0, 4, 5, 1],
        [1, 5, 6, 2],
        [2, 6, 7, 3],
        [3, 7, 4, 0],
      ]
    )
    mesh = build(mesh_info)
    print("Mesh Points:")
    for i, p in enumerate(mesh.points):
        print(i, p)
    print("Point numbers in tetrahedra:")
    for i, t in enumerate(mesh.elements):
        print(i, t)
    mesh.write_vtk("test.vtk")
#-----------------------------------------
    Mesh2DBuild=mesh.points

#for floor

#"example10.py"
#------------------------------
    if __name__ == '__main__':
       import matplotlib.pyplot as plt
       from FEM.Elasticity2D import PlaneStressSparse
       from FEM.Geometry import Geometry2D, Delaunay
       import numpy as np

       E = 21000000.0  # MPa
       v = 0.2  # m
       h = 0.6  # m
       b = 0.3  # m
       L = 2.5  # m
       a = h**2/100
       gamma = 23.54

       coords = np.array([[0.0, 0.0], [L, 0.0], [L, h], [0.0, h]])
       params = Delaunay._strdelaunay(a=0.01, q=30, o=2)
       geo = Delaunay(coords, params, nvn=2, fast=True)
       cb = geo.cbFromRegion(3, 0.0, 1)
       cb += geo.cbFromRegion(3, 0.0, 2)
       geo.setCbe(cb)
       O = PlaneStressSparse(geo, E, v, b,
                          fy=lambda x: -gamma, verbose=True)
       O.solve()
       O.exportJSON("Example10.json")
    #plt.show()
#---------------------------------

#test01=float(O.fx)

#for a in Mesh2DBuild:
#    hh=Mesh2DBuild.tolist()
    for a,aa2 in enumerate(Mesh2DBuild):
    #gg=hh.index(a)
        for b in Mesh2D:
            if aa2==b :
            #stress2D=O.fx   # O.fz is needed ,test other examples 
               stress2D=100   # O.fz is needed ,test other examples 
            #stress2D=O.fx
               frame.add_node_load( meshnode[a], 'FZ', stress2D)  # O




#continue "Space Frame - Nodal Loads 1.py" for stress load
#-----------------------------------
# Add nodal loads
frame.add_node_load('N1', 'FY', -50)
frame.add_node_load('N1', 'MX', -1000)
#-----------------------------------

#solve in "Space Frame - Nodal Loads 1.py"
#----------------------------------
# Analyze the model
frame.analyze(check_statics=True)

# Render the deformed shape
Visualization.render_model(frame, annotation_size=5, deformed_shape=True, deformed_scale=100, render_loads=True)

# Print the node 1 displacements
print('Node 1 deformations:')
print('Calculated values: ', frame.Nodes['N1'].DX, frame.Nodes['N1'].DY, frame.Nodes['N1'].DZ, frame.Nodes['N1'].RX, frame.Nodes['N1'].RY, frame.Nodes['N1'].RZ)
print('Expected values: ', 7.098e-5, -0.014, -2.352e-3, -3.996e-3, 1.78e-5, -1.033e-4)
#-----------------------------------
#Macro send parameters to Excel
#Macro run
#Macro get results
#print and draw results 
#//----------