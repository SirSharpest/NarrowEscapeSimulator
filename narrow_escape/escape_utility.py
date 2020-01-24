import numpy as np


def sphere_vol_to_r(v): return (3*v/(4*np.pi))**(1/3)
def cube_vol_to_r(v): return np.cbrt(v)
def calculate_delta(D, dt): return 6*D*dt
