from PyEscape.escape_points import fibonacci_spheres, points_on_cube_surface
from PyEscape.escape_detection import in_sphere, in_cube

def test_points_in_sphere():
    assert in_sphere(fibonacci_spheres(1, 100)[0], 1) == False


def test_points_in_cube():
    assert in_cube(points_on_cube_surface(1, r=100)[0], r=1) == False
