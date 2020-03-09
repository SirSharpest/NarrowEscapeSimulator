from narrow_escape.escape_points import fibonacci_spheres, points_on_cube_surface
from narrow_escape.escape_detection import in_sphere, in_cube

def test_fibo_spheres():
    assert in_sphere(fibonacci_spheres(1, 1)[0], 1)


def test_ponts_on_cube():
    assert in_cube(points_on_cube_surface(1, 1)[0], 1.1)
