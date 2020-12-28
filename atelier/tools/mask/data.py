from bpy.types import PropertyGroup
from bpy.props import EnumProperty, BoolProperty, FloatProperty, IntProperty, StringProperty


class MaskPG(PropertyGroup):
    ''' MASK CAVITY. '''
    cavity_angle : IntProperty(name = "Cavity Angle", default = 85, min = 30, max = 90, step=1)
    cavity_strength : FloatProperty(name = "Mask Strength", default = 1.0, min = 0.1, max = 1.0, step=0.1)
