from . ops import set_meshfilter_scale, set_meshfilter_smooth
from bpy.props import BoolVectorProperty, FloatProperty
from bpy.types import PropertyGroup

MIN_SLIDER = -2
MAX_SLIDER =  2
STEP_SLIDER = 1/100
ACC_SLIDER = 2

mesh_filter_sliders = (
    'smooth', 'scale'
)

class MeshFilter_Sliders(PropertyGroup):
    axis : BoolVectorProperty(size=3, default=[False, False, False], name="Deform Axis", description="Apply the deformation in the selected axis")

    smooth  : FloatProperty(soft_min =MIN_SLIDER, soft_max=MAX_SLIDER, default=0, precision=ACC_SLIDER,
        name="Smooth", description="Smooth mesh", set=set_meshfilter_smooth
    )
    scale   : FloatProperty(soft_min =MIN_SLIDER, soft_max=MAX_SLIDER, default=0, precision=ACC_SLIDER,
        name="Scale", description="Scale mesh", set=set_meshfilter_scale
    )
