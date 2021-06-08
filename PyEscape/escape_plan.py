import numpy as np
from .escape_utility import sphere_vol_to_r, cube_vol_to_r, calculate_delta
from .escape_utility import calculate_opt_dt, vol_ellipsoid
from .escape_detection import in_sphere, in_cube, in_polygon, in_ellipsoid
from .escape_detection import passthrough_pore
MAX_NEW_MOVEMENTS = 100


def travel(delta,  pa):
    """Find a new position for a particle

    Takes a delta, movement size and a particle of N dimensions returns a new
    array of similar dimensions to pa.

    """

    p = pa.copy()
    xyz = np.random.random(p.shape)
    xyz_sum = np.sum(xyz)
    xyz = np.sqrt(xyz / xyz_sum) * delta * \
        np.random.choice([-1, +1], p.shape)
    p += xyz
    return p


def escape_with_path(r, delta, dt, max_steps,
                     pore_locs, pore_size, check_func, cur_pos):
    """Provides the full path of a particle as it escapes from a container

    Takes a radius of container, delta step size, dt difference of time, a
    shape (cube of sphere), a maximum number of steps to allow, location of
    escape pore(s), size of escape pore(s), a checking function for collision
    and the current position of the particle

    returns a multi-dimensional array of a particle at each position as it
    escapes the container will return if max steps is reached or when escape is
    detected

    """
    path = np.zeros((max_steps, 3))
    path[0] = cur_pos
    steps = 0
    while steps < max_steps:

        new_pos_steps = 0
        new_pos = travel(delta, cur_pos)
        steps = steps + 1
        while (not (check_func(new_pos, r)) and new_pos_steps < MAX_NEW_MOVEMENTS):
            for pd_loc in pore_locs:
                if passthrough_pore(new_pos, pd_loc, r=pore_size):
                    path[steps] = new_pos
                    return path[:steps]
            new_pos = travel(delta, cur_pos)
            new_pos_steps += 1

        cur_pos = new_pos
        path[steps] = cur_pos
    return path[:steps] if steps < max_steps else np.zeros(path.shape)


def escape(D, vol, pore_size, pore_locs, dt=None, seed=None,
           shape='sphere', hull=None, ABC=None, max_steps=(int(1e7)), with_path=False,
           random_start=False, tol=1):
    """Wrapper function that can be called by a user - used to optimise code
    shared between escape methods

    Takes a diffusion coefficent, volume of container, escape pore size, escape
    pore(s) location. Optional arguments of step-size and a numpy random seed
    can be given, as well as specifying maximum number of steps that a walk can
    take. Switches to return the full path (or just the time required), to
    start the particle at the container centroid or random placement


    """
    if dt is None:
        dt = calculate_opt_dt(pore_size, D)
    delta = calculate_delta(D, dt)
    if seed is not None:
        np.random.seed(seed)
    else:
        np.random.seed()
    max_steps = (int(1/dt) if max_steps is None else max_steps)

    if shape == 'sphere':
        check_func = in_sphere
        r = sphere_vol_to_r(vol)
    elif shape == 'cube':
        check_func = in_cube
        r = cube_vol_to_r(vol)
    elif shape == 'ellipsoid':
        if ABC is None:
            raise NameError("Argument 'ABC' is undefined")
        ABC = np.array(ABC).astype('float64')
        volN = vol_ellipsoid(*ABC)
        cbrt_diff = vol/np.cbrt(volN)
        a, b, c = np.array(ABC * cbrt_diff)

        def ellipsoid_wrapper(p, r):
            return in_ellipsoid(p[0], p[1], p[2], a, b, c)
        check_func = ellipsoid_wrapper
        r = 0

    elif shape == 'polygon':
        check_func = in_polygon
        if hull is None:
            raise NameError("Argument 'hull' is undefined")
        r = hull

    cur_pos = np.zeros(3)

    if with_path:
        return escape_with_path(r, delta, dt,
                                max_steps, pore_locs,
                                pore_size, check_func, cur_pos)

    return escape_quick(r, delta, dt,
                        max_steps, pore_locs,
                        pore_size, check_func, cur_pos, tol)


def escape_quick(r, delta, dt, max_steps,
                 pore_locs, pore_size, check_func, cur_pos, tol):
    """Simulates escape without tracking position through container

    Takes a radius of container, delta step size, dt difference of time, a
    shape (cube of sphere), a maximum number of steps to allow, location of
    escape pore(s), size of escape pore(s), a checking function for collision
    and the current position of the particle

    returns a number of steps taken to escape

    """
    steps = 0
    while steps < max_steps:
        new_pos = travel(delta, cur_pos)
        new_pos_steps = 0
        while (not (check_func(new_pos, r)) and new_pos_steps < MAX_NEW_MOVEMENTS):
            new_pos = travel(delta, cur_pos)
            new_pos_steps += 1
            for pd_loc in pore_locs:
                if passthrough_pore(new_pos, pd_loc, r=pore_size, tol=tol):
                    return (steps+1)*dt
        cur_pos = new_pos
        steps = steps + 1
    return steps*dt if steps < max_steps else 0
