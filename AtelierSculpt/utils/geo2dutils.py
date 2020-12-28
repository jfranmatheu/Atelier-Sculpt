from mathutils import Vector
import math
from math import cos, sin, sqrt, pi, atan2, degrees


# 2D METHOD
def distance_between(_p1, _p2): # Punto - Punto
    return math.hypot(_p1[0] - _p2[0], _p1[1] - _p2[1]) # Método 1
    #return math.sqrt((_p1[1] - _p1[0])**2 + (_p2[1] - _p2[0])**2) # Método 2

def direction(origin, destination):
    return destination - origin

def direction_normalized(origin, destination):
    return direction(origin, destination).normalized()

def is_inside_2d_rect(_point, _x, _y, _width, _height):
    return ((_x + _width) > _point[0] > _x) and ((_y + _height) > _point[1] > _y)

def is_inside_2d_circle(_mousePos, _coords, _radius):
    return distance_between(_mousePos, _coords) < _radius

def get_nearest_2d_point(_base, _points, _minDist = 0): # POINTS SHOULD BE VECTORS (2D)
    n = 0
    index = 0
    nearestPoint = None
    minDist = _minDist
    for point in _points:
        dist = distance_between(_base, point)
        if  dist < minDist:
            minDist = dist
            nearestPoint = point
            index = n
        n+=1
    return nearestPoint, minDist, index # point.co & float


# Function to return the minimum distance
# between a line segment AB and a point E
def min_distance_line_point(A, B, E):

    # vector AB
    AB = [None, None]
    AB[0] = B[0] - A[0]
    AB[1] = B[1] - A[1]

    # vector BP
    BE = [None, None]
    BE[0] = E[0] - B[0]
    BE[1] = E[1] - B[1]

    # vector AP
    AE = [None, None]
    AE[0] = E[0] - A[0]
    AE[1] = E[1] - A[1]

    # Variables to store dot product

    # Calculating the dot product
    AB_BE = AB[0] * BE[0] + AB[1] * BE[1]
    AB_AE = AB[0] * AE[0] + AB[1] * AE[1]

    # Minimum distance from
    # point E to the line segment
    reqAns = 0

    # Case 1
    if (AB_BE > 0) :

        # Finding the magnitude
        y = E[1] - B[1]
        x = E[0] - B[0]
        reqAns = sqrt(x * x + y * y)

    # Case 2
    elif (AB_AE < 0) :
        y = E[1] - A[1]
        x = E[0] - A[0]
        reqAns = sqrt(x * x + y * y)

    # Case 3
    else:

        # Finding the perpendicular distance
        x1 = AB[0]
        y1 = AB[1]
        x2 = AE[0]
        y2 = AE[1]
        mod = sqrt(x1 * x1 + y1 * y1)
        reqAns = abs(x1 * y2 - y1 * x2) / mod

    return reqAns

def rotate_point_around_another(o, angle, p):
  s = sin(angle)
  c = cos(angle)

  # translate point back to origin:
  p.x -= o.x
  p.y -= o.y

  # rotate point
  xnew = p.x * c - p.y * s
  ynew = p.x * s + p.y * c

  # translate point back:
  p.x = xnew + o.x
  p.y = ynew + o.y
  return p

def angle_from_vector(vector):
    return atan2(vector[1], vector[0])*180/pi

def perpendicular_vector3(v):
    if v.x == 0 and v.y == 0:
        if v.z == 0:
            # v is Vector(0, 0, 0)
            raise ValueError('zero vector')

        # v is Vector(0, 0, v.z)
        return Vector(0, 1, 0)

    return Vector((-v.y, v.x, 0))

def perpendicular_vector2(v):
    if v.x == 0 and v.y == 0:
        return Vector(0, 1)

    return Vector((v.y, -v.x)) # -v.y, v.x

def centroid_of_triangle(p1, p2, p3):
    # Formula to calculate centroid
    x = round((p1.x + p2.x + p3.x) / 3, 2)
    y = round((p1.y + p2.y + p3.y) / 3, 2)
    return Vector((x, y))


import numpy as np

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between_vectors(v1, v2, as_degree=False):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)) if not as_degree else degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))

def mathutils_vector_to_numpy_array(vector):
    return np.array(list(vector))
