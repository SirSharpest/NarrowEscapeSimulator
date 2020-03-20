from PyEscape.escape_points import fibonacci_spheres, points_on_cube_surface
from PyEscape.escape_detection import in_sphere, in_cube
from PyEscape.escape_utility import sphere_vol_to_r


V = 1
P = 1
eps = .001 * V 

def test_fibo_spheres_inside():

    assert in_sphere(fibonacci_spheres(P, V)[0], sphere_vol_to_r(V+eps))

def test_fibo_spheres_outside():
    assert in_sphere(fibonacci_spheres(P, V)[0], sphere_vol_to_r(V-eps)) == False

def test_ponts_on_cube_inside():
    assert in_cube(points_on_cube_surface(P, V)[0], V+eps)

def test_ponts_on_cube_outside():
    assert in_cube(points_on_cube_surface(P, V)[0], V-eps) == False
