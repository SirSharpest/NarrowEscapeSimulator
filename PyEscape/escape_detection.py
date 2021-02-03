import numpy as np
from scipy.spatial import ConvexHull


def in_sphere(p, r, p0=None):
    """Checks if a particle p is in a sphere with radius r

    Optional arguments of p0 is the offset of the container

    returns True if p is in p0
    """
    if p0 is None:
        return sum(p**2) < r * r
    return sum((p-p0)**2) < r * r


def in_circle(x, y, a=0, b=0, r=25):
    """Check if 2D coordinates are within a circle

    Optional arguments offset the circle's centre and specify radius

    returns True if x,y is in circle of position a,b and radius r
    """
    x -= a
    y -= b
    return x * x + y * y < r * r


def in_cube(p, r=1):
    """Checks if point is in a centroid cube

    Optional argument of radius (diameter) of cube

    returns True if p is in specified cube
    """
    r = r/2
    return not any(np.logical_or(p <= -r, p >= r))


def in_ellipsoid(x, y, z, a, b, c): return (
    (x**2/a**2) + (y**2/b**2) + (z**2/c**2)) < 1


def passthrough_pore(p, p0, r=1, tol=0.9):
    """Checks if a point has entered the escape zone of a pore p0

    Optional arguments of r size

    Optional extra argument of tol, adds a tolerance factor
    for error

    returns True if p is within p0
    """
    if np.linalg.norm(p-p0) < r*tol:
        return True
    else:
        return False


def passthrough_flat_pore(p, p0, r=1):
    """Checks if a point has entered escape zone of a pore,
    flat to the surface of shape
    Optional arguments of r size
    """
    if -r < p[2] - p0[2] < r:
        return in_circle(p[0], p[1], a=p0[0], b=p0[1], r=r)
    else:
        return False


def in_polygon(p, hull):
    """Checks if p is within a convex hull"""
    new_hull = ConvexHull(np.concatenate((hull.points, [p])))
    if np.array_equal(new_hull.vertices, hull.vertices):
        return True
    return False
