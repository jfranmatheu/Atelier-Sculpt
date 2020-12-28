import bpy
from bpy.types import Operator
from mathutils import Vector
from mathutils.geometry import interpolate_bezier
from enum import Enum
from time import time as Time
from ...utils.geo2dutils import (
    distance_between, get_nearest_2d_point, is_inside_2d_circle,
    direction_normalized, centroid_of_triangle, min_distance_line_point,
    perpendicular_vector2, angle_from_vector, rotate_point_around_another,
    angle_between_vectors, mathutils_vector_to_numpy_array
)
from ...utils.space_conversion import raycast_2d_3d, convert_3d_spaceCoords_to_2d_screenCoords, convert_2d_screenCoords_to_3d_spaceCoords
from .draw import draw_stroke_callback
from ...utils.draw2d import Alignment, Color, Space, Region, Label#, Canvas, CanvasModal, CanvasOperator
from ...utils.others import ShowMessageBox, blender_version
from bpy.props import BoolProperty, StringProperty
from numpy import arange
from math import sqrt, log, radians
import random

extended = blender_version()[1] >= 2.90

def hello_world():
    print("Hello World")

class StrokeTool(Enum):
    Draw = 1
    Move = 2
    Liquify = 3
    Extrude = 4
    Erase = 5
    Curve = 6
    Rope = 7
    Magnet = 8
    ALL = Magnet
    NONE = 0

tool_text = (
    ("Draw", StrokeTool.Draw),
    ("Move", StrokeTool.Move),
    ("Liquify", StrokeTool.Liquify),
    ("Extrude", StrokeTool.Extrude),
    ("Erase", StrokeTool.Erase),
    ("Curve", StrokeTool.Curve),
    ("Rope", StrokeTool.Rope),
    ("Magnet", StrokeTool.Magnet)
)

