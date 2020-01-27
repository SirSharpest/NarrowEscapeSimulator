import numpy as np
from .escape_utility import sphere_vol_to_r, cube_vol_to_r, calculate_delta
from .escape_detection import in_sphere, in_cube, passthrough_pore


def travel(delta, pa):
    p = pa.copy()
    xy = np.random.random(p.shape)
    xy = np.sqrt(xy/xy.sum() * delta) * np.random.choice([-1, +1], p.shape)
    p += xy
    return p


def escape_with_path(D, vol, pd_size, pore_locs, dt=1e-7, seed=None,
                     shape='sphere', max_tries=None):
    delta = calculate_delta(D, dt)
    if seed is not None:
        np.random.seed(seed)
    else:
        np.random.seed()
    max_tries = (int(1/dt) if max_tries is None else max_tries)
    particle = np.zeros(3)
    path = np.zeros((max_tries, 3))
    path[0] = particle
    tries = 0
    cur_pos = path[0]
    check_func = in_sphere if shape == 'sphere' else in_cube
    r = sphere_vol_to_r(vol) if shape == 'sphere' else cube_vol_to_r(vol)
    while tries < max_tries:
        new_pos = travel(delta, cur_pos)
        tries = tries + 1
        while (not (check_func(new_pos, r))):
            for pd_loc in pore_locs:
                if passthrough_pore(new_pos, pd_loc, r=pd_size):
                    path[tries] = new_pos
                    return path[:tries]
            new_pos = travel(delta, cur_pos)
        cur_pos = new_pos
        path[tries] = cur_pos
    return path[:tries]


def escape(D, vol, pore_size, pore_locs, dt=1e-7,
           seed=None, shape='sphere', max_steps=int(1e7)):
    """
    Removed tracking to optimise speed
    """
    delta = calculate_delta(D, dt)
    if seed is not None:
        np.random.seed(seed)
    else:
        np.random.seed()
    cur_pos = np.zeros(3)
    check_func = in_sphere if shape == 'sphere' else in_cube
    r = sphere_vol_to_r(vol) if shape == 'sphere' else cube_vol_to_r(vol)
    steps = 0
    while steps < max_steps:
        new_pos = travel(delta, cur_pos)
        while (not (check_func(new_pos, r))):
            for pd_loc in pore_locs:
                if passthrough_pore(new_pos, pd_loc, r=pore_size):
                    return (steps+1)*dt
            new_pos = travel(delta, cur_pos)
        cur_pos = new_pos
        steps = steps + 1
    return steps*dt
