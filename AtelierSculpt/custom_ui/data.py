from bpy.types import PropertyGroup
from bpy.props import (
    BoolProperty, IntVectorProperty,
    FloatVectorProperty, CollectionProperty,
    IntProperty, StringProperty,
    PointerProperty, FloatProperty,
    BoolVectorProperty, EnumProperty
)

class BLOCK_ITEM(PropertyGroup):
    draw_function = [None]
    width : IntProperty(default=1)
    x : IntProperty(default=1)
    name : StringProperty(default="Name")
    id : StringProperty(default='')

    def draw(self, th):
        self.draw_function[0](th)


class BLOCK_LIST(PropertyGroup):
    block_slots : CollectionProperty(type=BLOCK_ITEM)
    active_block_index : IntProperty(default=0)


class ToolHeader_PG_custom_ui(PropertyGroup):
    #blocks = []
    #width = []
    #pos_x = []
    # NOTE: can't modify data to fill width from draw functions in panel so is useful shit...
    #ui_blocks : PointerProperty(type=BLOCK_LIST)
    #_______________#
    # BRUSH MANAGER #
    # BRUSH OPTIONS # (Linked with Brush manager as it's used when show_collapsed)
    #bman_selection_grid_size : IntVectorProperty (
    #    size=2, default=(8, 6), min=1, max=20, step=1,
    #    name="Grid Size", description="Brush selection horizontal and vertical slots"
    #)
    brush_options_show_add       : BoolProperty(default=True, name="Show Add Brush Button")
    brush_options_show_remove    : BoolProperty(default=True, name="Show Remove Brush Button")
    brush_options_show_reset     : BoolProperty(default=True, name="Show Reset Brush Button")
    brush_options_show_collapsed : BoolProperty(default=False, name="Show Collapsed (dropdown panel)")
    
    #_______________#
    # BRUSH MANAGER #
    show_mesh_tools : BoolProperty(default=True, name="Show Mesh Tools")
    
    #_______________#
    # TEXTURE MANAGER #
    texture_manager_collapse : BoolProperty(default=False, name="Collapse")

    #_________________#
    # TEXTURE OPTIONS #
    texture_options_show_new_texture : BoolProperty(default=False, name="Show new texture button")
    texture_options_show_open_image : BoolProperty(default=False, name="Show open image button")

    #_________________#
    # FALLOFF PRESETS #
    depress_smooth  : BoolProperty(default=True) # True is False! ;)
    depress_round   : BoolProperty(default=True)
    depress_root    : BoolProperty(default=True)
    depress_sharp   : BoolProperty(default=True)
    depress_line    : BoolProperty(default=True)
    depress_max     : BoolProperty(default=True)


classes = [
    BLOCK_ITEM, BLOCK_LIST,
    ToolHeader_PG_custom_ui,
]
