
from bpy.types import PropertyGroup
from bpy.props import EnumProperty, IntProperty, BoolProperty


class MeshCloseGapsPG(PropertyGroup):
    # CLOSE GAPS PROPS
    use : EnumProperty (
        items=(
            ('TRIS', "Tris", ""),
            ('QUADS', "Quads", "")
        ),
        default='TRIS', name="Use tris or quads", description="Close gap with tris or quads"
    )
    smooth_passes : IntProperty (default = 3, max = 10, min = 0, name = "Smooth Passes", 
        description = "Number of smooth passes that will be applied after closing the gap"
    )
    keep_dyntopo : BoolProperty ( default = True, name="Keep Dyntopo", description="Only works if you are using dyntopo")
