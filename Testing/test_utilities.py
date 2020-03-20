from PyEscape.escape_utility import sphere_vol_to_r, cube_vol_to_r, calculate_delta, calculate_opt_dt
import numpy.testing as npt


def test_cube_vol_to_r():
    npt.assert_almost_equal(cube_vol_to_r(1), 1.0, decimal=5)


def test_sphere_vol_to_r():
    npt.assert_almost_equal(sphere_vol_to_r(1), 0.62035, decimal=5)


def test_calc_delta():
    npt.assert_almost_equal(calculate_delta(400, 1e-8), 0.004898979485566357, decimal=5)


def test_opt_dt():
    npt.assert_almost_equal(calculate_opt_dt(0.1, 400), 4.166666666666668e-06, decimal=5)
