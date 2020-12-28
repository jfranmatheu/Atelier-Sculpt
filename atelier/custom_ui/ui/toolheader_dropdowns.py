from bpy.types import Panel
from ..blocks.block_id_cats import *
from ...icons import Icon
from ... import __package__ as main_package
from ...tools.brush_thumbnailer.ui import BrushThumbnailerOptions


class BAS_PT_brush_options_dropdown(Panel):
    bl_label = "Brush Options"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "NONE"
    bl_category = 'Sculpt'
    bl_description = "Dropdown Panel for Brush Options! You can create/remove/reset/create custom icon (all based in active brush)"

    #   BRUSH OPTIONS
    def draw(self, context):
        scn = context.scene
        wm = context.window_manager
        brush = context.tool_settings.sculpt.brush
        prefs = context.preferences.addons[main_package].preferences

        icon_brushAdd = Icon.BRUSH_ADD()
        icon_brushReset = Icon.BRUSH_RESET()
        icon_brushRemove = Icon.BRUSH_REMOVE()

        # 1ST ROW
        col = self.layout.column()
        row = col.row(align=True)
        row.scale_y = 1.5
        # NEW BRUSH BUTTON (DUPLICATE)
        row.operator("brush.add", text="New / Duplicate", icon_value=icon_brushAdd)

        # 2ND ROW
        row = col.row(align=True)
        # RESET BRUSH BUTTON
        row.operator("brush.reset", text="Reset", icon_value=icon_brushReset) # RESET BRUSH
        # DELETE BRUSH BUTTON
        row.operator("bas.brush_remove", text="Remove", icon_value=icon_brushRemove)
        col.separator()

        # 3RD-4TH ROW
        BrushThumbnailerOptions.draw(self, context)

        # 5th Row
        self.layout.separator(factor=.3)
        col = self.layout.column()
        box = col.box()
        box.label(text="Brush Selector")
        box.row().prop(prefs, 'brush_selector_grid_size')


classes = [
    BAS_PT_brush_options_dropdown
]
