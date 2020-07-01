#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Olivier Devauchelle, 2018

"""
Distributes points randomly on a polygon.
"""

__author__ = "Olivier Devauchelle"
__copyright__ = "Copyright 2018"
__license__ = "GPL"

from pylab import *
import matplotlib.path as mplPath


def rand2d( npts, rectangle = array( [ [ 0, 0 ], [ 1., 1. ] ] ) ) :

    xmin, ymin = tuple( rectangle[0] )
    xmax, ymax = tuple( rectangle[1] )

    x = xmin + ( xmax - xmin )*rand( npts )
    y = ymin + ( ymax - ymin )*rand( npts )

    return array( [ x, y ] ).T

def rectangle_around_polygon( polygon ) :

    x, y = polygon[:,0], polygon[:,1]

    return array( [ [ min(x), min(y)] , [ max(x), max(y)] ] )

def number_of_points( density, rectangle ) :

    xmin, ymin = tuple( rectangle[0] )
    xmax, ymax = tuple( rectangle[1] )

    area = ( xmax - xmin )*( ymax - ymin )

    return int( density*area )

def random_points_in_polygon( polygon, density, rand2d = rand2d ) :

    rectangle = rectangle_around_polygon( polygon )

    npts = number_of_points( density, rectangle )

    if npts < 10 :
        print('Warning random_points_in_polygon: total number of random points =', npts)

    cloud = rand2d( npts, rectangle = rectangle )

    in_polygon = mplPath.Path( polygon ).contains_points( cloud )

    return list( cloud[ in_polygon ] )


if __name__ == '__main__' :

    theta = linspace( 0, 2*pi, 50 )
    r = 1. + 0.2*cos( 5*theta )

    polygon = array( [ r*cos(theta), r*sin(theta) ] ).T

    cloud =  array( random_points_in_polygon( polygon, 10 ) )

    print( cloud )

    plot( cloud[:,0], cloud[:,1], '.' )
    plot( polygon[:,0], polygon[:,1] )

    axis( 'equal' )
    show()
