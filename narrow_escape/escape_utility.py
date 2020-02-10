import numpy as np


def sphere_vol_to_r(v): return (3*v/(4*np.pi))**(1/3)


def cube_vol_to_r(v): return np.cbrt(v)


def calculate_delta(D, dt): return np.sqrt(6*D*dt)


def calculate_opt_dt(a, D): return (a*0.1) / (6*D)
