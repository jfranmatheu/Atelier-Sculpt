import bpy
from bpy.types import Operator


class BAS_OT_rewind_start(Operator):
    bl_idname = "bas.rewind_start"
    bl_label = "Start Rewind"
    bl_description = "Start Rewind"
    bl_options = {'REGISTER', 'UNDO'}#, 'BLOCKING'}

    def execute(self, context):
        self.area = context.area
        self.mouse_pos = Vector((0, 0))
        self.point_pos = Vector((0, 0))
        self.start = False
        self.stroke_finished = False
        self.active_point = None
        self.active_point_index = -1
        self.snap_point = None
        self.strokes = context.window_manager.bas_nondestructive.strokes
        self.strokes.clear()
        self.space_points = []
        self.screen_points = []

        self.using_tool = False
        self.liquifying = False
        self.snapping = False
        self.dragging = False
        self.dragging_multiple = False
        self.snapping = False
        self.can_snap = False
        self.dist_threshold = 10
        self.active_tool = StrokeTool.Draw
        self.points_in_area = []
        self.hover_tool = None

        context.window_manager.modal_handler_add(self)
        args = (self, context)
        self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_stroke_callback, args, 'WINDOW', 'POST_PIXEL')
        return {'RUNNING_MODAL'}

    def add_stroke(self, context, event):
        hit_point = self.get_hit_point(context)
        if not hit_point:
            return
        print("add stroke")
        stroke = self.strokes.add()
        stroke.is_start = False
        stroke.mouse = self.mouse_pos
        stroke.time = Time() - self.start_time

        stroke.size = self.brush.size
        stroke.pressure = event.pressure
        stroke.location = hit_point

        self.space_points.append(hit_point)
        self.screen_points.append(self.mouse_pos)

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
            #print(d)
            strokes.append(d)
        return strokes

    def do_stroke(self, context):
        print("end stroke")
        bpy.ops.ed.undo_push(message="Stroke")
        bpy.ops.sculpt.brush_stroke(stroke=self.get_dict(), mode='NORMAL', ignore_background_click=False)

    def redo_stroke(self, context):
        bpy.ops.ed.undo()
        # TODO: PROJECT SCREEN POINTS AND FORGET OTHER PROJECTIONS
        self.do_stroke(context)

    def modal(self, context, event):
        if event.type == 'ESC':
            if event.value == 'PRESS':
                self.finish()
                return {'FINISHED'}
        elif self.area != context.area:
            self.finish()
            return {'FINISHED'}

        if self.start:
            if event.type in {'PEN', 'LEFTMOUSE'} and event.value == 'RELEASE': # event.type not in {'PEN', 'RIGHTMOUSE', 'MOUSEMOVE'} or
                self.do_stroke(context)
                self.stroke_finished = True
                return {'PASS_THROUGH'}
            elif distance_between(self.mouse_pos, self.point_pos) > 20:
                self.point_pos = self.mouse_pos
                self.add_stroke(context, event)
                return {'PASS_THROUGH'}

        elif event.type in {'PEN', 'LEFTMOUSE'} and event.value == 'PRESS': # and event.alt:
            hit_point = self.get_hit_point(context)
            if not hit_point:
                return
            print("start stroke")
            self.start = True
            self.start_time = Time()
            self.point_pos = self.mouse_pos
            stroke = self.strokes.add()
            stroke.is_start = True
            stroke.mouse = self.mouse_pos
            stroke.time = 0

            stroke.size = self.brush.size
            stroke.pressure = event.pressure
            stroke.location = hit_point

            self.space_points.append(hit_point)
            self.screen_points.append(self.mouse_pos)
            return {'RUNNING_MODAL'}

        return {'PASS_THROUGH'}