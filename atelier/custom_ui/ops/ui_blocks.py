import bpy
from bpy.types import Operator
from bpy.props import StringProperty, IntProperty
from ..blocks.block_data import UI_Block
from ..io import save_actual_ui_state
from ... import __package__ as main_package


class BAS_OT_add_item_to_custom_ui(Operator):
    bl_idname = "bas.add_item_to_custom_ui"
    bl_label = ""
    bl_description = "Add item to Custom UI"
    block : StringProperty(default='')
    def execute(self, context):
        if self.block != '':
            UI_Block(self.block)
            #ui = context.scene.bas_custom_ui
            #ui.blocks.append(eval('UI_BLOCK_DRAW.' + self.block))
            #ui.width.append(20)
            #ui.pos_x.append(10)
            #block = context.scene.bas_custom_ui.ui_blocks.block_slots.add()
            #block.draw_function[0] = eval('UI_BLOCK_DRAW.' + self.block)
            #block.name = self.block.capitalize()
            #block.id = self.block
            save_actual_ui_state(context)
        else:
            self.report({'ERROR'}, "Not valid block!")
            return {'CANCELLED'}
        return {'FINISHED'}


class BAS_OT_remove_item_from_custom_ui(Operator):
    bl_idname = "bas.remove_item_from_custom_ui"
    bl_label = ""
    bl_description = "Remove item from Custom UI"
    index : IntProperty(default=-1)
    def execute(self, context):
        if self.index != -1:
            #context.scene.bas_custom_ui.blocks.pop(self.index)
            UI_Block.pop(self.index)
        else:
            self.report({'ERROR'}, "Not valid item index!")
            return {'CANCELLED'}
        return {'FINISHED'}


class BAS_OT_show_custom_ui_context_menu(Operator):
    bl_idname = "bas.show_custom_ui_context_menu"
    bl_label = ""
    bl_description = "Show Custom UI Context Menu"

    index: IntProperty(default=-1)

    def execute(self, context):
        block = UI_Block.get_block(self.index)
        if not block:
            return {'FINISHED'}
        block_props = block.ppts
        if not block_props or not isinstance(block_props, dict):
            return {'FINISHED'} # TODO: report block has no properties.

        UI_Block.set_active_block(self.index)
        bpy.ops.wm.call_panel(name="BAS_PT_toolheader_edit_uiblock_context_menu", keep_open=True)
        return {'FINISHED'}


classes = [
    BAS_OT_add_item_to_custom_ui,
    BAS_OT_remove_item_from_custom_ui,
    BAS_OT_show_custom_ui_context_menu
]
