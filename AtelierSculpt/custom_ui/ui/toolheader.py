from bl_ui.properties_paint_common import UnifiedPaintPanel
#from .icons import preview_collections
from bl_ui.space_view3d import VIEW3D_HT_tool_header as ToolHeader
from ..blocks.block_data import blocks
from ... import __package__ as main_package

widths = []


class BAS_HT_toolHeader(ToolHeader):  # , UnifiedPaintPanel):
    bl_idname = "BAS_HT_ToolHeader"
    bl_label = "Toolheader"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOL_HEADER"
    #bl_context = ".paint_common"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        if (context.mode != "SCULPT"):
            super().draw(context)
            return
        # Not a brush but a tool.
        elif not UnifiedPaintPanel.paint_settings(context):
            super().draw(context)
            return

        # self.layout.template_header() # to change region

        # VARIABLES
        self.act_obj = context.active_object
        toolsettings = context.tool_settings
        self.sculpt = toolsettings.sculpt
        self.brush = brush = self.sculpt.brush

        wm = context.window_manager
        scn = context.scene

        # Not a brush but a tool.
        if brush is None:
            return

        self.capabilities = self.brush.sculpt_capabilities
        self.ups = toolsettings.unified_paint_settings
        self.context = context

        self.prefs = context.preferences.addons[main_package].preferences
        self.sep = 5 * context.preferences.view.ui_scale

        self.props = scn.bas_custom_ui

        layout = self.layout

        for block in blocks:
            block(self)

        # layout.separator_spacer()

        #layout.popover('BAS_PT_custom_ui_uilist', text="Slots")

        #layout.menu("BAS_MT_custom_ui_items", text="", icon='ADD')
        #layout.operator('bas.edit_custom_ui', text="", icon='GREASEPENCIL')
