from bpy.types import Panel

class BAS_PT_experimental_panel(Panel):
    bl_label = "Experimental"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Sculpt"

    @classmethod
    def poll(cls, context):
        return context.object and context.mode == 'SCULPT'

    def draw(self, context):
        pass
