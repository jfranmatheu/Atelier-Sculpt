from bpy.types import Panel
from . data import mesh_filter_sliders
from .. panel import BAS_PT_experimental_panel

class BAS_PT_mesh_filter(Panel):
    bl_parent_id = 'BAS_PT_experimental_panel'
    bl_label = "Mesh Filter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Sculpt"
    #bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.object and context.mode == 'SCULPT'

    def draw(self, context):
        main = self.layout.column(align=True)
        main.scale_y = 1.1
        sliders = context.window_manager.bas_meshfilter_sliders

        for filter in mesh_filter_sliders:
            box = main.box()
            box.prop(sliders, filter, text=filter.capitalize(), slider=True)
