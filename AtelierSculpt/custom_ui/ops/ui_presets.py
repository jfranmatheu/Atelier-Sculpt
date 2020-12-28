import bpy
from bpy.types import Operator
from bpy.props import StringProperty, IntProperty
from ..blocks.block_data import UI_Block
from ..io import save_actual_ui_state
from ... import __package__ as main_package


class BAS_OT_clear_custom_ui(Operator):
    bl_idname = "bas.clear_custom_ui_preset"
    bl_label = ""
    bl_description = "Clear Custom UI"
    def execute(self, context):
        UI_Block.clear()
        self.report({'INFO'}, "Preset has been cleared")
        return {'FINISHED'}

class BAS_OT_remove_custom_ui(Operator):
    bl_idname = 'bas.remove_custom_ui_preset'
    bl_label = ""
    bl_description = "Remove Custom UI"
    def execute(self, context):
        from ..io import remove_custom_ui
        remove_custom_ui(context)
        self.report({'INFO'}, "Preset has been removed")
        return {'FINISHED'}

class BAS_OT_create_custom_ui_preset(Operator):
    bl_idname = "bas.create_custom_ui_preset"
    bl_label = ""
    bl_description = "Create Custom UI Preset"

    name : StringProperty(default="My preset", name="Preset Name")

    def execute(self, context):
        if self.name == '' or self.name == ' ':
            self.report({'ERROR'}, "Preset name is invalid")
            return {'CANCELLED'}
        from ..io import create_custom_ui_preset
        if not create_custom_ui_preset(context, self.name):
            self.report({'ERROR'}, "Couldn't create new preset!")
            return {'CANCELLED'}
        self.report({'INFO'}, "Preset %s has been created" % self.name)
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


class BAS_OT_duplicate_custom_ui_preset(Operator):
    bl_idname = "bas.duplicate_custom_ui_preset"
    bl_label = ""
    bl_description = "Duplicate Custom UI Preset"

    def execute(self, context):
        from ..io import duplicate_custom_ui_preset
        if not duplicate_custom_ui_preset(context):
            self.report({'ERROR'}, "Couldn't duplicate active preset!")
            return {'CANCELLED'}
        return {'FINISHED'}


class BAS_OT_reset_custom_ui_preset(Operator):
    bl_idname = "bas.reset_custom_ui_preset"
    bl_label = ""
    bl_description = "Reset Custom UI Preset"

    def execute(self, context):
        from ..io import reset_custom_ui_preset
        if not reset_custom_ui_preset(context):
            self.report({'ERROR'}, "Couldn't reset active preset!")
            return {'CANCELLED'}
        self.report({'INFO'}, "Preset has been reset")
        return {'FINISHED'}


classes = [
    BAS_OT_create_custom_ui_preset,
    BAS_OT_duplicate_custom_ui_preset,
    BAS_OT_reset_custom_ui_preset,
    BAS_OT_clear_custom_ui,
    BAS_OT_remove_custom_ui
]
