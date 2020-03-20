def escape_en_mass(check_func, N=1000, delta=1, r=1):
    def mass_travel(delta, pa):
        """Find a new position for a particle

        Takes a delta, movement size and a particle of N dimensions
        returns a new array of similar dimensions to pa.

        """
        p = pa.copy()
        xyz = np.random.random(p.shape)
        xyz_sq_sum = np.sum(xyz**2)
        xyz = np.sqrt(xyz**2 / xyz_sq_sum) * delta * \
            np.random.choice([-1, +1], p.shape)
        p += xyz
        return p

    particles = np.zeroes(N, 3)

    def check_helper(x): return check_func(x, r)
    escape_times = []

    while len(particles):
        new_particle_pos = mass_travel(delta, particles)
        boundary_idx = np.apply_along_axis(
            lambda x: check_helper, 1, new_particle_pos)

        while len(boundary_idx):
            pass

        # TODO:
