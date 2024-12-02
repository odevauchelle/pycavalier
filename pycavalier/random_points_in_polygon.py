"""
Distributes points randomly on a polygon.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mplPath


def rand2d(npts, rectangle=np.array([[0, 0], [1., 1.]])):

    xmin, ymin = tuple(rectangle[0])
    xmax, ymax = tuple(rectangle[1])

    x = xmin + (xmax-xmin) * np.random.rand(npts)
    y = ymin + (ymax-ymin) * np.random.rand(npts)

    return np.array([x, y]).T


def rectangle_around_polygon(polygon):

    x, y = polygon[:, 0], polygon[:, 1]

    return np.array([[min(x), min(y)], [max(x), max(y)]])


def number_of_points(density, rectangle):

    xmin, ymin = tuple(rectangle[0])
    xmax, ymax = tuple(rectangle[1])

    area = (xmax-xmin) * (ymax-ymin)

    return int(density * area)


def random_points_in_polygon(polygon, density, rand2d=rand2d):

    rectangle = rectangle_around_polygon(polygon)

    npts = number_of_points(density, rectangle)

    if npts < 10:
        print('Warning random_points_in_polygon: total number of random points =', npts)

    cloud = rand2d(npts, rectangle=rectangle)

    in_polygon = mplPath.Path(polygon).contains_points(cloud)

    return list(cloud[in_polygon])


if __name__ == '__main__':

    theta = np.linspace(0, 2 * np.pi, 50)
    r = 1. + 0.2 * np.cos(5 * theta)

    polygon = np.array([r * np.cos(theta), r * np.sin(theta)]).T

    cloud = np.array(random_points_in_polygon(polygon, 10))

    print(cloud)

    fig, ax = plt.subplots(1, 1)

    ax.plot(cloud[:, 0], cloud[:, 1], '.')
    ax.plot(polygon[:, 0], polygon[:, 1])

    ax.set_aspect('equal')
    plt.show()
