import numpy as np
from scipy.spatial.distance import euclidean
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


def sample_in_hull(hull, npts=100):

    def sample(npts):
        xmin, xmax = hull.points[:, 0].min(), hull.points[:, 0].max()
        ymin, ymax = hull.points[:, 1].min(), hull.points[:, 1].max()
        zmin, zmax = hull.points[:, 2].min(), hull.points[:, 2].max()

        Xs = np.random.uniform(low=xmin, high=xmax, size=npts)
        Ys = np.random.uniform(low=ymin, high=ymax, size=npts)
        Zs = np.random.uniform(low=zmin, high=zmax, size=npts)

        stacked = np.zeros((npts, 3))
        stacked[:, 0] = Xs
        stacked[:, 1] = Ys
        stacked[:, 2] = Zs

        mask = np.ones(npts).astype('bool')
        for idx, p in enumerate(stacked):
            if not in_polygon(p, hull):
                mask[idx] = 0
        stacked = stacked[mask]
        return stacked

    stacked = sample(npts)
    while len(stacked) < npts:
        stacked = np.concatenate((stacked, sample(npts)))

    return stacked[:npts]


def random_points_on_hull(hull, npts=1, samples=100):
    pts = []
    delta = calculate_delta(400, 1e-6)
    sampled = []
    start_pos = sample_in_hull(hull, npts=samples)
    for i in range(samples):
        cur_pos = start_pos[i]
        while(in_polygon(cur_pos, hull)):
            cur_pos = travel(delta, cur_pos)
        sampled.append(cur_pos)

    NSections = 11
    p0 = hull.max_bound
    maxDist = euclidean(p0, hull.min_bound)
    ranges = np.linspace(0, maxDist, num=NSections)

    for pt in range(npts):
        ptsSelection = []
        np.random.shuffle(sampled)
        for mi, ma in zip(ranges[:-1], ranges[1:]):
            for p1 in sampled:
                dist = euclidean(p0, p1)
                if mi < dist < ma:
                    ptsSelection.append(p1)
                    break
        np.random.shuffle(ptsSelection)
        pts.append(ptsSelection[0])

    return pts, sampled


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
    cbrt_diff = np.cbrt(vol/volN)
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
