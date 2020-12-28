from bpy.types import Operator
from .... import __package__ as main_package

# ----------------------------------------------------------------- #
#   ACTIVATORS !                                     #
# ----------------------------------------------------------------- #

class BAS_OT_toolHeader_activator(Operator):
    bl_idname = "bas.toolheader_activator"
    bl_label = ""
    bl_description = "De/activate Addon's Tool Header"
    def execute(self, context):
        from bpy.utils import register_class, unregister_class
        from ...ui.toolheader import ToolHeader, BAS_HT_toolHeader
        prefs = context.preferences.addons[main_package].preferences
        if prefs.is_custom_tool_header_active:
            unregister_class(BAS_HT_toolHeader)
            #unregister_class(NSMUI_PT_dyntopo_stages)
            #unregister_class(NSMUI_PT_brush_optionsMenu)
            #unregister_class(NSMUI_PT_Support_Dev)

            register_class(ToolHeader)
            prefs.is_custom_tool_header_active = False
        else:
            unregister_class(ToolHeader)

            register_class(BAS_HT_toolHeader)
            #register_class(NSMUI_PT_dyntopo_stages)
            #register_class(NSMUI_PT_brush_optionsMenu)
            #register_class(NSMUI_PT_Support_Dev)
            prefs.is_custom_tool_header_active = True
        return {'FINISHED'}

class BAS_OT_header_activator(Operator):
    bl_idname = "bas.header_activator"
    bl_label = ""
    bl_description = "De/activate Addon's Header"
    def execute(self, context):
        from bpy.utils import register_class, unregister_class
        from ...ui.header import Header, BAS_HT_header
        prefs = context.preferences.addons[main_package].preferences
        if prefs.is_custom_header_active:
            unregister_class(BAS_HT_header)
            #unregister_class(NSMUI_HT_header_sculpt)
            #unregister_class(NSMUI_PT_remeshOptions)
            #register_class(VIEW3D_HT_header)
            register_class(Header)
            prefs.is_custom_header_active = False
        else:
            unregister_class(Header)
            register_class(BAS_HT_header)
            #unregister_class(VIEW3D_HT_header)
            #register_class(NSMUI_HT_header_sculpt)
            #register_class(NSMUI_PT_remeshOptions)
            prefs.is_custom_header_active = True
        return {'FINISHED'}
    
classes = [
    BAS_OT_header_activator,
    BAS_OT_toolHeader_activator
]
