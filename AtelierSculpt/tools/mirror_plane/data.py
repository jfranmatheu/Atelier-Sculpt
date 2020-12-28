from bpy.types import PropertyGroup, Object
from bpy.props import BoolProperty, FloatVectorProperty, PointerProperty
from . prop_fun import *


class MirrorPlanePG(PropertyGroup):
    # MIRROR PLANE
    use_world_origin : BoolProperty(default = False, name="Use World Origin")
    show : BoolProperty(default=False, name="Show mirror plane", update = update_mirror)
    created : BoolProperty(default=False, name="Mirror Plane Created")
    offset : FloatVectorProperty(name="", description="", default=(1, 1), step=1, precision=2, options={'ANIMATABLE'}, subtype='XYZ', unit='LENGTH', size=2, update=None, get=None, set=None)
    mirror_object : PointerProperty(type=Object, name="Mirrow Plane Object")
    source_model : PointerProperty(type=Object, name="Source Object")
    color : FloatVectorProperty(name="Color for the mirror plane", subtype='COLOR', default=(0.2,0.3,1,0.1), size=4, min=0, max=1, description="Change Color of the mirror plane", update=update_mirror_plane_color)
