def register():
    from .ops import classes
    from bpy.utils import register_class

    from .ui import BAS_PT_mirror_plane_options
    register_class(BAS_PT_mirror_plane_options)

    for cls in classes:
        register_class(cls)

    from .data import MirrorPlanePG
    register_class(MirrorPlanePG)

    from bpy.types import Scene as scn
    from bpy.props import PointerProperty as Pointer
    scn.bas_mirrorplane = Pointer(type=MirrorPlanePG)

def unregister():
    from bpy.utils import unregister_class
    from bpy.types import Scene as scn
    del scn.bas_mirrorplane

    from .data import MirrorPlanePG
    unregister_class(MirrorPlanePG)

    from .ui import BAS_PT_mirror_plane_options
    unregister_class(BAS_PT_mirror_plane_options)

    from .ops import classes
    for cls in reversed(classes):
        unregister_class(cls)
