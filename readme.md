# Narrow Escape Simulator

[![status](https://joss.theoj.org/papers/c47ec67686a14361072ed703a58bac15/status.svg)](https://joss.theoj.org/papers/c47ec67686a14361072ed703a58bac15)


This is a python 3 library which provides ready-made simulations for determining the average escape time for a Brownian particle out of a container.
Examples are provided in the `notebooks` folder.


This software can be used by anyone wanting to simulate how long a particle under Brownian motion will take to escape from a container with a number of escape pores on it's surface. This was developed with a cellular biology context, however usage in chemistry, physics and animal sciences could easily be imagined. This software is presented as easily modifiable.


## A note on running

This software can be run on a standard PC, we have tested for both OSX and Linux. However, running large numbers of simulations is best done on high-performance-computing equiment. This package is optimised for larger number of CPUs. Runnining on older/slower hardware may require additional time.

# As a command line app

To get results for a model with:

- Diffusion coefficient (D) of 400
- Volume (v) of 1um^3
- Pore area (a) of 0.1
- Number of pores (p) of 1
- Number of simulations (N) of 10

You can run:

``` bash
narrow_escape -D 400 -v 1 -a 0.1 -p 1 -N 1
```

For help type:

``` bash
narrow_escape --help
```


# To run as a python package


To get a single simulation result:

``` python
from narrow_escape.escape_plan import escape
from narrow_escape.escape_points import fibonacci_spheres, points_on_cube_surface


D = 400
v = 1
p = 1
a = 0.1
dt = 1e-6 # dt approaching 0 will take longer but give more accurate results

pores = fibonacci_spheres(p, v)

res = escape(D, v, a, pores, dt=dt)

print(res)

```

To get a more accurate value, multiple simulations are required e.g. :

``` python
from narrow_escape.escape_plan import escape
from narrow_escape.escape_points import fibonacci_spheres, points_on_cube_surface
import numpy as np

D = 400
v = 1
a = 0.1

pores = fibonacci_spheres(p, v)

res = [escape(D, v, a, pores, dt=dt) for i in range(100)]

res_mean = np.mean(res)

print(res_mean)

```

To extend this further, we much wish to multi-process to speed up simulations:
(tqdm is now used to monitor progress, can be removed!)

``` python
from narrow_escape.escape_plan import escape
from narrow_escape.escape_points import fibonacci_spheres, points_on_cube_surface
import numpy as np

D = 400
v = 1
a = 0.1
p = 1
N = 100
pores = fibonacci_spheres(p, v)


def esc(i):
    res = escape(D, v, a, pores, dt=dt)
    return res


with multiprocessing.Pool(processes=os.cpu_count()) as pool:
    res = list(tqdm.tqdm(pool.imap(esc, np.arange(0, N)), total=N))

res_mean = np.mean(res)

print(res_mean)

```


# Installation

In a conda environment (recommended) with python 3.6+ simply clone the repository and run:

``` bash
pip install .
```

If using base install of python (not recommended), you may want to run:

``` bash
pip install . --user
```

Running the examples notebook will require additional requirements which can be installed with:

``` bash
pip install jupyter tqdm
```

To run tests you will require the pytest-timeout module:

``` bash
pip install pytest-timeout
```

# Contributions

Any and all suggestions for improvements and feature additions are welcome. We ask that new features be requested with specific data, test case scenarios and desired outputs. Python code submitted for pull requests should be appropriately formatted to a PEP8 standard.

Bug reports and other issues can be made through the issues report feature of github.

Requests for collboration, or research based questions can be made to nathan.hughes@jic.ac.uk

# Acknowledgements

We thank Prof. Richard Morris for supervising and providing instrumental advice in the development of this research, Dr. Melissa Tomkins for help, advice and problem solving and BBSRC + Norwich Research Park Doctoral Training Programme for their funding and support.
