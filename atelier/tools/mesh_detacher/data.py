from bpy.types import PropertyGroup, Object
from bpy.props import EnumProperty, BoolProperty, FloatProperty, PointerProperty, IntProperty, StringProperty


class DetacherPG(PropertyGroup):
    ''' MESH DETACHER '''
    go_sculpt_masked_mesh : BoolProperty(default = False, name="Go Sculpt Masked Mesh", description="Go to sculpt new mesh when detaching it from mask")
    detach_multi_objects : BoolProperty(default = True, name="Detach in Different Objects", description="Detach meshes into different objects")
    separate_loose_parts : BoolProperty(default = False, name="Detach By Mask Islands", description="Detach all loose parts, those that are separate meshes")
    close_detached_meshes : BoolProperty(default = True, name="Close Detached Meshes", description="Close hooles in the meshes made by the detacher")
    do_remesh : BoolProperty(default = True, name="Remesh it", description="Post-Remesh with voxel remesher")
    close_only_masked : BoolProperty(default = False, name="Only Masked", description="Remesh only masked part")
