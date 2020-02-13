import numpy as np


def in_sphere(p, r, p0=np.array([0, 0, 0])):
    """Checks if a particle p is in a sphere with radius r

    Optional arguments of p0 is the offset of the container

    returns True if p is in p0
    """
    return np.sum((p-p0)**2) < r**2


def in_circle(x, y, a=0, b=0, r=25):
    """Check if 2D coordinates are within a circle

    Optional arguments offset the circle's centre and specify radius

    returns True if x,y is in circle of position a,b and radius r
    """
    return (x - a)*(x - a) + (y - b)*(y - b) < r**2


def in_cube(p, r=1):
    """Checks if point is in a centroid cube

    Optional argument of radius (diameter) of cube

    returns True if p is in specified cube
    """
    r = r/2
    return not (np.any(np.logical_or(p <= -r, p >= r)))


def passthrough_pore(p, p0, r=1):
    """Checks if a point has entered the escape zone of a pore p0

    Optional arguments of r size

    returns True if p is within p0
    """
    return in_sphere(p, r, p0=p0)


def passthrough_flat_pore(p, p0, r=1):
    """Checks if a point has entered escape zone of a pore,
    flat to the surface of shape

    Optional arguments of r size
    """
    if (p0[2] - r) > p[2] < (p0[2] + r):
        return in_circle(p[0], p[1], a=p0[0], b=p0[1], r=r)
    else:
        False
