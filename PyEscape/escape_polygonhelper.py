from scipy.spatial import ConvexHull
import numpy as np


def isolate_points_from_segmented_imagestack(img_stack, i, scaleX=1, scaleY=1, scaleZ=1):
    """Given a segmented 3 dimensional image isolate points of the
    polygon to escape from

    returns only points of interest as 3D coordinates
    """
    return np.array(list(zip(*np.where(img_stack == i)))).astype('float64') * \
        [scaleX, scaleY, scaleZ]


def scale_voxel_points(pts, Xs, Ys, Zs, Tv):
    pts_n = pts * [Xs. Ys, Zs]
    h = ConvexHull(pts_n)
    V = h.volume  # True volume


def make_hull_and_scale(pts, V_t=1):
    """Given a list of points this calculates the convex hull, centres it
    on 0,0,0 and scales to target volume

    returns a convex hull and list of points
    """
    pts = pts.astype('float64')
    hull = ConvexHull(pts)
    V = hull.volume
    cx = np.mean(hull.points[hull.vertices, 0])
    cy = np.mean(hull.points[hull.vertices, 1])
    cz = np.mean(hull.points[hull.vertices, 2])
    pts -= [cx, cy, cz]
    scaling_f = np.cbrt(V_t/V)
    pts_c = pts*scaling_f
    hull_c = ConvexHull(pts_c)
    return hull_c, pts_c
