import argparse
import numpy as np
from .escape_plan import escape
from .escape_points import fibonacci_spheres, points_on_cube_surface
import multiprocessing
from tqdm import tqdm


def esc(args):
    return escape(*args)


def run_simulations(D, v, a, s, p, N, dt, cpu):

    pores = fibonacci_spheres(
        p, v) if s == 'sphere' else points_on_cube_surface(p, v)
    arguments = [(D, v, a, pores, dt, None, s) for i in range(N)]
    with multiprocessing.Pool(processes=cpu) as pool:
        res = list(tqdm(pool.imap(esc, arguments), total=N))
    return res


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-D', help='Diffusion coefficient')
    parser.add_argument('-v', help='Container volume')
    parser.add_argument('-a', help='Escape pore area size')
    parser.add_argument(
        '-s', help='Shape to escape (cube or sphere)', default='cube')
    parser.add_argument('-p', help='Number of pores', default=1)
    parser.add_argument(
        '-N', help='Number of simulations to run', default=1)
    parser.add_argument(
        '-dt', help='Difference in time to use', default=3e-8)
    parser.add_argument(
        '--cpu', help='Number of cores to use', default=1)
    parser.add_argument(
        '-o', help='Output file', default="./results.csv")
    args = parser.parse_args()
    args = vars(args)
    D, v, a, s, p, n, dt, cpu = float(args['D']), float(args['v']), float(
        args['a']), str(args['s']), int(args['p']), int(args['N']), float(args['dt']), int(args['cpu'])

    res = run_simulations(D, v, a, s, p, n, dt, cpu)
    print(np.mean(res))
    np.savetxt(args['o'], np.array(res).flatten(), delimiter=',')


if __name__ == '__main__':
    main()
