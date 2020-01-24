import pytest
import numpy as np
from narrow_escape.escape_plan import escape
from narrow_escape.escape_points import fibonacci_spheres, points_on_cube_surface
from narrow_escape.escape_utility import sphere_vol_to_r, calculate_delta


def test_escape():
    D = 400
    v = 1
    a = 0.1
    r = sphere_vol_to_r(v)
    pores = fibonacci_spheres(1, r)
    t = escape(D, v, a, pores)
    assert t < 1


def test_escape_cube():
    D = 400
    v = 1
    a = 0.1
    r = sphere_vol_to_r(v)
    pores = points_on_cube_surface(1, r)
    t = escape(D, v, a, pores, shape='cube')
    assert t < 1
