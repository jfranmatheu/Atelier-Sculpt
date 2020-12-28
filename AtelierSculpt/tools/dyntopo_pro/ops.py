from bpy.types import Operator
from bpy.props import IntProperty
from ... import __package__ as main_package


class BAS_OT_dyntopo_change_value(Operator):
    bl_idname = "bas.dyntopo_change_value"
    bl_label = ""
    bl_description = "Value for Dyntopo Detail Size"

    value: IntProperty(name="value", default=5)
    detail : IntProperty(default=1) # low, mid, high (as numbers 1-3)

    def execute(self, context):
        context.scene.bas_dyntopo.detail_level = self.detail

        if(self.value != 0):
            if context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT':
                context.scene.tool_settings.sculpt.constant_detail_resolution = self.value
            elif context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH':
                context.scene.tool_settings.sculpt.detail_percent = self.value
            else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
                context.scene.tool_settings.sculpt.detail_size = self.value
        return {'FINISHED'}


class BAS_OT_dyntopo_change_level(Operator):
    bl_idname = "bas.dyntopo_change_level"
    bl_label = ""
    bl_description = "The more level the more detail !"

    lvl : IntProperty(default=1) # low, mid, high (as numbers 1-3)

    def execute(self, context):
        context.scene.bas_dyntopo.levels_active = self.lvl
        prefs = context.preferences.addons[main_package].preferences
        lvl = self.lvl - 1
        if context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT':
            context.scene.tool_settings.sculpt.constant_detail_resolution = prefs.dyntopo_levels_constant[lvl]
        elif context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH':
            context.scene.tool_settings.sculpt.detail_percent = prefs.dyntopo_levels_brush[lvl]
        else: # 'MANUAL' // 'RELATIVE'
            context.scene.tool_settings.sculpt.detail_size = prefs.dyntopo_levels_relative[lvl]
        return {'FINISHED'}


classes = (
    BAS_OT_dyntopo_change_level,
    BAS_OT_dyntopo_change_value
)
