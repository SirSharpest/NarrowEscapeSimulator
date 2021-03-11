import numpy as np
from .escape_utility import sphere_vol_to_r, calculate_delta, vol_ellipsoid
from .escape_plan import travel
from .escape_detection import in_polygon, in_ellipsoid


def make_clusters(npointspercluster, nclusters=0, v=1, jitter=0.1, cluster_points=None):
    """
    Takes a number of points per cluster, option number of clusters and points and creates a random
    distribution of points on the surface of a cell

    returns a list of clusters and their associated points
    """

    if cluster_points is None:
        cluster_points = fibonacci_spheres(samples=nclusters, v=v)
    else:
        nclusters = len(cluster_points)
    clusters = []
    for ic in cluster_points:
        jit = np.random.normal(0, jitter, (3, npointspercluster))
        points = np.reshape(ic, (3, 1)) + jit
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


def random_points_on_hull(hull, npts=1):
    pts = []
    delta = calculate_delta(400, 1e-7)
    for i in range(npts):
        cur_pos = np.array([0., 0., 0.])
        while(in_polygon(cur_pos, hull)):
            cur_pos = travel(delta, cur_pos)
        pts.append(cur_pos)
    return pts


def random_point_ellipsoid(a, b, c):
    """
    This function is taken from stackoverflow user Nikolay Frick
    https://stackoverflow.com/a/61786434

    It is used with minor modification
    """

    u = np.random.rand()
    v = np.random.rand()
    theta = u * 2.0 * np.pi
    phi = np.arccos(2.0 * v - 1.0)
    sinTheta = np.sin(theta)
    cosTheta = np.cos(theta)
    sinPhi = np.sin(phi)
    cosPhi = np.cos(phi)
    rx = a * sinPhi * cosTheta
    ry = b * sinPhi * sinTheta
    rz = c * cosPhi
    return rx, ry, rz


def random_points_on_ellipsoid(ABC, vol=1, npts=1):
    pts = []
    ABC = np.array(ABC).astype('float64')
    volN = vol_ellipsoid(*ABC)
    cbrt_diff = vol/np.cbrt(volN)
    a, b, c = np.array(ABC * cbrt_diff)
    for i in range(npts):
        pts.append(random_point_ellipsoid(a, b, c))
    return pts


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
