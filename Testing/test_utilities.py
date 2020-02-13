import pytest
import numpy as np
from narrow_escape.escape_utility import sphere_vol_to_r, cube_vol_to_r, calculate_delta, calculate_opt_dt


def test_cube_vol_to_r():
    assert cube_vol_to_r(1) == 1.0


def test_sphere_vol_to_r():
    assert np.around(sphere_vol_to_r(1), 2) == 0.62


def test_calc_delta():
    assert calculate_delta(400, 1e-8) == 0.004898979485566357


def test_opt_dt():
    assert calculate_opt_dt(0.1, 400) == 4.166666666666668e-06
