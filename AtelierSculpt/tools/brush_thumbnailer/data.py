from bpy.types import PropertyGroup
from bpy.props import (
    BoolProperty, FloatVectorProperty, IntProperty,
    StringProperty,FloatProperty, EnumProperty
)


class BrushThumbnailerPG(PropertyGroup):
    #___________________#
    # RENDER ICON PROPS #
    bg_color : FloatVectorProperty (
        size=3, default=(0, 0, 0), min=0, max=1, subtype='COLOR',
        name="Background Color", description="New brush icon background color"
    )
    # shading.single_color
    tint : FloatVectorProperty (
        size=4, default=(.9, .6, .4, 1), min=0, max=1, subtype='COLOR',
        name="Color", description="New brush icon tint color for mesh"
    )
    focal_length : IntProperty(default=80, min=20, max=200, step=5, name="Lens", description="Snapshot lens angle")
    # film_transparent
    use_alpha   : BoolProperty(default=False, name="Use Alpha", description="Toggle alpha for rendering the custom brush icon. NOTE: Not working in 'Sculpting' Workspace!")
    # shading.color_type -> SINGLE
    use_tint    : BoolProperty(default=False, name="Use Tint")

    mode : EnumProperty (
        items = (
            ('MANUAL', "Manual", "Snapshot based on the actual viewport view"),
            ('AUTO', "Automatic", "Pre-made setup. Advanced settings")
        ), default='MANUAL',
        name="Mode", description="Snapshot mode"
    )
    inverted : BoolProperty(default=False, description="Invert brush effect")
    override_size : BoolProperty(default=False, description="Override Original Brush Size")
    override_strength : BoolProperty(default=False, description="Override Original Brush Strength")
    brush_size : IntProperty(default=32, min=1, max=500, name="Brush Size")
    brush_strength : FloatProperty(default=.5, min=0.1, max=2, name="Brush Strength")
    use_text : BoolProperty(default=False, name="Use Text")
    text : StringProperty(default="My Brush", name="Text")
    text_size : FloatProperty(default=.3, min=.1, max=1.5, name="Text Size")
    text_color : FloatVectorProperty (
        size=4, default=(.9, .5, .2, 1), min=0, max=1, subtype='COLOR',
        name="Text Color", description="New brush icon tint color for mesh"
    )
