from bpy.types import Panel


class BAS_PT_Mask_By_Cavity(Panel):
    bl_label = "Options"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "NONE"
    bl_category = 'Sculpt'
    bl_description = "Mask By Cavity options"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        mask = context.window_manager.bas_mask
        layout = self.layout
        layout.label(text="May be slow", icon='INFO')
        row = layout.row()
        row.prop(mask, 'cavity_angle', slider=True)
        row = layout.row()
        row.prop(mask, 'cavity_strength', slider=True)
