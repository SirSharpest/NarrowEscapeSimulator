from numpy.linalg import eig, inv
from scipy.spatial import ConvexHull
import numpy as np
from .escape_utility import vol_ellipsoid


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


def ls_ellipsoid(xx, yy, zz):
    # finds best fit ellipsoid. Found at http://www.juddzone.com/ALGORITHMS/least_squares_3D_ellipsoid.html
    # least squares fit to a 3D-ellipsoid
    #  Ax^2 + By^2 + Cz^2 +  Dxy +  Exz +  Fyz +  Gx +  Hy +  Iz  = 1
    #
    # Note that sometimes it is expressed as a solution to
    #  Ax^2 + By^2 + Cz^2 + 2Dxy + 2Exz + 2Fyz + 2Gx + 2Hy + 2Iz  = 1
    # where the last six terms have a factor of 2 in them
    # This is in anticipation of forming a matrix with the polynomial coefficients.
    # Those terms with factors of 2 are all off diagonal elements.  These contribute
    # two terms when multiplied out (symmetric) so would need to be divided by two

    # change xx from vector of length N to Nx1 matrix so we can use hstack
    x = xx[:, np.newaxis]
    y = yy[:, np.newaxis]
    z = zz[:, np.newaxis]

    #  Ax^2 + By^2 + Cz^2 +  Dxy +  Exz +  Fyz +  Gx +  Hy +  Iz = 1
    J = np.hstack((x*x, y*y, z*z, x*y, x*z, y*z, x, y, z))
    K = np.ones_like(x)  # column of ones

    # np.hstack performs a loop over all samples and creates
    # a row in J for each x,y,z sample:
    # J[ix,0] = x[ix]*x[ix]
    # J[ix,1] = y[ix]*y[ix]
    # etc.

    JT = J.transpose()
    JTJ = np.dot(JT, J)
    InvJTJ = np.linalg.inv(JTJ)
    ABC = np.dot(InvJTJ, np.dot(JT, K))

    # Rearrange, move the 1 to the other side
    #  Ax^2 + By^2 + Cz^2 +  Dxy +  Exz +  Fyz +  Gx +  Hy +  Iz - 1 = 0
    #    or
    #  Ax^2 + By^2 + Cz^2 +  Dxy +  Exz +  Fyz +  Gx +  Hy +  Iz + J = 0
    #  where J = -1
    eansa = np.append(ABC, -1)

    return (eansa)


def polyToParams3D(vec):
    # gets 3D parameters of an ellipsoid. Found at http://www.juddzone.com/ALGORITHMS/least_squares_3D_ellipsoid.html
    # convert the polynomial form of the 3D-ellipsoid to parameters
    # centre, axes, and transformation matrix
    # vec is the vector whose elements are the polynomial
    # coefficients A..J
    # returns (centre, axes, rotation matrix)

    # Algebraic form: X.T * Amat * X --> polynomial form

    Amat = np.array(
        [
            [vec[0],     vec[3]/2.0, vec[4]/2.0, vec[6]/2.0],
            [vec[3]/2.0, vec[1],     vec[5]/2.0, vec[7]/2.0],
            [vec[4]/2.0, vec[5]/2.0, vec[2],     vec[8]/2.0],
            [vec[6]/2.0, vec[7]/2.0, vec[8]/2.0, vec[9]]
        ])

    # See B.Bartoni, Preprint SMU-HEP-10-14 Multi-dimensional Ellipsoidal Fitting
    # equation 20 for the following method for finding the centre
    A3 = Amat[0:3, 0:3]
    A3inv = inv(A3)
    ofs = vec[6:9]/2.0
    centre = -np.dot(A3inv, ofs)

    # Center the ellipsoid at the origin
    Tofs = np.eye(4)
    Tofs[3, 0:3] = centre
    R = np.dot(Tofs, np.dot(Amat, Tofs.T))
    R3 = R[0:3, 0:3]
    s1 = -R[3, 3]
    R3S = R3/s1
    (el, ec) = eig(R3S)
    recip = 1.0/np.abs(el)
    axes = np.sqrt(recip)
    inve = inv(ec)  # inverse is actually the transpose here

    return (centre, axes, inve)


def fit_polygon_to_ellipsoid(hull, tV=1):
    """Given a hull calculate the ABC of ellipsoid which fits """
    pts = hull.points
    X = pts[:, 0]
    Y = pts[:, 1]
    Z = pts[:, 2]

    # get convex hull
    surface = np.stack((X, Y, Z), axis=-1)
    hullV = ConvexHull(surface)
    lH = len(hullV.vertices)
    hull = np.zeros((lH, 3))
    for i in range(len(hullV.vertices)):
        hull[i] = surface[hullV.vertices[i]]
    hull = np.transpose(hull)
    eansa = ls_ellipsoid(hull[0], hull[1], hull[2])
    centre, axes, inve = polyToParams3D(eansa)

    axes = np.array(axes).astype('float64')
    volN = vol_ellipsoid(*axes)
    cbrt_diff = np.cbrt(tV/volN)
    a, b, c = np.array(axes * cbrt_diff)
    return np.array([a, b, c])
