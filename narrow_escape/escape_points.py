import numpy as np
from .escape_utility import sphere_vol_to_r


def fibonacci_spheres(samples=1, v=1, randomize=True):
    radius = sphere_vol_to_r(v)
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
    points = []
    r = np.cbrt(r)
    for i in range(samples):
        p = np.random.random(3) * (r/2) * \
            np.random.choice([-1, 1])
        dim = np.random.choice([0, 1, 2])
        p[dim] = (r/2) * np.random.choice([-1, 1])
        points.append(p)
    return points
