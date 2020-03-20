from PyEscape.escape_plan import escape
from PyEscape.escape_points import fibonacci_spheres, points_on_cube_surface
from PyEscape.escape_utility import sphere_vol_to_r
import pytest
import numpy as np


@pytest.mark.timeout(60)
def test_escape():
    D = 400
    v = 1
    a = 0.1
    r = sphere_vol_to_r(v)
    pores = fibonacci_spheres(1, r)
    t = escape(D, v, a, pores)
    assert t



@pytest.mark.timeout(60)
def test_escape_cube():
    D = 400
    v = 1
    a = 0.1
    r = sphere_vol_to_r(v)
    pores = points_on_cube_surface(1, r)
    t = escape(D, v, a, pores, shape='cube')
    assert t

@pytest.mark.timeout(120)
def test_avg_escape_sphere_time():
    N = 50
    D = 400
    v = 1
    a = 0.1
    r = sphere_vol_to_r(v)
    pores = points_on_cube_surface(1, r)
    ts = np.mean([escape(D, v, a, pores, shape='cube') for _ in range(N)])
    assert 0.01 < ts < 0.1

def test_timeout():
    D = 400
    v = 1
    a = 0.1
    r = sphere_vol_to_r(v)
    pores = points_on_cube_surface(1, r)
    t = escape(D, v, a, pores, shape='cube', max_steps=(1))
    assert int(t) == 0

def test_timeout_from_dt():
    D = 400
    v = 1
    a = 0.1
    r = sphere_vol_to_r(v)
    pores = points_on_cube_surface(1, r)
    t = escape(D, v, a, pores, shape='cube', max_steps=(1e3), dt=1)
    assert int(t) == 0
