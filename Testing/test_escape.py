from PyEscape.escape_plan import escape
from PyEscape.escape_points import fibonacci_spheres, points_on_cube_surface
from PyEscape.escape_utility import sphere_vol_to_r
from PyEscape.escape_points import random_points_on_hull
from PyEscape.escape_points import random_points_on_ellipsoid
from PyEscape.escape_polygonhelper import make_hull_and_scale
import pytest
import numpy as np


def test_escape():
    D = 400
    v = 1
    a = 0.1
    r = sphere_vol_to_r(v)
    pores = fibonacci_spheres(1, r)
    t = escape(D, v, a, pores, dt=1e-6)
    assert t


def test_escape_cube():
    D = 400
    v = 1
    a = 0.1
    r = sphere_vol_to_r(v)
    pores = points_on_cube_surface(1, r)
    t = escape(D, v, a, pores, shape='cube', dt=1e-6)
    assert t


def test_escape_ellipsoid():
    D = 400
    v = 1
    a = 0.1
    ABC = [3, 2, 1]
    pores = random_points_on_ellipsoid(ABC, v)
    t = escape(D, v, a, pores, shape='ellipsoid', dt=1e-6, ABC=ABC)
    assert t


def test_avg_escape_sphere_time():
    N = 10
    D = 400
    v = 1
    a = 0.1
    r = sphere_vol_to_r(v)
    pores = fibonacci_spheres(1, r)
    ts = np.mean([escape(D, v, a, pores, dt=1e-6) for _ in range(N)])
    assert 0.001 < ts < 1


def test_timeout():
    D = 400
    v = 1
    a = 0.1
    r = sphere_vol_to_r(v)
    pores = fibonacci_spheres(1, r)
    t = escape(D, v, a, pores, dt=1e-6)
    assert int(t) == 0


def test_timeout_from_dt():
    D = 400
    v = 1
    a = 0.1
    r = sphere_vol_to_r(v)
    pores = fibonacci_spheres(1, r)
    t = escape(D, v, a, pores, max_steps=5, dt=1e-6)
    assert int(t) == 0


def test_escape_polygon():
    D = 400
    v = 1
    a = 0.1
    hull, _ = make_hull_and_scale(np.random.random((10, 3)))
    pores = random_points_on_hull(hull)
    t = escape(D, v, a, pores, dt=1e-6, hull=hull, shape='polygon')
    assert t
