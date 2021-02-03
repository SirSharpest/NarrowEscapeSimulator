import numpy as np


def sphere_vol_to_r(v):
    """Finds radius from a sphere's volume

    returns radius of sphere
    """
    return (3*v/(4*np.pi))**(1/3)


def vol_ellipsoid(a, b, c):
    """
    Calculates volume of ellipsoid
    """
    return 4/3*np.pi*a*b*c


def cube_vol_to_r(v):
    """Calculates cube radius from it's volume

    returns radius of cube
    """
    return np.cbrt(v)


def calculate_delta(D, dt):
    """Calculates appropriate step-size for a diffusion coefficient

    returns the step-size for a random-walk particle to take per dt
    """
    return np.sqrt(6*D*dt)


def calculate_opt_dt(a, D):
    """Calculates the optimal dt based on size of pore
    and diffusion coefficent

    returns a value for dt
    """
    return (a*1e-3) / (6*D)
