from bpy.types import PropertyGroup, Object
from bpy.props import EnumProperty, BoolProperty, FloatProperty, PointerProperty, IntProperty, StringProperty


class RemeshPG(PropertyGroup):
    remesher : EnumProperty (
        items = (
            ('VOXEL', "Voxel", "Voxel Remesher"),
            ('QUADRIFLOW', "Quadriflow", "Quad Remesher"),
            ('DYNTOPO', "Dyntopo", "Dyntopo Remesher (flood fill)"),
            ('DECIMATE', "Decimate", "Decimate Remesher (modifier)")
        )
    )

    ''' VOXEL REMESH PROPS '''
    voxel_join_object : PointerProperty(type=Object, name="Object to join with")
    voxel_edit_size_presets : BoolProperty(default=False, name="Edit Voxel Size Presets")
    voxel_reprojection : EnumProperty (
        items = (
            ('NONE', "None", "Not use reprojection (quickest)"),
            ('SIMPLE', "Simple", "One single reprojection"),
            ('DOUBLE', "Double", "Double reprojection (slowest)")
        ), default = 'NONE',
        name="Reprojection", description="Reprojection mode"
    )
    voxels_incremental_sign : BoolProperty(default=True, name="Increment Voxel Size Direction")

    ''' QUADRIFLOW REMESH PROPS '''


    ''' DYNTOPO REMESH PROPS '''
    dyntopo_resolution : FloatProperty (
        subtype='FACTOR', default=100, min=1, max=300, precision=2,
        name="Resolution", description="Mesh resolution. Higher value for a high mesh resolution"
    )
    dyntopo_symmetry : BoolProperty(name="Force Symmetry", description="", default=False)
    dyntopo_symmetry_axis : EnumProperty(
        items=(('POSITIVE_X', "X", ""), ('POSITIVE_Y', "Y", ""), ('POSITIVE_Z', "Z", "")),
        default='POSITIVE_X', name="Axis", description="Axis where apply symmetry"
    )
    dyntopo_only_masked : BoolProperty(name="Remesh masked", default=False)

    ''' DECIMATE REMESH PROPS '''
    decimate_type : EnumProperty (
        items=(('COLLAPSE', "Collapse", ""), ('UNSUBDIVIDE', "Un-Subdivide", ""), ('PLANAR', "Planar", "")),
        default='COLLAPSE', name="Type", description="Decimation Type to apply"
    )
    decimate_ratio : FloatProperty (
        subtype='PERCENTAGE', default=100, min=0.0001, max=100, precision=2,
        name="% of Tris", description="Percentage of triangles. Less value = less triangles"
    )
    decimate_triangulate : BoolProperty(name="Triangulate", description="Force mesh triangulation", default=False)
    decimate_symmetry : BoolProperty(name="Use Symmetry", description="Symmetrize mesh", default=False)
    decimate_symmetry_axis : EnumProperty (
        items=(('X', "X", ""), ('Y', "Y", ""), ('Z', "Z", "")),
        default='X', name="Axis", description="Axis where apply symmetry"
    )


    ''' MESH TOOLS '''
    #show_remesher : BoolProperty(name='', default=True)
    #show_mesh_tools : BoolProperty(name='', description="Show Mesh Tools", default=False)
