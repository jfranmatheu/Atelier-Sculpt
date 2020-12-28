from mathutils import Color
import bpy
from . draw import draw_callback_px, draw_callback_px_2


def applyChanges(self):
    unify_settings = bpy.context.tool_settings.unified_paint_settings

    if self.doingstr:
        if self.uni_str:
            if self.increments:
                modrate = 0.0001
                newval = unify_settings.strength + modrate
            else:
                modrate = self.strmod * 0.0025
                newval  = unify_settings.strength + modrate
            if 10.0 > newval > -0.1:
                unify_settings.strength = newval
                self.strmod_total += modrate


        else:
            if self.increments:
                modrate = self.strmod * 0.0001
                newval = self.brush.strength + modrate
            else:
                modrate = self.strmod * 0.0025
                newval  = self.brush.strength + modrate
            if 10.0 > newval > -0.1:
                self.brush.strength = newval
                self.strmod_total += modrate


    if self.doingrad:
        if self.uni_size:
            newval = unify_settings.size + self.radmod
            if 2000 > newval > 0:
                unify_settings.size = newval
                self.radmod_total += self.radmod
        else:
            newval = self.brush.size + self.radmod
            if 2000 > newval > 0:
                self.brush.size = newval
                self.radmod_total += self.radmod



def revertChanges(self):
    unify_settings = bpy.context.tool_settings.unified_paint_settings

    if self.doingstr:
        if self.uni_str:
            unify_settings.strength -= self.strmod_total
        else:
            self.brush.strength -= self.strmod_total

    if self.doingrad:
        if self.uni_size:
            unify_settings.size -= self.radmod_total
        else:
            self.brush.size -= self.radmod_total

