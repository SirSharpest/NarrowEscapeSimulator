import numpy as np


def in_sphere(p, r, p0=np.array([0, 0, 0])):
    return np.sum((p-p0)**2) < r**2


def in_circle(x, y, a=0, b=0, r=25):
    return (x - a)*(x - a) + (y - b)*(y - b) < r**2


def in_cube(p, r=1):
    r = r/2
    return not (np.any(np.logical_or(p <= -r, p >= r)))


def passthrough_pore(p, p0, r=1):
    return in_sphere(p, r, p0=p0)


def passthrough_flat_pore(p, p0, r=1):
    if (p0[2] - r) > p[2] < (p0[2] + r):
        return inside_circle(p[0], p[1], a=p0[0], b=p0[1], r=r)
    else:
        False


def inside_circle(x, y, a=0, b=0, r=25):
    return (x - a)*(x - a) + (y - b)*(y - b) < r**2
