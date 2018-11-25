from sys import path as sys_path
sys_path.append('./../')

from pycavalier import projection_tools as pt
from pylab import *

# create a view point

viewpoint = pt.viewpoint( latitude = 0.9*pi/2., longitude = pi/10. )

# create box

sides = [ [ [0,0,1], [0,1,1], [1,1,1], [1,0,1] ] ]
sides += [ [ [1,0,0], [1,0,1], [1,1,1], [1,1,0] ] ]
sides += [ [ [0,1,0], [0,1,1], [1,1,1], [1,1,0] ] ]

# show box

for side in sides :
    viewpoint.plot_patch( side, color = 'tab:brown', edgecolor = 'black' )

axis('equal')
show()
