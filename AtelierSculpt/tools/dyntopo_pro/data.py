from bpy.types import PropertyGroup
from bpy.props import (
    EnumProperty, BoolProperty, IntProperty
)


class DyntopoProPG(PropertyGroup):
    #________________#
    # DYNTOPO        #
    def update_dyntopo_detailing(self, context):
        context.scene.tool_settings.sculpt.detail_type_method = self.detailing
    detailing : EnumProperty(
        items=(
            ('RELATIVE', "Relative", ""),
            ('CONSTANT', "Constant", ""),
            ('BRUSH', "Brush", "")
        ),
        default='RELATIVE',
        update=update_dyntopo_detailing,
        description="Switch between detailing method used for dynamic topology."
    )
    stage : EnumProperty(
        items=(
            ('1', "Sketch", "First Stage: first shapes and volumes"),
            ('2', "Details", "Second Stage: bringing details"),
            ('3', "Polish", "Third Stage: polish and closing up more detailed shapes")
        ), default='1',
        description="Switch between Stage. Stages improve and divide the workflow in 3 stages: Sketch, Details and Polish."
    )
    toggle_stages : BoolProperty(default=True, description="Switch between Stage Mode (per Stages) and Default Mode (per Levels [1-6]).")
    stages_edit_values : BoolProperty(default=False, name="Edit Custom Values", description="Show custom values to be able of editing them")
    levels_active : IntProperty(default=0, min=1, max=6)
    detail_level : IntProperty(default=1, min=1, max=3)
