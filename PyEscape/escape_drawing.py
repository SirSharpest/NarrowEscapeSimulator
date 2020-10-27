from itertools import product, combinations
import numpy as np
from .escape_utility import sphere_vol_to_r, cube_vol_to_r

import matplotlib.pyplot as plt


def set_axes_equal(ax: plt.Axes):
    """Set 3D plot axes to equal scale.
    Functions from @Mateen Ulhaq and @karlo

    Make axes of 3D plot have equal scale so that spheres appear as
    spheres and cubes as cubes.  Required since `ax.axis('equal')`
    and `ax.set_aspect('equal')` don't work on 3D.
    """
    limits = np.array([
        ax.get_xlim3d(),
        ax.get_ylim3d(),
        ax.get_zlim3d(),
    ])
    origin = np.mean(limits, axis=1)
    radius = 0.5 * np.max(np.abs(limits[:, 1] - limits[:, 0]))
    _set_axes_radius(ax, origin, radius)


def _set_axes_radius(ax, origin, radius):
    x, y, z = origin
    ax.set_xlim3d([x - radius, x + radius])
    ax.set_ylim3d([y - radius, y + radius])
    ax.set_zlim3d([z - radius, z + radius])


def draw_sphere(v, ax):
    """Draws a sphere on an axis

    Sphere volume and axis to draw on need to be specified

    ax must be a 3D axis
    """
    r = sphere_vol_to_r(v)
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = r * np.outer(np.cos(u), np.sin(v))
    y = r * np.outer(np.sin(u), np.sin(v))
    z = r * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z,  rstride=4, cstride=4,
                    color='r', linewidth=0.1, alpha=0.1)
    set_axes_equal(ax)


def draw_cube(v, ax):
    """Draws a cube on axis

    Cube volume and axis to draw on need to be specified

    ax must be a 3D axis
    """
    r = cube_vol_to_r(v)
    r = [-r/2, r/2]
    for s, e in combinations(np.array(list(product(r, r, r))), 2):
        if np.sum(np.abs(s-e)) == r[1]-r[0]:
            ax.plot3D(*zip(s, e), color="r")
    set_axes_equal(ax)
