from bpy.types import OperatorStrokeElement, PropertyGroup
from bpy.props import CollectionProperty, BoolProperty, FloatProperty, PointerProperty, IntProperty, StringProperty
from enum import Enum


class StrokeMode(Enum):
    NORMAL = 'NORMAL'
    INVERT = 'INVERT'
    SMOOTH = 'SMOOTH'

    def __call__(self):
        return self.value

class Stroke(PropertyGroup):
    points : CollectionProperty(type=OperatorStrokeElement)
    mode : StringProperty(default=StrokeMode.NORMAL())

class SculptLayer(PropertyGroup):
    strokes : CollectionProperty(type=Stroke)

class NonDestructiveSculptingPG(PropertyGroup):
    # OLD SYSTEM
    strokes : CollectionProperty(type=OperatorStrokeElement)

    # USER PROPERTIES
    show_overlays : BoolProperty(default=True, name="Show Overlays")

    liquify_strength : FloatProperty(default=2.0, min=1.0, max=20.0, name="Liquify Strength")
    curve_mode_follow_cursor : BoolProperty(default=False, name="Follow Cursor")

    # NEW LAYER SYSTEM
    layers : CollectionProperty(type=SculptLayer)
    active_layer_index : IntProperty(default=-1)
