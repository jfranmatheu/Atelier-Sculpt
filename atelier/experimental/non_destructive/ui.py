from bpy.types import Panel
from ..panel import BAS_PT_experimental_panel

class BAS_PT_non_destructive_sculpting(Panel):
    bl_parent_id = "BAS_PT_experimental_panel"
    bl_label = "Non-Destructive Sculpting"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Sculpt"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.object and context.mode == 'SCULPT'

    def draw(self, context):
        main = self.layout
        main.scale_y = 1
        rewind = context.window_manager.bas_nondestructive

        main.operator('bas.rewind_start_rec', text="Start").op_mode = 'DEFAULT'
        main.operator('bas.rewind_start_rec', text="Start (Curve)").op_mode = 'CURVE'
        main.operator('bas.rewind_start_rec', text="Start (Bristle)").op_mode = 'BRISTLE'

        main.separator()

        props = main.box()
        props.prop(rewind, 'show_overlays')
        props.prop(rewind, 'liquify_strength')
        props.separator()
        props.prop(rewind, 'curve_mode_follow_cursor')
