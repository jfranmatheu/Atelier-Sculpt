def register():
    from .ops import classes
    from bpy.utils import register_class

    from .ui import BAS_PT_Close_Gaps_Options
    register_class(BAS_PT_Close_Gaps_Options)

    for cls in classes:
        register_class(cls)

    from .data import MeshCloseGapsPG
    register_class(MeshCloseGapsPG)

    from bpy.types import WindowManager as wm
    from bpy.props import PointerProperty as Pointer
    wm.bas_closegaps = Pointer(type=MeshCloseGapsPG)

def unregister():
    from bpy.utils import unregister_class
    from bpy.types import WindowManager as wm
    del wm.bas_closegaps

    from .data import MeshCloseGapsPG
    unregister_class(MeshCloseGapsPG)

    from .ui import BAS_PT_Close_Gaps_Options
    unregister_class(BAS_PT_Close_Gaps_Options)

    from .ops import classes
    for cls in reversed(classes):
        unregister_class(cls)
