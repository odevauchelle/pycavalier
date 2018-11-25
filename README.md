# Pycavalier

Pycavalier is a Python library to draw 3D objects using an oblique projection.

It is based on Matplotlib. In fact, it is just some tools added to Matplolib.

## Quick example:

```python
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
```
