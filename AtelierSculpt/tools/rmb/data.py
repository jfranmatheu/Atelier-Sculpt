from bpy.types import PropertyGroup
from bpy.props import (
    EnumProperty, BoolProperty, IntProperty, FloatProperty
)


class RMBPG(PropertyGroup):
    deadzone_prop : IntProperty(
        name        = "Pixel Deadzone",
        description = "Screen distance after which movement has effect",
        default     = 4,
        min         = 0,
        max         = 16,
        subtype     = 'PIXEL',
        step        = 1,
        )

    sens_prop : FloatProperty(
        name        = "Sensitivity",
        description = "Multiplier to affect brush settings by",
        default     = 1.0,
        min         = 0.2,
        max         = 2.0,
        step        = 0.1,
        precision   = 1,
        subtype     = 'FACTOR',
        unit        = 'NONE',
        )

    textDisplaySize : EnumProperty(
        name        = "Text: Display Size",
        description = "Change Text Display Size",
        items       = (
            ('NONE', 'None', ''),
            ('LARGE', 'Large', ''),
            ('MEDIUM', 'Medium', ''),
            ('SMALL', 'Small', '')
        ),
        default     = 'LARGE'
    )

    invertAxis : BoolProperty(
        name        = "Invert Axis",
        description = "Invert Shortcut Directions",
        default     = False
    )