class BAS_OT_rewind_start_rec(Operator):
    bl_idname = "bas.rewind_start_rec"
    bl_label = "Start Recording"
    bl_description = "Start Recording Sculpt Strokes"
    bl_options = {'REGISTER', 'UNDO'}#, 'BLOCKING'}

    draw_curve : BoolProperty(default=False)
    op_mode : StringProperty(default='DEFAULT')

    def change_tool(self, ascii):
        if ascii.isnumeric():
            num = int(ascii)
            if num < StrokeTool.ALL.value:
                self.active_tool = StrokeTool(num)
                return True
        return False

    def invoke(self, context, event):
        #toolbar = None
        #for reg in context.area.regions:
        #    if reg.type == 'TOOLS':
        #        toolbar = reg

        #if not toolbar:
        #    return {'FINISHED'}

        #bpy.utils.register_class(CanvasOperator)

        #self.canvas = CanvasModal(Space.VIEW_3D, Region.WINDOW)#, context.area.x, context.area.y)
        #self.canvas.lock_to_area(context.area)
        #button = self.canvas.new_button([toolbar.width*2 + 20, 60], [120]*2, Color.Aquamarine, Color.Gold, hello_world).set_alpha(.8)
        #button.add_label("Click Me", 16, Alignment.Center, Color.Black)

        #if not self.canvas.start():
        #    return {'FINISHED'}

        #Canvas().start().new_button([60]*2, [120]*2, Color.Aquamarine, Color.Gold, hello_world, Label("Click Me"))

        #CanvasOperator.canvas = self.canvas
        #bpy.ops.canvas.operator()
        #return {'FINISHED'}

        self.area = context.area
        self.mouse_pos = Vector((0, 0))
        self.point_pos = Vector((0, 0))
        self.prev_dir_mouse = Vector((0, 0))
        self.move_ui_offset = Vector((0, 0))
        self.curve_drag_point = Vector((0, 0))
        self.start = False
        self.stroke_finished = False
        self.active_point = None
        self.active_point_index = -1
        self.snap_point = None
        self.props = context.window_manager.bas_nondestructive
        self.strokes = context.window_manager.bas_nondestructive.strokes
        self.strokes.clear()
        self.space_points = []
        self.screen_points = []

        self.using_tool = False

        self.dragging_ui = False
        self.x = 90
        self.y = 45

        self.liquifying = False
        self.snapping = False
        self.can_snap = False
        self.dist_threshold = 10
        self.active_tool = StrokeTool.Draw
        self.points_in_area = []
        self.points_in_area_distances = []
        self.hover_tool = None
        self.inverted = False
        self.num_points = 0
        self.bezier_points = []
        self.bez_screen_point = []
        self.dragging_bezier = False
        self.dragging_bezier_paint = False
        self.bez_length = 1
        self.bez_point_count = 10
        self.bez_first_time_project = True
        self.curve_drag_point_active = False

        ''' Bristle Brush Properties '''
        self.cursor_origin = None
        self.cursor_points = []
        self.cursor_points_size = []
        self.cursor_drawing = False
        self.cursor_active = False

        bpy.ops.ed.undo_push(message="Dummy") # TODO. DELETE PLS u.u
        bpy.ops.ed.undo_push(message="Dummy")

        context.window_manager.modal_handler_add(self)
        args = (self, context)
        self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_stroke_callback, args, 'WINDOW', 'POST_PIXEL')
        return {'RUNNING_MODAL'}

    def get_dict(self):
        strokes = []
        # expected a each sequence member to be a dict for an RNA collection
        for i, stroke in enumerate(self.strokes):
            d = {
                'name' : "Stroke_" + str(i),
                'is_start' : stroke.is_start,
                'location' : stroke.location,
                'mouse' : stroke.mouse,
                'pen_flip' : stroke.pen_flip,
                'pressure' : stroke.pressure,
                'size' : stroke.size,
                'time' : stroke.time
            }
            if extended:
                d2 = {
                    'mouse_event' : stroke.mouse,
                    'x_tilt' : 0.0,
                    'y_tilt' : 0.0
                }
                d.update(d2)
            #print(d)
            strokes.append(d)
        return strokes

    def get_hit_point(self, context):
        hit, pos, normal, index, obj, matrix = raycast_2d_3d(context, self.mouse_pos)
        return pos if hit else None #convert_2d_screenCoords_to_3d_spaceCoords(context, self.mouse_pos)

    def recalculate_screen_points(self, context):
        for i, p in enumerate(self.screen_points):
            p = convert_3d_spaceCoords_to_2d_screenCoords(context, self.space_points[i])

    def start_trick(self, context):
        self.redo_stroke(context)
        self.redo_stroke(context)

    def add_stroke(self, context, event):
        hit_point = self.get_hit_point(context)
        if not hit_point:
            return
        #print("add stroke")
        stroke = self.strokes.add()
        stroke.is_start = False
        stroke.mouse = self.mouse_pos
        stroke.time = Time() - self.start_time

        stroke.size = self.ups.size if self.ups.use_unified_size else self.brush.size
        stroke.pressure = event.pressure
        stroke.location = hit_point

        self.space_points.append(hit_point)
        self.screen_points.append(self.mouse_pos)

    def do_stroke(self, context):
        #print("end stroke")
        bpy.ops.ed.undo_push(message="Stroke")
        bpy.ops.sculpt.brush_stroke(stroke=self.get_dict(), mode='NORMAL' if not self.inverted else 'INVERT', ignore_background_click=True)

    def do_Stroke_no_undo_push(self):
        bpy.ops.sculpt.brush_stroke(stroke=self.get_dict(), mode='NORMAL' if not self.inverted else 'INVERT', ignore_background_click=True)

    def redo_stroke(self, context):
        # bpy.ops.ed.undo_history(item=0) x number of strokes
        #context.window_manager.print_undo_steps()
        #try:
        #    bpy.ops.ed.undo_redo(context) # NOTE: Check if this is actually working.
        #except Exception as e:
        #    print(e)
        #try:
        #    bpy.ops.ed.undo()
        #    self.do_stroke(context)
        #except Exception as e:
        #    print(e)
        try:
            bpy.ops.ed.undo()
            # TODO: PROJECT SCREEN POINTS AND FORGET OTHER PROJECTIONS
        except RuntimeError:
            return None
        finally:
            self.do_stroke(context)

    def move(self, context):
        hit, pos, normal, index, obj, matrix = raycast_2d_3d(context, self.mouse_pos)
        if hit:
            self.strokes[self.active_point_index].location = self.space_points[self.active_point_index] = pos
            if distance_between(self.prev_drag_pos, self.mouse_pos) > 20:
                self.prev_drag_pos = self.mouse_pos
                self.redo_stroke(context)

    def liquify(self, context):
        # GET AFFECTED POINTS
        rad = self.ups.size if self.ups.use_unified_size else self.brush.size
        strength = context.window_manager.bas_nondestructive.liquify_strength
        #affected_points = []
        #for i, point in enumerate(self.screen_points):
        #    if is_inside_2d_circle(self.mouse_pos, point, rad):
        #        affected_points.append(i)

        if not self.points_in_area:
            return
        # CALCULATE DIRECTION
        dir = direction_normalized(self.prev_drag_pos, self.mouse_pos)

        # MOVE POINTS IN DESIGNED DIRECTION IWTHIN A FALLOFF
        for i in self.points_in_area:
            dist = distance_between(self.screen_points[i], self.prev_drag_pos)
            factor = abs(1 - dist / rad)
            self.screen_points[i] += dir * factor * 10 * strength

        # REFRESH STROKE
        if distance_between(self.prev_drag_pos, self.mouse_pos) > 24:
            self.prev_drag_pos = self.mouse_pos
            # self.redo_stroke(context)
            try:
                bpy.ops.ed.undo()
            except RuntimeError:
                return None

            # PROJECT POINTS TO NEW POINTS
            for i in self.points_in_area:
                hit, pos, normal, index, obj, matrix = raycast_2d_3d(context, self.screen_points[i])
                if hit:
                    self.strokes[i].location = self.space_points[i] = pos
                    self.strokes[i].mouse = self.screen_points[i]

            #affected_points.clear()
            self.do_stroke(context)

    def pull(self, context):
        diff_mouse = distance_between(self.prev_drag_pos, self.mouse_pos)
        self.mode = -1 if self.active_point_index == 0 else 1 if self.active_point_index == (self.num_points - 1) else 0


        if self.mode == 0:
            rango_L = range(self.active_point_index, 0)
            rango_R = range(self.active_point_index, self.num_points - 1)
            # Store distances.
            distances_L = distances_R = []
            #print("dL")
            for i in rango_L:
                #print(i)
                distances_L.append(distance_between(self.screen_points[i - 1], self.screen_points[i]))
            #print("dR")
            for i in rango_R:
                #print(i)
                distances_R.append(distance_between(self.screen_points[i + 1], self.screen_points[i]))
        else:
            rango = range(0, self.num_points - 1) if self.mode == -1 else reversed(range(0, self.num_points - 1))
            # Store distances.
            distances = []
            for i in rango:
                #print(i)
                distances.append(distance_between(self.screen_points[i + 1], self.screen_points[i]))

        # Move active point
        #hit, pos, normal, index, obj, matrix = raycast_2d_3d(context, self.mouse_pos)
        #if hit:
        #    self.strokes[self.active_point_index].location = self.space_points[self.active_point_index] = pos
        #    self.screen_points[self.active_point_index] = self.mouse_pos

        # CALCULATE DIRECTION
        if diff_mouse > 6:
            mouse_dir = direction_normalized(self.prev_drag_pos, self.mouse_pos)

            self.screen_points[self.active_point_index] = self.prev_drag_pos + mouse_dir * diff_mouse

            # CALCULATE DISPLACEMENT FOR EACH POINT BASED ON DISTANCE DIFFERENCE.
            if self.mode == 0:
                i = self.active_point_index
                #print("L")
                for prev_dist in distances_L:
                    #print(i)
                    dir = direction_normalized(self.screen_points[i], self.screen_points[i - 1])
                    self.screen_points[i - 1] = self.screen_points[i] + dir * prev_dist
                    i-=1
                i = self.active_point_index
                #print("R")
                for prev_dist in distances_R:
                    #print(i)
                    dir = direction_normalized(self.screen_points[i], self.screen_points[i + 1])
                    self.screen_points[i + 1] = self.screen_points[i] + dir * prev_dist
                    i+=1
            else:
                inc = self.mode * -1
                i = 0 if self.mode == -1 else self.num_points - 1
                for prev_dist in distances:
                    #print(i)
                    dir = direction_normalized(self.screen_points[i], self.screen_points[i + inc])
                    self.screen_points[i + inc] = self.screen_points[i] + dir * prev_dist
                    i+=inc

            # REFRESH STROKE
            if diff_mouse > 24:
                self.prev_drag_pos = self.mouse_pos
                # self.redo_stroke(context)
                try:
                    bpy.ops.ed.undo()
                except RuntimeError:
                    return None

                # PROJECT POINTS TO NEW POINTS
                for i in range(0, self.num_points):
                    hit, pos, normal, index, obj, matrix = raycast_2d_3d(context, self.screen_points[i])
                    if hit:
                        self.strokes[i].location = self.space_points[i] = pos
                        self.strokes[i].mouse = self.screen_points[i]

                self.do_stroke(context)

    def extrude(self, context, event):
        self.add_stroke(context, event)
        self.redo_stroke(context)

    def update_points_in_area(self, context):
        # GET AFFECTED POINTS
        rad = self.ups.size if self.ups.use_unified_size else self.brush.size
        self.points_in_area.clear()
        for i, point in enumerate(self.screen_points):
            if is_inside_2d_circle(self.mouse_pos, point, rad):
                self.points_in_area.append(i)

    def update_points_in_area_distances(self, context):
        self.points_in_area_distances.clear()
        for i in self.points_in_area:
            self.points_in_area_distances.append(distance_between(self.mouse_pos, self.screen_points[i]))

    def erase(self, context):
        if not self.points_in_area:
            return

        for i in self.points_in_area:
            self.screen_points.pop(i)
            self.space_points.pop(i)
            self.strokes.remove(i)

        self.points_in_area.clear()
        self.redo_stroke(context)

    def magnet(self, context, inverted):
        if not self.points_in_area:
            return
        if not self.points_in_area_distances:
            return
        if distance_between(self.prev_drag_pos, self.mouse_pos) > 10:
            sign = 1 if not inverted else -1
            mult = 10
            rad = self.ups.size if self.ups.use_unified_size else self.brush.size
            for idk, i in enumerate(self.points_in_area):
                dist = self.points_in_area_distances[idk]
                factor = dist / rad * sign
                dir = direction_normalized(self.screen_points[i], self.mouse_pos)
                self.screen_points[i] = self.screen_points[i] + dir * factor * mult

            self.prev_drag_pos = self.mouse_pos

            try:
                bpy.ops.ed.undo()
            except RuntimeError as e:
                return None

            # PROJECT POINTS TO NEW POINTS
            for i in self.points_in_area:
                hit, pos, normal, index, obj, matrix = raycast_2d_3d(context, self.screen_points[i])
                if hit:
                    self.strokes[i].location = self.space_points[i] = pos
                    self.strokes[i].mouse = self.screen_points[i]

            self.do_stroke(context)

    def from_blender_bezier_curve(self, bez_points, count=10):
        # Get a list of points distributed along the curve.
        points_on_curve = interpolate_bezier(
            bez_points[0].co,
            bez_points[0].handle_right,
            bez_points[1].handle_left,
            bez_points[1].co,
            count)
        return points_on_curve

    # bez_points should be list of Vector type.
    def from_quadratic_bezier_curve(self, bez_points, count=24):
        points_on_curve = []
        t_inc = 1 / count
        prev_point = None
        dist = 0
        for t in arange(t_inc, 1, t_inc): # 0, 1 + t_inc, t_inc
            p = pow(1 - t, 2)*bez_points[0] + 2*t*(1 - t)*bez_points[1] + pow(t, 2)*bez_points[2]
            points_on_curve.append(p)
            if prev_point is not None:
                dist += distance_between(p, prev_point)
            prev_point = p
        return points_on_curve, dist

    # bez_points should be list of Vector type.
    def from_cubic_bezier_curve(self, bez_points, count=10):
        points_on_curve = []
        t_inc = 1 / count
        for t in arange(0, 1 + t_inc, t_inc):
            A = pow(1 - t, 3)*bez_points[0]
            B = 3*t*pow(1 - t, 2)*bez_points[1]
            C = 3*pow(t, 2)*(1 - t)*bez_points[2]
            D = pow(t, 3)*bez_points[3]
            points_on_curve.append(A + B + C + D)
        return points_on_curve

    def quadratic_bezier_length(self, bez_points):
        a = Vector((bez_points[0][0], bez_points[0][1]))
        b = Vector((bez_points[1][0], bez_points[1][1]))
        c = Vector((bez_points[2][0], bez_points[2][1]))

        v = w = Vector((0, 0))
        v.x = 2*(b.x - a.x)
        v.y = 2*(b.y - a.y)
        w.x = c.x - 2*b.x + a.x
        w.y = c.y - 2*b.y + a.y

        uu = 4*(w.x*w.x + w.y*w.y)

        if(uu < 0.00001):
            return float(sqrt((c.x - a.x)*(c.x - a.x) + (c.y - a.y)*(c.y - a.y)))

        vv = 4*(v.x*w.x + v.y*w.y)
        ww = v.x*v.x + v.y*v.y

        t1 = float(2*sqrt(uu*(uu + vv + ww)))
        t2 = 2*uu+vv
        t3 = vv*vv - 4*uu*ww
        t4 = float((2*sqrt(uu*ww)))

        return float(((t1*t2 - t3*log(t2+t1) -(vv*t4 - t3*log(vv+t4))) / (8*pow(uu, 1.5))))

    def update_bezier_curve_points(self, context, event):
        self.bez_point_count = int((max(90, min(self.bez_length, 1000)) / 1000) * 100)
        self.bez_screen_point, self.bez_length = self.from_quadratic_bezier_curve(self.bezier_points, self.bez_point_count)

    def update_bezier_drag_point(self):
        if self.props.curve_mode_follow_cursor:
            v_AC = direction_normalized(self.bezier_points[0], self.bezier_points[2])
            normal = perpendicular_vector2(v_AC)
            d_AC = distance_between(self.bezier_points[0], self.bezier_points[2])
            mid_AC = self.bezier_points[0] + v_AC * (d_AC / 2.0)
            d_base_handler = min_distance_line_point(self.bezier_points[0], self.bezier_points[2], self.bezier_points[1])
            if d_base_handler < 15:
                self.curve_drag_point = mid_AC + normal * -30
            else:
                bez_t05 = pow(1 - .5, 2)*self.bezier_points[0] + 2*.5*(1 - .5)*self.bezier_points[1] + pow(.5, 2)*self.bezier_points[2]
                # 1st Method.
                #v_MH = direction_normalized(mid_AC, self.bezier_points[1])
                #self.curve_drag_point = bez_t05 - v_MH * 30
                # 2nd Method (centroid of triangle).
                self.curve_drag_point = centroid_of_triangle(self.bezier_points[0], bez_t05, self.bezier_points[2])


            #print("Drag Point:", self.curve_drag_point)

    def project_curve(self, context, event):
        self.strokes.clear()
        self.start_time = Time()
        size = self.ups.size if self.ups.use_unified_size else self.brush.size
        for p in self.bez_screen_point:
            hit, pos, normal, index, obj, matrix = raycast_2d_3d(context, p)
            if hit:
                stroke = self.strokes.add()
                stroke.is_start = False
                stroke.mouse = p
                stroke.time = Time() - self.start_time
                stroke.size = size
                stroke.pressure = event.pressure
                stroke.location = pos
        if self.bez_first_time_project:
            self.do_stroke(context)
        else:
            self.redo_stroke(context)

    def project_cursor(self, context, event):
        self.strokes.clear()
        #size = self.ups.size if self.ups.use_unified_size else self.brush.size
        #size = size / len(self.cursor_points)
        size = 5
        for i, p in enumerate(self.cursor_points):
            hit, pos, normal, index, obj, matrix = raycast_2d_3d(context, p)
            if hit:
                stroke = self.strokes.add()
                stroke.is_start = False
                stroke.mouse = p
                stroke.time = Time() - self.start_time
                stroke.size = self.cursor_points_size[i]
                stroke.pressure = event.pressure
                stroke.location = pos
        self.do_Stroke_no_undo_push()

    def isLeft(self, a, b, c):
        return ((b[0] - a[0])*(c[1] - a[1]) - (b[1] - a[1])*(c[0] - a[0])) > 0


    def finish(self):
        self.remove_graphics()
        self.area.tag_redraw()

    def apply_tool(self, context, event):
        if self.active_tool == StrokeTool.Liquify:
            self.liquify(context)
        elif self.active_tool == StrokeTool.Move:
            self.move(context)
        elif self.active_tool == StrokeTool.Rope:
            self.pull(context)
        elif self.active_tool == StrokeTool.Erase:
            self.erase(context)
        elif self.active_tool == StrokeTool.Magnet:
            self.magnet(context, event.alt)

    def move_ui(self):
        self.x = self.mouse_pos[0] - self.move_ui_offset[0]
        self.y = self.mouse_pos[1] - self.move_ui_offset[1]

    def modal(self, context, event):
        if event.type == 'ESC':
            if event.value == 'PRESS':
                self.finish()
                return {'FINISHED'}
        elif self.area != context.area:
            self.finish()
            return {'FINISHED'}

        if self.change_tool(event.ascii):
            return {'RUNNING_MODAL'}

        # TODO: Filter if it's not a brush
        self.brush = context.tool_settings.sculpt.brush
        self.ups = context.tool_settings.unified_paint_settings
        self.mouse_pos = Vector((event.mouse_region_x, event.mouse_region_y))

        self.area.tag_redraw()

        if self.stroke_finished:
            if self.op_mode == 'BRISTLE':
                # Está usando el cursor.
                if self.cursor_drawing or (event.shift and event.type in {'LEFTMOUSE', 'PEN'}):
                    if event.type in {'LEFTMOUSE', 'PEN'} and event.value == 'RELEASE':
                        self.cursor_drawing = False
                        return {'RUNNING_MODAL'}
                    # Moving cursor points. (using threshold)
                    d_diff_mouse = distance_between(self.prev_cursor_pos, self.mouse_pos)
                    if d_diff_mouse > 4:
                        dir_mouse = direction_normalized(self.cursor_origin, self.mouse_pos)
                        dir_angle = angle_from_vector(dir_mouse)
                        prev_dir_angle = angle_from_vector(self.prev_dir_mouse)
                        diff_angle = radians(dir_angle - prev_dir_angle)
                        # Transpose and rotate points.
                        offset = self.mouse_pos - self.prev_cursor_pos
                        d_drag_mouse = distance_between(self.cursor_origin, self.mouse_pos)
                        dir_drag_mouse = direction_normalized(self.cursor_origin, self.mouse_pos)
                        for i in range(0, len(self.cursor_points)):
                            self.cursor_points[i] = rotate_point_around_another(self.cursor_origin, diff_angle, self.cursor_points[i]) + offset
                        #self.update_bezier_drag_point()
                        self.cursor_origin = self.mouse_pos
                        # Project points.
                        self.prev_cursor_pos = self.mouse_pos
                        self.prev_dir_mouse = dir_mouse
                        self.project_cursor(context, event)
                # Se hace click.
                elif event.type in {'LEFTMOUSE', 'PEN'} and event.value == 'PRESS':
                    # Se hace sobre el origen del cursor ?
                    if distance_between(self.cursor_origin, self.mouse_pos) < 14:
                        self.cursor_drawing = True
                        self.start_time = Time()
                    else:
                        self.cursor_points.append(self.mouse_pos)
                        self.cursor_points_size.append(1 + random.randrange(0, 9))
                    return {'RUNNING_MODAL'}
                elif event.ctrl and event.value == 'PRESS':
                    self.cursor_origin = self.mouse_pos
                else:
                    self.cursor_active = distance_between(self.cursor_origin, self.mouse_pos) < 14
                return {'PASS_THROUGH'}
            elif self.op_mode == 'CURVE':
                if self.dragging_bezier_paint:
                    if event.type in {'LEFTMOUSE', 'PEN'} and event.value == 'RELEASE':
                        self.dragging_bezier_paint = False
                        return {'RUNNING_MODAL'}
                    # MOVE CURVE BRUSH.
                    d_diff_mouse = distance_between(self.prev_drag_pos, self.mouse_pos)
                    if d_diff_mouse > 20:
                        dir_mouse = direction_normalized(self.curve_drag_point, self.mouse_pos)
                    # 1ST METHOD:
                        #v_AC = direction_normalized(self.bezier_points[0], self.bezier_points[2])
                        #normal = perpendicular_vector2(v_AC)
                        #v1 = mathutils_vector_to_numpy_array(normal)
                        #v2 = mathutils_vector_to_numpy_array(dir_mouse)
                        #diff_angle = angle_between_vectors(v1, v2)
                        #print("1:", diff_angle)
                    # 2ND METHOD:
                        dir_angle = angle_from_vector(dir_mouse)
                        prev_dir_angle = angle_from_vector(self.prev_dir_mouse)
                        diff_angle = radians(dir_angle - prev_dir_angle)
                        #print("2:", diff_angle)
                    # TRANSPOSE AND ROTATE POINTS.
                        offset = self.mouse_pos - self.prev_drag_pos
                        d_drag_mouse = distance_between(self.curve_drag_point, self.mouse_pos)
                        dir_drag_mouse = direction_normalized(self.curve_drag_point, self.mouse_pos)
                        for i in range(0, len(self.bezier_points)):
                            #dist = distance_between(p, self.mouse_pos)
                            #dir = direction_normalized(p, self.mouse_pos)
                            #p = rotate_point_around_another(self.curve_drag_point, angle, p) + dir * dist + dir_drag_mouse * d_drag_mouse
                            self.bezier_points[i] = rotate_point_around_another(self.curve_drag_point, diff_angle, self.bezier_points[i]) + offset #dir_drag_mouse * d_drag_mouse #+ dir_mouse * d_diff_mouse
                        self.update_bezier_drag_point()
                    # UPDATE and PROJECT.
                        self.update_bezier_curve_points(context, event)
                        self.prev_drag_pos = self.mouse_pos
                        self.prev_dir_mouse = dir_mouse
                        self.project_curve(context, event)
                elif self.dragging_bezier:
                    if event.type in {'LEFTMOUSE', 'PEN'} and event.value == 'RELEASE':
                        self.dragging_bezier = False
                        return {'RUNNING_MODAL'}
                    else:
                        self.bezier_points[self.active_point_index] = self.active_point = self.mouse_pos
                        self.update_bezier_curve_points(context, event)
                        self.update_bezier_drag_point()
                    #self.bez_length = self.quadratic_bezier_length(self.bezier_points)
                elif self.active_point or self.curve_drag_point_active:
                    if event.type in {'LEFTMOUSE', 'PEN'} and event.value == 'PRESS':
                        if self.curve_drag_point_active:
                            print("Active Drag Point")
                            self.dragging_bezier_paint = True
                        else:
                            self.dragging_bezier = True
                        self.prev_drag_pos = self.mouse_pos
                        return {'RUNNING_MODAL'}
                else:
                    self.update_bezier_drag_point()
            elif self.using_tool:
                if event.type in {'LEFTMOUSE', 'PEN'} and event.value == 'RELEASE':
                    self.using_tool = False
                    return {'RUNNING_MODAL'}
                self.apply_tool(context, event)
            elif self.dragging_ui:
                if event.type in {'LEFTMOUSE', 'PEN'} and event.value == 'RELEASE':
                    self.dragging_ui = False
                    return {'RUNNING_MODAL'}
                self.move_ui()
            elif event.type in {'LEFTMOUSE', 'PEN'} and event.value == 'PRESS':
                # Change tool by clicking.
                if isinstance(self.hover_tool, StrokeTool):
                    if self.hover_tool == StrokeTool.NONE:
                        #print("MOVE UI")
                        self.dragging_ui = True
                        self.move_ui_offset[0] = self.mouse_pos[0] - self.x
                        self.move_ui_offset[1] = self.mouse_pos[1] - self.y
                    else:
                        self.active_tool = self.hover_tool
                    return {'RUNNING_MODAL'}
                # Check if there's a valid active point. {MOVE, ROPE...} Modes that need a point.
                elif self.active_tool in {StrokeTool.Move, StrokeTool.Rope}:
                    if self.active_point_index == -1 or not self.active_point:
                        return {'PASS_THROUGH'}
                    if self.active_tool == StrokeTool.Rope:
                        self.num_points = len(self.screen_points)
                # Modes that are only one-click action. (no drag and so)
                elif self.active_tool == StrokeTool.Extrude:
                    self.extrude(context, event)
                    return {'RUNNING_MODAL'}
                self.prev_drag_pos = self.mouse_pos
                self.using_tool = True
                return {'RUNNING_MODAL'}
            elif event.type == 'I' and event.value == 'PRESS':
                self.inverted = not self.inverted
                self.redo_stroke(context)
                return {'RUNNING_MODAL'}
            return {'PASS_THROUGH'}

        # START RELEASE
        elif self.start:
            if event.type in {'PEN', 'LEFTMOUSE'} and event.value == 'RELEASE': # event.type not in {'PEN', 'RIGHTMOUSE', 'MOUSEMOVE'} or
                # RELEASE CURVE DRAW
                if self.op_mode == 'CURVE':
                    dist = distance_between(self.bezier_points[0], self.mouse_pos)
                    dir = direction_normalized(self.bezier_points[0], self.mouse_pos)
                    mid_point = self.bezier_points[0] + dir * (dist / 2.0)
                    self.bezier_points.append(mid_point)
                    self.bezier_points.append(self.mouse_pos)
                    self.update_bezier_curve_points(context, event)
                    #self.bez_length = self.quadratic_bezier_length(self.bezier_points)
                else:
                    self.do_stroke(context)
                    self.start_trick(context)
                self.stroke_finished = True
                return {'RUNNING_MODAL'}
            elif self.op_mode == 'DEFAULT' and distance_between(self.mouse_pos, self.point_pos) > 20:
                self.point_pos = self.mouse_pos
                self.add_stroke(context, event)
                return {'PASS_THROUGH'}
            elif self.op_mode == 'BRISTLE':
                self.cursor_origin = self.mouse_pos # update origin point
                return {'PASS_THROUGH'}

        # START PRESS
        elif event.type in {'PEN', 'LEFTMOUSE'} and event.value == 'PRESS': # and event.alt:
            hit_point = self.get_hit_point(context)
            if not hit_point:
                return {'PASS_THROUGH'}
            #print("start stroke")
            self.start = True
            self.start_time = Time()
            self.point_pos = self.mouse_pos
            if self.op_mode == 'DEFAULT':
                stroke = self.strokes.add()
                stroke.is_start = True
                stroke.mouse = self.mouse_pos
                stroke.time = 0

                stroke.size = self.brush.size
                stroke.pressure = event.pressure
                stroke.location = hit_point

                self.space_points.append(hit_point)
                self.screen_points.append(self.mouse_pos)
            elif self.op_mode == 'BRISTLE':
                self.cursor_origin = self.prev_cursor_pos = self.mouse_pos
            else:
                self.bezier_points.append(self.mouse_pos)
            return {'RUNNING_MODAL'}

        return {'PASS_THROUGH'}

    def remove_graphics(self):
        try:
            if hasattr(self, '_handle'):
                bpy.types.SpaceView3D.draw_handler_remove(self._handle, "WINDOW")
                del self._handle
            if hasattr(self, 'canvas'):
                self.canvas.stop()
                del self.canvas
        except Exception as e:
            print(e)


classes = (
    BAS_OT_rewind_start_rec,
)