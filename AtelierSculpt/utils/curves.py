import bpy
from mathutils.geometry import interpolate_bezier
from math import *
from numpy import linspace


def convert_handles_type(_points, _handleType = 'AUTO'):
    for p in _points:
        p.handle_left_type = _handleType
        p.handle_right_type = _handleType

def close_spline(_spline):
    if _spline.use_cyclic_u:
        _spline.use_cyclic_u = False
        _spline.use_cyclic_v = False
    else:
        _spline.use_cyclic_u = True
        _spline.use_cyclic_v = True
    # bpy.ops.curve.cyclic_toggle()

def interpolate_bezier(curve):
    spline = curve.splines[0]

    if len(spline.bezier_points) >= 2:
        r = spline.resolution_u + 1
        segments = len(spline.bezier_points)
        if not spline.use_cyclic_u:
            segments -= 1

        points = []
        for i in range(segments):
            inext = (i + 1) % len(spline.bezier_points)

            knot1 = spline.bezier_points[i].co
            handle1 = spline.bezier_points[i].handle_right
            handle2 = spline.bezier_points[inext].handle_left
            knot2 = spline.bezier_points[inext].co

            _points = interpolate_bezier(knot1, handle1, handle2, knot2, r)
            points.extend(_points)
        return points
    return None


def interpolate_3d_cursor_in_curve(curve_object, t):
    def interpBez3(bp0, t, bp3):
        # bp1, HR, HL, bp2

        return interpBez3_(bp0.co, bp0.handle_right, bp3.handle_left, bp3.co, t)
    #    return interpBez3_(bp0.co, bp0.handle_left, bp3.handle_right, bp3.co, t)

    def interpBez3_(p0, p1, p2, p3, t):
        r = 1-t
        return (r*r*r*p0 +
                3*r*r*t*p1 +
                3*r*t*t*p2 +
                t*t*t*p3)

    def interpBlenderSpline(spline, i1, t2):

        bp1 = spline.bezier_points[i1]
        bp2 = spline.bezier_points[i1+1]
        return interpBez3(bp1, t2, bp2)

    def mission1(obj, t):
        """ mathematically correct spline interpolation """

        i1 = floor(t)

        curve = obj.data

        bpy.context.scene.cursor.location = obj.matrix_world @ interpBlenderSpline(curve.splines[0], i1, t-i1)


    def mission2(obj, t):
        """ spline interpolation that matches the resolution_u setting inside blender """
        i1 = floor(t)
        t2 = t - i1
        spline = obj.data.splines[0]

        res = obj.data.render_resolution_u or obj.data.resolution_u
        t3 = t2*res
        t3i = floor(t3) / res
        t3f = t3 - floor(t3)

        p8 = interpBlenderSpline(spline, i1, t3i)
        p9 = interpBlenderSpline(spline, i1, t3i + 1/res)

        p = (1-t3f)*p8 + t3f*p9

        bpy.context.scene.cursor_location = obj.matrix_world * p

    mission1(curve_object, t)


def interpolate_curve(curve_object, t):
    def interpBez3(bp0, t, bp3):
        # bp1, HR, HL, bp2

        return interpBez3_(bp0.co, bp0.handle_right, bp3.handle_left, bp3.co, t)
    #    return interpBez3_(bp0.co, bp0.handle_left, bp3.handle_right, bp3.co, t)

    def interpBez3_(p0, p1, p2, p3, t):
        r = 1-t
        return (r*r*r*p0 +
                3*r*r*t*p1 +
                3*r*t*t*p2 +
                t*t*t*p3)

    def interpBlenderSpline(spline, i1, t2):

        bp1 = spline.bezier_points[i1]
        bp2 = spline.bezier_points[i1+1]
        return interpBez3(bp1, t2, bp2)

    def mission1(obj, t):
        """ mathematically correct spline interpolation """

        i1 = floor(t)

        curve = obj.data

        return obj.matrix_world @ interpBlenderSpline(curve.splines[0], i1, t-i1)


    def mission2(obj, t):
        """ spline interpolation that matches the resolution_u setting inside blender """
        i1 = floor(t)
        t2 = t - i1
        spline = obj.data.splines[0]

        res = obj.data.render_resolution_u or obj.data.resolution_u
        t3 = t2*res
        t3i = floor(t3) / res
        t3f = t3 - floor(t3)

        p8 = interpBlenderSpline(spline, i1, t3i)
        p9 = interpBlenderSpline(spline, i1, t3i + 1/res)

        p = (1-t3f)*p8 + t3f*p9

        bpy.context.scene.cursor_location = obj.matrix_world * p

    return mission1(curve_object, t)


def get_bezier_curve_points(curve_object, ratio=0.01):
    num = len(curve_object.data.splines[0].bezier_points)
    pairs = int(num / 2.0)
    loops = int(1.0 / ratio)

    points = []
    for k in range(0, pairs):
        factors = linspace(k, k + 1, num=loops)
        for l in range(0, loops):
            t = float(factors[l])
            if k == (pairs - 1) and t >= k + 1:
                break
            points.append(interpolate_curve(curve_object, t))
    return points
