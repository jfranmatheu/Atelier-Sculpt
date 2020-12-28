import bpy


def toggle_off_curves(ui):
    ui.depress_smooth = True
    ui.depress_round = True
    ui.depress_root = True
    ui.depress_sharp = True
    ui.depress_line = True
    ui.depress_max = True

# TODO: dynamic description
class BAS_OT_falloff_curve_presets(bpy.types.Operator):
    bl_idname = "bas.falloff_curve_presets"
    bl_label = ""
    bl_description = "Select Curve Preset"
    shape: bpy.props.StringProperty(name="shape", default='SMOOTH')
    def execute(self, context):
        ui = context.scene.bas_custom_ui
        toggle_off_curves(ui)
        if self.shape == 'SMOOTH':
            ui.depress_smooth = False
        elif self.shape == 'SPHERE':
            ui.depress_round = False
        elif self.shape == 'ROOT':
            ui.depress_root = False
        elif self.shape == 'SHARP':
            ui.depress_sharp = False
        elif self.shape == 'LIN':
            ui.depress_line = False
        elif self.shape == 'CONSTANT':
            ui.depress_max = False

        context.tool_settings.sculpt.brush.curve_preset = self.shape
        return {'FINISHED'}
