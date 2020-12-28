from bpy.types import Menu
from ..blocks.block_id_cats import *


def draw_items(self, items):
    layout = self.layout
    for item in items:
        if item[0] == '':
            layout.separator()
        else:
            layout.operator("bas.add_item_to_custom_ui", text=item[1]).block = item[0]


class DefaultMenu(Menu):
    bl_idname = "BAS_MT_default"
    bl_label = "DefaultMenu"
    def draw(self, context):
        draw_items(self, default)

class BrushMenu(Menu):
    bl_idname = "BAS_MT_brush"
    bl_label = "BrushMenu"
    def draw(self, context):
        draw_items(self, brush)
class TextureMenu(Menu):
    bl_idname = "BAS_MT_texture"
    bl_label = "TextureMenu"
    def draw(self, context):
        draw_items(self, texture)
class SlidersMenu(Menu):
    bl_idname = "BAS_MT_sliders"
    bl_label = "SlidersMenu"
    def draw(self, context):
        draw_items(self, sliders)
class FalloffMenu(Menu):
    bl_idname = "BAS_MT_falloff"
    bl_label = "FalloffMenu"
    def draw(self, context):
        draw_items(self, falloff)
class MaskMenu(Menu):
    bl_idname = "BAS_MT_mask"
    bl_label = "MaskMenu"
    def draw(self, context):
        draw_items(self, mask)
class StrokeMenu(Menu):
    bl_idname = "BAS_MT_stroke"
    bl_label = "StrokeMenu"
    def draw(self, context):
        draw_items(self, stroke)
class OthersMenu(Menu):
    bl_idname = "BAS_MT_others"
    bl_label = "OthersMenu"
    def draw(self, context):
        draw_items(self, others)
class UtilsMenu(Menu):
    bl_idname = "BAS_MT_utils"
    bl_label = "UtilsMenu"
    def draw(self, context):
        draw_items(self, utils)
class SpacingMenu(Menu):
    bl_idname = "BAS_MT_spacing"
    bl_label = "SpacingMenu"
    def draw(self, context):
        draw_items(self, spacing)

submenus = [ DefaultMenu,
    BrushMenu, TextureMenu, SlidersMenu, FalloffMenu,
    MaskMenu, StrokeMenu, OthersMenu, UtilsMenu, SpacingMenu
]

class BAS_MT_custom_ui_items(Menu):
    bl_idname = "BAS_MT_custom_ui_items"
    bl_label = "Items"

    def draw(self, context):
        layout = self.layout

        for cat in categories: # UI_BLOCK_DRAW_STR.ALL.value (deprecated)
            if cat == 'NONE':
                layout.separator()
            else:
                layout.menu("BAS_MT_"+cat.lower(), text=cat)


classes = [
    BAS_MT_custom_ui_items
] + submenus
