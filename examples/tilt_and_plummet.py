from sys import path as sys_path
sys_path.append('./../')

from pycavalier import projection_tools as pt
from pylab import *

# define the vertical direction

tilt_angles = [ 0, -pi/8, -pi/4 ]

for tilt_angle in tilt_angles :

    # create viewpoint with tilt

    viewpoint = pt.viewpoint( latitude = 0.9*pi/2., longitude = pi/10., plummet = [ 0,-sin(tilt_angle), -cos(tilt_angle) ] )

    # translate reference frame

    viewpoint.reference_frame['center'] = viewpoint.reference_frame['center'] + array( [-6, 0, 0] )

    # show refrence frame and plummet

    viewpoint.show_reference_frame()
    viewpoint.show_plummet()


axis('equal')
savefig('tilt.svg', bbox_inches = 'tight')
show()
