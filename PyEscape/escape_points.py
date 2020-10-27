import numpy as np
from .escape_utility import sphere_vol_to_r


def make_clusters(nclusters, npointspercluster, v=1, r=0.1, jitter=0.1):

    cluster_points = fibonacci_spheres(samples=nclusters, v=v)
    clusters = []
    for ic in cluster_points:
        jit = np.random.normal(r, (1+jitter)*r, (3, npointspercluster))
        points = ic * (1+jit)
        points /= np.linalg.norm(points, axis=0)
        points *= sphere_vol_to_r(v)
        clusters.append(points)
    return clusters


def fibonacci_spheres(samples=1, v=1, randomize=True, r=0):
    """Produces pseudo-evenly distributed points on the surface
    of a sphere

    Optional arguments give the number of points to return, volume
    of the sphere and to randomize the points initial positions.

    returns 3D coordinates of specified number of points
    """
    radius = sphere_vol_to_r(v) - r
    rnd = 1 if randomize is False else np.random.randint(10)
    points = []
    offset = 2./samples
    increment = np.pi * (3. - np.sqrt(5.))
    for i in range(samples):
        y = ((i * offset) - 1) + (offset / 2)
        r = np.sqrt(1 - pow(y, 2))
        phi = ((i + rnd) % samples) * increment
        x = np.cos(phi) * r
        z = np.sin(phi) * r
        z = z * radius
        y = y * radius
        x = x * radius
        points.append(np.array([x, y, z]))
    return points


def points_on_cube_surface(samples, r=1):
    """Gives a random distribution of points on a cube surface

    A number of samples and an optional cube radius can be given

    returns a series of points randomly distributed on surface of cube
    """
    points = []
    r = np.cbrt(r)
    for i in range(samples):
        p = np.random.random(3) * (r/2) * \
            np.random.choice([-1, 1])
        dim = np.random.choice([0, 1, 2])
        p[dim] = (r/2) * np.random.choice([-1, 1])
        points.append(p)
    return points
