from sys import path as sys_path
sys_path.append('./../')

from pycavalier import projection_tools as pt
from pylab import *

# create a view point

viewpoint = pt.viewpoint( latitude = 0.7*pi/2., longitude =-.4*pi/2. )
viewpoint.show_reference_frame()

# create sandy wavy bed

x = linspace( 0, 4*pi, 100 )
z = -.5*cos(x)
points = array( [ x, 0*x, z ] ).T
width = array([0, 3, 0])
patches = [ [ points[i], points[i+1], points[i+1] + width,  points[i] + width] for i in range( len(points) - 1 ) ]

# show bed patches

for patch in patches :
    viewpoint.plot_patch( patch, color = 'tab:brown', alpha = .3, edgecolor = 'none' )
    dots = pt.dotify( patch, 30 )
    viewpoint.plot_points( dots, '.', ms = 2, color = 'tab:brown', alpha = .3 )

axis('equal')
savefig('decoration.svg', bbox_inches = 'tight')
show()
