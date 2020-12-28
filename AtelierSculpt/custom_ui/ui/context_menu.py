from bpy.types import Menu, Panel
from ... import __package__ as main_package


class WM_MT_button_context(Menu):
    bl_label = "Unused"

    def draw(self, context):
        pass


class BAS_MT_toolheader_ctx_ui_presets(Menu):
    bl_idname = "BAS_MT_toolheader_ctx_ui_presets"
    bl_label = "Tool Header Preset Operators"

    def draw(self, context):
        layout = self.layout
        prefs = context.preferences.addons[main_package].preferences
        if prefs.custom_ui_presets != 'NONE':
            layout.prop(prefs, 'custom_ui_presets', text="")
            layout.separator()
        layout.operator('bas.create_custom_ui_preset',      text="Create New Preset")
        layout.operator('bas.duplicate_custom_ui_preset',   text="Duplicate Active Preset")
        layout.operator('bas.reset_custom_ui_preset',       text="Reset Active Preset")
        layout.operator('bas.clear_custom_ui_preset',       text="Clear Active Preset")
        layout.operator('bas.remove_custom_ui_preset',      text="Remove Active Preset")


def menu_ctx_tool_header(self, context):
    layout = self.layout
    layout.separator()
    layout.operator('bas.edit_custom_ui', text="Edit Tool Header")
    layout.menu('BAS_MT_toolheader_ctx_ui_presets', text="Tool Header Presets")
    #layout.separator()


class BAS_PT_toolheader_edit_uiblock_context_menu(Panel):
    bl_idname = "BAS_PT_toolheader_edit_uiblock_context_menu"
    bl_label = "UI Block Context Menu"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "NONE"
    bl_category = 'Sculpt'

    def draw(self, context):
        from .ui_block_data import UI_Block
        block = UI_Block.get_active_block()
        if not block:
            return
        block_props = block.ppts

        if not block_props or not isinstance(block_props, dict):
            return

        layout = self.layout
        prefs = context.preferences.addons[main_package].preferences
        props = context.scene.bas_custom_ui
        layout.label(text="'" + block.name + "' Properties:")

        for key, value in block_props.items():
            if key.startswith('_'):
                data = prefs
                key = key[1:]
            else:
                data = props
            draw_prop(layout, data, key, value)


def draw_prop(layout, data, prop, tipo):
    #if tipo is int:
    layout.prop(data, prop)

classes = [
    WM_MT_button_context,
    BAS_MT_toolheader_ctx_ui_presets,
    BAS_PT_toolheader_edit_uiblock_context_menu
]
