from bpy.types import Panel


class BAS_PT_Close_Gaps_Options(Panel):
    bl_label = "Close gaps options"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "NONE"
    bl_category = 'Sculpt'
    bl_description = "Close gaps options"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        props = context.window_manager.bas_closegaps
        layout = self.layout
        row = layout.row()
        row.prop(props, 'use', expand=True, text="Tris")
        row = layout.row()
        row.prop(props, 'smooth_passes')
        row = layout.row()
        row.prop(props, 'keep_dyntopo')
