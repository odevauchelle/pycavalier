from sys import path as sys_path
sys_path.append('./../')

from pycavalier import projection_tools as pt
from pylab import *

# create a view point

viewpoint = pt.viewpoint( latitude = 0.9*pi/2., longitude = pi/10. )

# show refrence frame

viewpoint.show_reference_frame()

# create disk

radius = 2
theta = linspace(0,2*pi,100)
center = array( [ 3, 2.5, 0 ] )
circle = center + array( [ radius*cos(theta), radius*sin(theta), 0.*theta ] ).T

# show disk

viewpoint.plot_points( circle, '--', lw = 3 )

axis('equal')
show()
