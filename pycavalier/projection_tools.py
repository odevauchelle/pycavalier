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
Pycavalier projection tools
"""

__author__ = "Olivier Devauchelle"
__copyright__ = "Copyright 2018"
__license__ = "GPL"

import numpy as np
from numpy.linalg import norm as np_norm
import matplotlib.pyplot as matplotlib_pyplot
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

if __name__ == '__main__' :
    from random_points_in_polygon import random_points_in_polygon
else :
    from .random_points_in_polygon import random_points_in_polygon


def projector( point, n_X, n_Y ) :
    return np.array( [ np.dot( point, n_X ), np.dot( point, n_Y ) ] )


default_reference_frame = { 'center' : np.array( [ 0, 0, 0 ] ),
    'direction' : { 'x' : np.array( [ 1, 0, 0 ] ),
        'y' : np.array( [ 0, 1, 0 ] ),
        'z' : np.array( [ 0, 0, 1 ] )
        }
    }

class viewpoint :
    '''
    A projection frame, oriented with respect to the viewer.
    '''

    def __init__( self, latitude, longitude, plummet = ( 0, 0, -1 ), reference_frame = default_reference_frame ) :
        '''
        Create a projection frame.

        Parameters
        ----------
        latitude : float
            Orientation of the viewer with respect to vertical.
        longitude : float
            Orientation of the viewer around z-axis.
        plummet : tuple of length 3, optional
            Defines the vertical direction.
        reference_frame : Frame dictionary, optional
        '''

        self.latitude = latitude
        self.longitude = longitude
        self.plummet = np.array( plummet )/np_norm( plummet ) # the vertical direction

        self.reference_frame = reference_frame

        self.n_view = np.array( [  -np.sin( self.latitude )*np.cos( self.longitude ), -np.sin( self.latitude )*np.sin( self.longitude ), -np.cos( self.latitude ) ] )

        n_X = np.cross( self.plummet, self.n_view )
        self.n_X = n_X/np_norm( n_X )
        self.n_Y = np.array( np.cross( self.n_X, self.n_view ) )


    def project_on_screen( self, points ) :

        if len( np.shape( points ) ) == 2 :

            return np.array( list( map( lambda point : projector( point, self.n_X, self.n_Y ), points ) ) )

        elif np.shape( points ) == (3,) :

            return projector( points, self.n_X, self.n_Y )

    def plot_points( self, points, *args, ax = None, **kwargs ) :

        if ax is None :
            ax = matplotlib_pyplot.gca()

        x, y = tuple( self.project_on_screen( points ).T )

        ax.plot( x, y, *args, **kwargs )


    def plot_patch( self, points, *args, ax = None, **kwargs ) :

        if ax is None :
            ax = matplotlib_pyplot.gca()

        ax.add_collection( PatchCollection( [ Polygon( self.project_on_screen( points ) ) ], *args, **kwargs ) )


    def text( self, point, message, ax = None, **kwargs ) :

        if ax is None :
            ax = matplotlib_pyplot.gca()

        ax.text( *tuple( self.project_on_screen( point ) ), s = message, **kwargs )


    def show_reference_frame( self, color = 'black', axes_names = { 'x':'x', 'y':'y', 'z':'z' }, with_arrows = True, ax = None, adjust_ax_lims = True, text_pad = .15, **kwargs ) :

        if ax is None :
            ax = matplotlib_pyplot.gca()

        for xyz, direction in self.reference_frame['direction'].items() :

            xy = self.project_on_screen( self.reference_frame['center'] )
            xytext = self.project_on_screen( self.reference_frame['center'] + direction )

            try :
                direction_proj = self.project_on_screen(direction)/np_norm( self.project_on_screen(direction) )
            except :
                direction_proj = np.array([-1,-1])/sqrt(2)

            xytext_wp = xytext + text_pad*direction_proj

            if with_arrows :

                if adjust_ax_lims :
                    ax.plot( *np.array([ xy, xytext_wp ]).T, linestyle = 'none')# ), marker = 'o', color = 'red', alpha = .1 )

                ax.annotate(
                    s = '', #axes_names[xyz],
                    xy = xy,
                    xytext = xytext,
                    arrowprops = dict( arrowstyle = '<-', shrinkB = 0, shrinkA = 0 ),
                    annotation_clip = False,
                    ha = 'center', va = 'center'
                    )
            else :
                self.plot_points( np.array( [ xy, xytext ] ), color = color, **kwargs )

            ax.text( *xytext_wp, axes_names[xyz], color = color, ha = 'center', va = 'center' )

    def show_plummet( self, color = 'lightgrey', scale = .7 ) :

        self.plot_points([self.reference_frame['center'],self.reference_frame['center']+scale*self.plummet],color=color)
        self.plot_points([self.reference_frame['center']+scale*self.plummet],color=color,marker='d', ms = 5)

    def plot_subspace_ref( self, subspace, color = 'tab:red' ) :

        self.plot_points( [subspace.origin ], color = color, marker = 'o' )

        for n in subspace.base :
            self.plot_points( [subspace.origin, subspace.origin + n ], color = color )

    def length_arrow( self, **kwargs ) :
        length_arrow( self, **kwargs )

class subspace_2D :
    '''
    A 2D plane in 3D space.
    '''
    def __init__( self, points ) :
        '''
        Parameters
        ----------
        points: list of three points
            These points define the plane. Only the three first elements of the list are used.
        '''

        self.origin = points[1]

        v1, v2 = points[0] - self.origin, points[2] - self.origin

        n = np.cross( v1, v2 )

        self.normal = n/np_norm(n)

        n1 = v1/np_norm(v1)
        n2 = np.cross( self.normal, n1 )

        self.base = n1, n2


    def import_points( self, points ) :
        '''
        Projects 3D points onto the 2D subspace.

        Parameters
        ----------
        points: list of points belonging to the 3D space

        Returns
        ----------
        List of projected points
        '''

        return np.array( list( map( lambda point: projector( point - self.origin, *( self.base ) ), points ) ) )

    def export_points( self, points ) :
        '''
        Converts points in the subspace to points of the 3D space.

        Parameters
        ----------
        points: list of points belonging to the subspace

        Returns
        ----------
        List of corresponding points in the 3D space.
        '''

        return np.array( list( map( lambda point: self.origin + self.base[0]*point[0] + self.base[1]*point[1], points ) ) )


#########################
#
# associated functions
#
#########################

def dotify( the_polygon, density ) :

    ref2D = subspace_2D(the_polygon)
    the_polygon_2D = ref2D.import_points( the_polygon )

    return list( ref2D.export_points( random_points_in_polygon( the_polygon_2D, density ) ) )

def get_segments( points ) :
    return list( map( transpose, array( [ points[1:].T, points[:-1].T ] ).T ) )

def flat_arrow( arrow_center, arrow_length, arrow_width ) :

    arrow_head_width = 2.*arrow_width
    arrow_head_length = 0.5*arrow_length

    arrow = 1.*np.array([[ 0, -arrow_width/2. ],
        [ arrow_length - arrow_head_length, -arrow_width/2. ],
        [ arrow_length - arrow_head_length, -arrow_head_width/2. ],
        [ arrow_length, 0. ]
        ])

    arrow = np.array( list( arrow ) + list( np.array([1,-1]).T*arrow[::-1][1:] ) )

    return arrow - np.mean( arrow, axis = 0 ) + arrow_center

def length_arrow( vp, points, bar_shift = None, label = '', va = 'center', ha = 'center', relative_arrow_pos = 0.75, relative_text_pos = 1.25, show_bounds = True, color = 'k', bar_linestyle = '--' ) :

    if bar_shift is None :
        bar_shift = np.array([0]*3)

    points_arrow = points + relative_arrow_pos*bar_shift

    matplotlib_pyplot.annotate(
        '', xy=vp.project_on_screen(points_arrow[0]), xycoords='data',
        xytext=vp.project_on_screen(points_arrow[1]), textcoords='data',
        arrowprops={'arrowstyle': '<->'})

    if show_bounds :
        for tip in points :
            vp.plot_points( [ tip, tip + bar_shift ], color = color, linestyle = bar_linestyle )

    vp.text( np.mean( points, axis = 0 ) + relative_text_pos*bar_shift, label, color = color, va = va, ha = ha )

def translate( list_of_points, vector ) :
    return list( map( lambda x: np.array(x) + vector, list_of_points ) )

#####################
#
# try it
#
#####################

if __name__ == '__main__':

    from pylab import *

    latitude = 0.8*np.pi/2.; longitude = -.1*np.pi/2

    vp = viewpoint( latitude, longitude )

    #####################
    #prepare_figure
    # frame of reference
    #
    #####################

    vp.show_reference_frame( )

    #####################
    #
    # patch
    #
    #####################

    l = 3.
    square_long = np.pi/4.
    square_center = np.array([0,1.5,1.5])

    the_square = np.array( [ square_center , square_center + l*np.array( [ np.cos( square_long ), np.sin( square_long ), 0 ] ), square_center +  l*np.array( [ np.cos( square_long ), np.sin( square_long ), 1 ] ), square_center + np.array( [ 0., 0., l ] ) ] )

    ref_square =  subspace_2D( the_square )
    vp.plot_subspace_ref( ref_square )
    projected_square = ref_square.import_points( the_square)
    projected_barycenter = np.mean( projected_square, axis = 0 )

    vp.plot_points( the_square, marker = 'o', color = 'C1' )
    vp.plot_points( translate( the_square, array([0,-.5,0]) ), 'o', color = 'C4'  )
    vp.plot_patch( the_square, color = 'C2', alpha = .1 )

    vp.plot_points( ref_square.export_points( [ projected_barycenter ] ), color = 'tab:red', marker = '+'  )

    matplotlib_pyplot.axis('equal')
    matplotlib_pyplot.show()