class SCULPT_OT_brush_rmb(bpy.types.Operator):
    bl_idname = "sculpt.brush_rmb"
    bl_label = "Brush RMB Quick Tweak"

    axisaffect : bpy.props.EnumProperty(
        name        = "Axis Order",
        description = "Which axis affects which brush property",
        items       = [('YSTR', 'X: Radius, Y: Strength', ''),
                       ('YRAD', 'Y: Radius, X: Strength', '')],
        default     = 'YRAD')

    textSize : bpy.props.EnumProperty(
        name        = "Size Value",
        description = "Text display; only shows when strength adjusted",
        items       = [('NONE', 'None', ''),
                       ('LARGE', 'Large', ''),
                       ('MEDIUM', 'Medium', ''),
                       ('SMALL', 'Small', '')],
        default     = 'MEDIUM')

    keyaction : bpy.props.EnumProperty(
        name        = "Key Action",
        description = "Hotkey second press or initial release behaviour",
        items       = [('IGNORE', 'Key Ignored', ''),
                       ('CANCEL', 'Key Cancels', ''),
                       ('FINISH', 'Key Applies', '')],
        default     = 'FINISH')

    text : bpy.props.EnumProperty(
        name        = "Numeric",
        description = "Text display; only shows when strength adjusted",
        items       = [('NONE', 'None', ''),
                       ('LARGE', 'Large', ''),
                       ('MEDIUM', 'Medium', ''),
                       ('SMALL', 'Small', '')],
        default     = 'LARGE')

    slider : bpy.props.EnumProperty(
        name        = "Slider",
        description = "Slider display for strength visualization",
        items       = [('NONE', 'None', ''),
                       ('LARGE', 'Large', ''),
                       ('MEDIUM', 'Medium', ''),
                       ('SMALL', 'Small', '')],
        default     = 'NONE')

    deadzone : bpy.props.IntProperty(
        name        = "Deadzone",
        description = "Screen distance after which movement has effect",
        default     = 4,
        min         = 0)

    sens : bpy.props.FloatProperty(
        name        = "Sens",
        description = "Multiplier to affect brush settings by",
        default     = 1.0,
        min         = 0.1,
        max         = 2.0)

    graphic : bpy.props.BoolProperty(
        name        = "Graphic",
        description = "Transparent circle to visually represent strength",
        default     = True)

    lock : bpy.props.BoolProperty(
        name        = "Lock Axis",
        description = "When adjusting one value, lock the other",
        default     = True)


    @classmethod
    def poll(cls, context):
        return (context.area.type == 'VIEW_3D'
                and context.mode in {'SCULPT', 'PAINT_WEIGHT', 'PAINT_VERTEX', 'PAINT_TEXTURE'})

    def changeValues(self, context):
        rmb = context.scene.bas_rmb
        self.deadzone = rmb.deadzone_prop
        self.sens = rmb.sens_prop
        #self.slider = scn.textDisplaySize
        self.text = rmb.textDisplaySize
        self.textSize = rmb.textDisplaySize
        if rmb.invertAxis:
            self.axisaffect = 'YSTR'
        else:
            self.axisaffect = 'YRAD'

    def modal(self, context, event):
        self.changeValues(context)

        self.cur = (event.mouse_region_x, event.mouse_region_y)
        diff = (self.cur[0] - self.prev[0], self.cur[1] - self.prev[1])
        #sens = (10) if event.ctrl else (self.sens)
        deadzone = self.deadzone
        sens = (self.sens * 0.5) if event.shift else (self.sens)
        if event.ctrl:
            self.increments = True
        else:
            self.increments = False

        if self.axisaffect == 'YRAD':
            # Y corresponds to radius
            s = (-1) if (self.cur[1] < self.prev[1]) else (0) if (self.cur[1] == self.prev[1]) else (1)
            if not self.doingrad:
                if self.lock:
                    if not self.doingstr and abs(self.cur[1] - self.start[1]) > deadzone:
                        self.doingrad = True
                        self.radmod = (self.strmod+10*s) if self.increments else (diff[1] * sens)
                elif abs(self.cur[1] - self.start[1]) > deadzone:
                    self.doingrad = True
                    self.radmod = (self.strmod+10*s) if self.increments else (diff[1] * sens)
            else:
                self.radmod = (self.strmod+10*s) if self.increments else (diff[1] * sens)
            #x = (-1) if (self.cur[0] < self.prev[0]) else (0) if (self.cur[0] == self.prev[0]) else (1)
            if not self.doingstr:
                if self.lock:
                    if not self.doingrad and abs(self.cur[0] - self.start[0]) > deadzone:
                        self.doingstr = True
                        self.strmod = diff[0] * sens#(self.strmod+.1*x) if self.increments else (diff[0] * sens)
                elif abs(self.cur[0] - self.start[0]) > deadzone:
                    self.doingstr = True
                    self.strmod = diff[0] * sens#(self.strmod+.1*x) if self.increments else (diff[0] * sens)
            else:
                self.strmod = diff[0] * sens#(self.strmod+.1*x) if self.increments else (diff[0] * sens)
        else:
            # Y corresponds to strength
            s = (-1) if (self.cur[0] < self.prev[0]) else (0) if (self.cur[0] == self.prev[0]) else (1)
            if not self.doingrad:
                if self.lock:
                    if not self.doingstr and abs(self.cur[0] - self.start[0]) > deadzone:
                        self.doingrad = True
                        self.radmod = (self.strmod+10*s) if self.increments else (diff[1] * sens)
                elif abs(self.cur[0] - self.start[0]) > deadzone:
                    self.doingrad = True
                    self.radmod = (self.strmod+10*s) if self.increments else (diff[1] * sens)
            else:
                self.radmod = (self.strmod+10*s) if self.increments else (diff[1] * sens)
            #x = (-1) if (self.cur[1] < self.prev[1]) else (0) if (self.cur[1] == self.prev[1]) else (1)
            if not self.doingstr:
                if self.lock:
                    if not self.doingrad and abs(self.cur[1] - self.start[1]) > deadzone:
                        self.doingstr = True
                        self.strmod = diff[0] * sens#(self.strmod+.1*x) if self.increments else (diff[0] * sens)
                elif abs(self.cur[1] - self.start[1]) > deadzone:
                    self.doingstr = True
                    self.strmod = diff[0] * sens#(self.strmod+.1*x) if self.increments else (diff[0] * sens)
            else:
                self.strmod = diff[0] * sens#(self.strmod+.1*x) if self.increments else (diff[0] * sens)

        context.area.tag_redraw()
        if event.type in {'LEFTMOUSE'} or self.action == 1:
            # apply changes, finished
            if hasattr(self, '_handle'):
                context.space_data.draw_handler_remove(self._handle, 'WINDOW')
                del self._handle
            applyChanges(self)
            return {'FINISHED'}
        elif event.type in {'ESC'} or self.action == -1:
            # do nothing, return to previous settings
            if hasattr(self, '_handle'):
                context.space_data.draw_handler_remove(self._handle, 'WINDOW')
                del self._handle
            revertChanges(self)
            return {'CANCELLED'}
        elif self.keyaction != 'IGNORE' and event.type in {self.hotkey} and event.value == 'RELEASE':
            # if key action enabled, prepare to exit
            if self.keyaction == 'FINISH':
                if hasattr(self, '_handle'):
                    context.space_data.draw_handler_remove(self._handle, 'WINDOW')
                    del self._handle
                self.action = 1
            elif self.keyaction == 'CANCEL':
                if hasattr(self, '_handle'):
                    context.space_data.draw_handler_remove(self._handle, 'WINDOW')
                    del self._handle
                self.action = -1
            return {'RUNNING_MODAL'}
        else:
            # continuation
            applyChanges(self)
            self.prev = self.cur
            return {'RUNNING_MODAL'}
        return {'CANCELLED'}


    def invoke(self, context, event):
        if bpy.context.mode == 'SCULPT':
            self.brush = context.tool_settings.sculpt.brush
        elif bpy.context.mode == 'PAINT_TEXTURE':
            self.brush = context.tool_settings.image_paint.brush
        elif bpy.context.mode == 'PAINT_VERTEX':
            self.brush = context.tool_settings.vertex_paint.brush
        elif bpy.context.mode == 'PAINT_WEIGHT':
            self.brush = context.tool_settings.weight_paint.brush
        else:
            self.report({'WARNING'}, "Mode invalid - only paint or sculpt")
            return {'CANCELLED'}

        self.hotkey = event.type
        if self.hotkey == 'NONE':
            self.keyaction = 'IGNORE'
        self.action = 0
        unify_settings = context.tool_settings.unified_paint_settings
        self.uni_size = unify_settings.use_unified_size
        self.uni_str = unify_settings.use_unified_strength
        self.cd = 10
        self.timer = 0
        self.doingrad = False
        self.doingstr = False
        self.start = (event.mouse_region_x, event.mouse_region_y)
        self.prev = self.start
        self.radmod_total = 0.0
        self.strmod_total = 0.0
        self.radmod = 0.0
        self.strmod = 0.0
        self.increments = False

        # self._handle = context.space_data.draw_handler_add(draw_callback_px, (self, context), 'WINDOW', 'POST_PIXEL')

        if self.graphic:
            if not hasattr(self, '_handle'):
                self._handle = context.space_data.draw_handler_add(draw_callback_px, (self, context), 'WINDOW', 'POST_PIXEL')

            self.brushcolor = self.brush.cursor_color_add
            if self.brush.sculpt_capabilities.has_secondary_color and self.brush.direction in {'SUBTRACT','DEEPEN','MAGNIFY','PEAKS','CONTRAST','DEFLATE'}:
                self.brushcolor = self.brush.cursor_color_subtract

        if self.text != 'NONE':
            if not hasattr(self, '_handle'):
                self._handle = context.space_data.draw_handler_add(draw_callback_px, (self, context), 'WINDOW', 'POST_PIXEL')

            self.offset = (30, -37)

            self.backcolor = Color((1.0, 1.0, 1.0)) - context.preferences.themes['Default'].view_3d.space.text_hi

        if self.slider != 'NONE':
            if not hasattr(self, '_handle'):
                self._handle = context.space_data.draw_handler_add(draw_callback_px, (self, context), 'WINDOW', 'POST_PIXEL')

            if self.slider == 'LARGE':
                self.sliderheight = 16
                self.sliderwidth = 180
            elif self.slider == 'MEDIUM':
                self.sliderheight = 8
                self.sliderwidth = 80
            else:
                self.sliderheight = 3
                self.sliderwidth = 60

            if not hasattr(self, 'offset'):
                self.offset = (30, -37)

            if not hasattr(self, 'backcolor'):
                self.backcolor = Color((1.0, 1.0, 1.0)) - context.preferences.themes['Default'].view_3d.space.text_hi

            self.frontcolor = context.preferences.themes['Default'].view_3d.space.text_hi

        # enter modal operation
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


