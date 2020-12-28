from bpy.types import Operator, SpaceView3D
import bpy
from mathutils import Vector
from ...utils.geo2dutils import is_inside_2d_rect as mouse_inside_item
from ..io import save_actual_ui_state
from ..blocks.block_data import blocks


class BAS_OT_edit_custom_ui(Operator):
    bl_idname = "bas.edit_custom_ui"
    bl_label = "Edit Tool Header"
    bl_description = "Interactive edition mode (press Escape key to exit this mode)"

    def execute(self, context):
        self.original_color = list(
            context.preferences.themes[0].view_3d.space.header)
        self.window = self.toolheader = self.region = context.region
        self.area = context.area
        self.workspace = context.workspace
        self.scene = context.scene
        #self.slots = context.scene.bas_custom_ui.blocks
        self.mouse_pos = Vector((0, 0))
        self.offset = Vector((0, 0))
        self.offset_x = 0
        self.active_slot_index = -1
        self.active_item = False
        self.moving = False
        self.moving_x = 0
        self.num_blocks = len(blocks)  # len(self.slots)
        self.spacing = 10
        #self.width = context.scene.bas_custom_ui.width
        #self.pos_x = context.scene.bas_custom_ui.pos_x
        self.new_color = (.6, .3, .15, 0)
        context.preferences.themes[0].view_3d.space.header = self.new_color

        for reg in context.area.regions:
            if reg.type == 'TOOL_HEADER':
                self.toolheader = reg
            elif reg.type == 'WINDOW':
                self.window = reg

        context.window_manager.modal_handler_add(self)
        args = (self, context)
        self._handle = context.space_data.draw_handler_add(
            edit_custom_ui_callback_px, args, 'TOOL_HEADER', 'POST_PIXEL')
        return {'RUNNING_MODAL'}

    def finish(self, context=None):
        if hasattr(self, '_handle'):
            if context is None:
                SpaceView3D.draw_handler_remove(self._handle, "TOOL_HEADER")
                bpy.context.preferences.themes[0].view_3d.space.header = self.original_color
                save_actual_ui_state(bpy.context)
            else:
                context.preferences.themes[0].view_3d.space.header = self.original_color
                context.space_data.draw_handler_remove(
                    self._handle, 'TOOL_HEADER')
                save_actual_ui_state(context)
                self.area.tag_redraw()
            del self._handle

    def slide_item(self, other_index, to_right):
        active_index = self.active_slot_index

        other_pos = blocks[other_index].x
        my_pos = blocks[active_index].x

        if to_right:
            my_new_pos = other_pos
            other_new_pos = other_pos + \
                blocks[active_index].width + self.spacing
        else:
            my_new_pos = other_pos
            other_new_pos = other_pos + \
                blocks[active_index].width + self.spacing

        blocks[active_index].x = my_new_pos
        blocks[other_index].x = other_new_pos

        blocks[active_index], blocks[other_index] = blocks[other_index], blocks[active_index]

        self.active_slot_index += 1 if to_right else -1

    def modal(self, context, event):
        if self.area != context.area:
            self.finish(context)
            return {'CANCELLED'}
        elif not context.region:
            self.finish(context)
            return {'CANCELLED'}
        elif self.workspace != context.workspace:
            self.finish(context)
            return {'CANCELLED'}
        elif self.scene != bpy.context.scene:
            return {'CANCELLED'}
        elif event.type == 'ESC' and event.value == 'PRESS':
            self.finish(context)
            return {'FINISHED'}

        self.mouse_pos = Vector((event.mouse_region_x, event.mouse_region_y))

        self.area.tag_redraw()

        win_x = self.window.x
        win_y = self.window.y
        win_h = self.window.height
        th_w = self.toolheader.width
        th_h = self.toolheader.height

        #print("Mouse:", self.mouse_pos, "   WinX:", win_x, "   WinY:", win_y, "   AreaWidth:", self.area.width, "   ToolHeader Height:", th_h)

        if self.moving:
            if event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
                self.moving = False
                self.active_slot_index = -1
                self.active_item = False
                return {'RUNNING_MODAL'}

            n = self.active_slot_index
            if n != 0:
                if self.mouse_pos[0] < blocks[n-1].x + blocks[n-1].width / 2 - self.spacing:
                    #print("SLIDE LEFT")
                    self.slide_item(n-1, False)
            if n != (self.num_blocks - 1):
                if self.mouse_pos[0] > blocks[n+1].x + blocks[n+1].width / 2 + self.spacing:
                    #print("SLIDE RIGHT")
                    self.slide_item(n+1, True)
            return {'PASS_THROUGH'}

        elif mouse_inside_item(self.mouse_pos, win_x, win_h, th_w, th_h):
            i = 0
            for n in range(0, self.num_blocks):
                if mouse_inside_item(self.mouse_pos, win_x + blocks[n].x, 2 + win_h, blocks[n].width, th_h - 6):
                    self.active_slot_index = i
                    self.active_item = True
                    #print("inside item:", n)
                    if event.type == 'LEFTMOUSE':
                        if event.value == 'PRESS':
                            self.moving = True
                        return {'RUNNING_MODAL'}
                    elif event.type == 'RIGHTMOUSE':
                        if event.value == 'RELEASE':
                            bpy.ops.bas.show_custom_ui_context_menu(index=i)
                        return {'RUNNING_MODAL'}
                    elif event.type in {'DEL', 'X'} and event.value == 'RELEASE':
                        blocks.pop(i)
                        self.num_blocks -= 1
                        self.active_slot_index = -1
                        self.active_item = False
                        return {'RUNNING_MODAL'}
                    return {'PASS_THROUGH'}
                i += 1
            self.active_slot_index = -1
            self.active_item = False
            if event.type == 'LEFTMOUSE':
                return {'RUNNING_MODAL'}
        else:
            self.active_slot_index = -1
            self.active_item = False
            if self.moving:
                self.moving = False

        return {'PASS_THROUGH'}