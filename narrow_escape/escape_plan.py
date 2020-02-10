import numpy as np
from .escape_utility import sphere_vol_to_r, cube_vol_to_r, calculate_delta, calculate_opt_dt
from .escape_detection import in_sphere, in_cube, passthrough_pore, passthrough_flat_pore


def travel(delta, pa):
    p = pa.copy()
    xyz = np.random.random(p.shape)
    xyz_sq_sum = np.sum(xyz**2)
    xyz = np.sqrt(xyz**2 / xyz_sq_sum) * delta * \
        np.random.choice([-1, +1], p.shape)
    p += xyz
    return p


def escape_with_path(r, delta, dt, shape, max_steps,
                     pore_locs, pore_size, check_func, cur_pos):
    path = np.zeros((max_steps, 3))
    path[0] = cur_pos
    steps = 0
    while steps < max_steps:
        new_pos = travel(delta, cur_pos)
        steps = steps + 1
        while (not (check_func(new_pos, r))):
            for pd_loc in pore_locs:
                if passthrough_pore(new_pos, pd_loc, r=pore_size):
                    path[steps] = new_pos
                    return path[:steps]
            new_pos = travel(delta, cur_pos)
        cur_pos = new_pos
        path[steps] = cur_pos
    return path[:steps]


def escape(D, vol, pore_size, pore_locs,
           dt=None, seed=None, shape='sphere',
           max_steps=(int(1e7)), with_path=False, random_start=False, flat=False):
    if dt is None:
        dt = calculate_opt_dt(pore_size, D)
    delta = calculate_delta(D, dt)
    if seed is not None:
        np.random.seed(seed)
    else:
        np.random.seed()

    max_steps = (int(1/dt) if max_steps is None else max_steps)
    check_func = in_sphere if shape == 'sphere' else in_cube
    r = sphere_vol_to_r(vol) if shape == 'sphere' else cube_vol_to_r(vol)

    if random_start:
        cur_pos = np.random.random(3) * (r/2) * np.random.choice([-1, +1], 3)
    else:
        cur_pos = np.zeros(3)

    if with_path:
        return escape_with_path(r, delta, dt,
                                shape, max_steps, pore_locs,
                                pore_size, check_func, cur_pos)
    elif flat:
        return escape_flat(r, delta, dt,
                           shape, max_steps, pore_locs,
                           pore_size, check_func, cur_pos)
    else:
        return escape_quick(r, delta, dt,
                            shape, max_steps, pore_locs,
                            pore_size, check_func, cur_pos)


def escape_flat(r, delta, dt, shape, max_steps,
                pore_locs, pore_size, check_func, cur_pos):
    """
    Removed tracking to optimise speed
    """
    check_func = in_sphere if shape == 'sphere' else in_cube
    steps = 0
    while steps < max_steps:
        new_pos = travel(delta, cur_pos)
        while (not (check_func(new_pos, r))):
            for pd_loc in pore_locs:
                if passthrough_flat_pore(new_pos, pd_loc, r=pore_size):
                    return (steps+1)*dt
            new_pos = travel(delta, cur_pos)
        cur_pos = new_pos
        steps = steps + 1
    return steps*dt


def escape_quick(r, delta, dt, shape, max_steps,
                 pore_locs, pore_size, check_func, cur_pos):
    """
    Removed tracking to optimise speed
    """
    check_func = in_sphere if shape == 'sphere' else in_cube
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