def applyChanges_2(self, context):
    brush = context.tool_settings.sculpt.brush

    if self.doingsmooth:
        if self.uni_smooth:
            modrate = self.smoothmod * 0.0025
            newval  = brush.auto_smooth_factor + modrate
            if 10.0 > newval > -0.1:
                brush.auto_smooth_factor = newval
                self.smoothmod_total += modrate
        else:
            modrate = self.smoothmod * 0.0025
            newval  = self.brush.auto_smooth_factor + modrate
            if 10.0 > newval > -0.1:
                self.brush.auto_smooth_factor = newval
                self.smoothmod_total += modrate

def revertChanges_2(self, context):
    brush = context.tool_settings.sculpt.brush
    if self.doingsmooth:
        if self.uni_smooth:
            brush.auto_smooth_factor -= self.smoothmod_total
        else:
            self.brush.auto_smooth_factor -= self.smoothmod_total

class SCULPT_OT_brush_rmb_alt(bpy.types.Operator):
    bl_idname = "sculpt.brush_rmb_alt"
    bl_label = "Brush RMB Quick Tweak"

    axisaffect : bpy.props.EnumProperty(
        name        = "Axis Order",
        description = "Which axis affects which brush property",
        items       = [('YSTR', 'X: Radius, Y: Strength', ''),
                       ('YRAD', 'Y: Radius, X: Strength', '')],
        default     = 'YRAD')

    textSmooth : bpy.props.EnumProperty(
        name        = "Smooth Value",
        description = "Text display; only shows when strength adjusted",
        items       = [('NONE', 'None', ''),
                       ('LARGE', 'Large', ''),
                       ('MEDIUM', 'Medium', ''),
                       ('SMALL', 'Small', '')],
        default     = 'LARGE')

    keyaction : bpy.props.EnumProperty(
        name        = "Key Action",
        description = "Hotkey second press or initial release behaviour",
        items       = [('IGNORE', 'Key Ignored', ''),
                       ('CANCEL', 'Key Cancels', ''),
                       ('FINISH', 'Key Applies', '')],
        default     = 'FINISH')

    slider : bpy.props.EnumProperty(
        name        = "Slider",
        description = "Slider display for strength visualization",
        items       = [('NONE', 'None', ''),
                       ('LARGE', 'Large', ''),
                       ('MEDIUM', 'Medium', ''),
                       ('SMALL', 'Small', '')],
        default     = 'LARGE')

    deadzone : bpy.props.IntProperty(
        name        = "Deadzone",
        description = "Screen distance after which movement has effect",
        default     = 4,
        min         = 0)

    sens : bpy.props.FloatProperty(
        name        = "Sens",
        description = "Multiplier to affect brush settings by",
        default     = 1.0,
        min         = 0.1,
        max         = 2.0)

    graphic : bpy.props.BoolProperty(
        name        = "Graphic",
        description = "Transparent circle to visually represent strength",
        default     = True)

    lock : bpy.props.BoolProperty(
        name        = "Lock Axis",
        description = "When adjusting one value, lock the other",
        default     = True)


    @classmethod
    def poll(cls, context):
        return (context.area.type == 'VIEW_3D'
                and context.mode in {'SCULPT', 'PAINT_WEIGHT', 'PAINT_VERTEX', 'PAINT_TEXTURE'})


    def changeValues(self, context):
        rmb = context.scene.bas_rmb
        self.deadzone = rmb.deadzone_prop
        self.sens = rmb.sens_prop
        self.textSmooth = rmb.textDisplaySize
        self.slider = rmb.textDisplaySize
        if rmb.invertAxis:
            self.axisaffect = 'YSTR'
        else:
            self.axisaffect = 'YRAD'

    def modal(self, context, event):
        self.changeValues(context)
        sens = (self.sens * 0.5) if event.shift else (self.sens)
        self.cur = (event.mouse_region_x, event.mouse_region_y)
        diff = (self.cur[0] - self.prev[0], self.cur[1] - self.prev[1])
        X = True
        if self.axisaffect == 'XRAD':
            # Y corresponds to Smooth
            if not self.doingspac:
                if self.lock:
                    if not self.doingsmooth and abs(self.cur[1] - self.start[1]) > self.deadzone:
                        self.doingspac = True
                        self.spacemod = diff[1] * sens
                elif abs(self.cur[1] - self.start[1]) > self.deadzone:
                    self.doingspac = True
                    self.spacemod = diff[1] * sens
            else:
                self.spacemod = diff[1] * sens
            if not self.doingsmooth:
                if self.lock:
                    if not self.doingspac and abs(self.cur[0] - self.start[0]) > self.deadzone:
                        self.doingsmooth = True
                        self.smoothmod = diff[0] * sens
                elif abs(self.cur[0] - self.start[0]) > self.deadzone:
                    self.doingsmooth = True
                    self.smoothmod = diff[0] * sens
            else:
                self.smoothmod = diff[0] * sens
        else:
            # Y corresponds to Spacing
            if not self.doingspac:
                if self.lock:
                    if not self.doingsmooth and abs(self.cur[0] - self.start[0]) > self.deadzone:
                        self.doingspac = True
                        self.spacemod = diff[0] * sens
                elif abs(self.cur[0] - self.start[0]) > self.deadzone:
                    self.doingspac = True
                    self.spacemod = diff[0] * sens
            else:
                self.spacemod = diff[0] * sens
            if not self.doingsmooth:
                if self.lock:
                    if not self.doingspac and abs(self.cur[1] - self.start[1]) > self.deadzone:
                        self.doingsmooth = True
                        self.smoothmod = diff[1] * sens
                elif abs(self.cur[1] - self.start[1]) > self.deadzone:
                    self.doingsmooth = True
                    self.smoothmod = diff[1] * sens
            else:
                self.smoothmod = diff[1] * sens

        context.area.tag_redraw()
        if event.type in {'LEFTMOUSE'} or self.action == 1:
            # apply changes, finished
            if hasattr(self, '_handle'):
                context.space_data.draw_handler_remove(self._handle, 'WINDOW')
                del self._handle
            applyChanges_2(self, context)
            return {'FINISHED'}
        elif event.type in {'ESC'} or self.action == -1:
            # do nothing, return to previous settings
            if hasattr(self, '_handle'):
                context.space_data.draw_handler_remove(self._handle, 'WINDOW')
                del self._handle
            revertChanges(self)
            return {'CANCELLED'}
        elif self.keyaction != 'IGNORE' and event.type in {self.hotkey} and event.value == 'RELEASE':
            # if key action enabled, prepare to exit
            if self.keyaction == 'FINISH':
                if hasattr(self, '_handle'):
                    context.space_data.draw_handler_remove(self._handle, 'WINDOW')
                    del self._handle
                self.action = 1
            elif self.keyaction == 'CANCEL':
                if hasattr(self, '_handle'):
                    context.space_data.draw_handler_remove(self._handle, 'WINDOW')
                    del self._handle
                self.action = -1
            return {'RUNNING_MODAL'}
        else:
            # continuation
            applyChanges_2(self, context)
            self.prev = self.cur
            return {'RUNNING_MODAL'}
        return {'CANCELLED'}


    def invoke(self, context, event):
        if bpy.context.mode == 'SCULPT':
            self.brush = context.tool_settings.sculpt.brush
        elif bpy.context.mode == 'PAINT_TEXTURE':
            self.brush = context.tool_settings.image_paint.brush
        elif bpy.context.mode == 'PAINT_VERTEX':
            self.brush = context.tool_settings.vertex_paint.brush
        elif bpy.context.mode == 'PAINT_WEIGHT':
            self.brush = context.tool_settings.weight_paint.brush
        else:
            self.report({'WARNING'}, "Mode invalid - only paint or sculpt")
            return {'CANCELLED'}

        self.hotkey = event.type
        if self.hotkey == 'NONE':
            self.keyaction = 'IGNORE'
        self.action = 0
        unify_settings = context.tool_settings.unified_paint_settings
        self.uni_size = unify_settings.use_unified_size
        self.uni_smooth = self.brush.auto_smooth_factor
        #self.uni_str = unify_settings.use_unified_strength
        self.smooth = self.brush.auto_smooth_factor

        self.doingsmooth = False
        self.doingspac = False
        self.start = (event.mouse_region_x, event.mouse_region_y)
        self.prev = self.start
        self.smoothmod_total = 0.0
        self.spacemod_total = 0.0
        #self.strmod_total = 0.0
        self.smoothmod = 0.0
        self.spacemod = 0.0
        #self.strmod = 0.0

        # self._handle = context.space_data.draw_handler_add(draw_callback_px, (self, context), 'WINDOW', 'POST_PIXEL')

        if self.graphic:
            if not hasattr(self, '_handle'):
                self._handle = context.space_data.draw_handler_add(draw_callback_px_2, (self, context), 'WINDOW', 'POST_PIXEL')

            self.brushcolor = self.brush.cursor_color_add
            if self.brush.sculpt_capabilities.has_secondary_color and self.brush.direction in {'SUBTRACT','DEEPEN','MAGNIFY','PEAKS','CONTRAST','DEFLATE'}:
                self.brushcolor = self.brush.cursor_color_subtract

        if self.textSmooth != 'NONE':
            if not hasattr(self, '_handle'):
                self._handle = context.space_data.draw_handler_add(draw_callback_px_2, (self, context), 'WINDOW', 'POST_PIXEL')

            self.offset = (30, -37)

            self.backcolor = Color((1.0, 1.0, 1.0)) - context.preferences.themes['Default'].view_3d.space.text_hi

        if self.slider != 'NONE':
            if not hasattr(self, '_handle'):
                self._handle = context.space_data.draw_handler_add(draw_callback_px_2, (self, context), 'WINDOW', 'POST_PIXEL')

            if self.slider == 'LARGE':
                self.sliderheight = 16
                self.sliderwidth = 180
            elif self.slider == 'MEDIUM':
                self.sliderheight = 8
                self.sliderwidth = 80
            else:
                self.sliderheight = 3
                self.sliderwidth = 60

            if not hasattr(self, 'offset'):
                self.offset = (30, -37)

            if not hasattr(self, 'backcolor'):
                self.backcolor = Color((1.0, 1.0, 1.0)) - context.preferences.themes['Default'].view_3d.space.text_hi

            self.frontcolor = context.preferences.themes['Default'].view_3d.space.text_hi

        # enter modal operation
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


classes = (
    SCULPT_OT_brush_rmb,
    SCULPT_OT_brush_rmb_alt
)
