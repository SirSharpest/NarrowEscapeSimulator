from scipy.spatial import ConvexHull
import numpy as np


def isolate_points_from_segmented_imagestack(img_stack, i):
    """Given a segmented 3 dimensional image isolate points of the
    polygon to escape from

    returns only points of interest as 3D coordinates
    """
    return np.array(list(zip(*np.where(img_stack == i))))


def make_hull_and_scale(pts, V_t=1):
    """Given a list of points this calculates the convex hull, centres it
    on 0,0,0 and scales to target volume

    returns a convex hull and list of points
    """
    hull = ConvexHull(pts)
    V = hull.volume
    cx = int(np.mean(hull.points[hull.vertices, 0]))
    cy = int(np.mean(hull.points[hull.vertices, 1]))
    cz = int(np.mean(hull.points[hull.vertices, 2]))
    pts -= [cx, cy, cz]
    scaling_f = np.cbrt(V_t/V)
    pts_c = pts*scaling_f
    hull_c = ConvexHull(pts_c)
    return hull_c, pts_c
