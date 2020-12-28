def register():
    from .ops import classes
    from bpy.utils import register_class

    from .ui import BAS_PT_dyntopo_stages
    register_class(BAS_PT_dyntopo_stages)

    for cls in classes:
        register_class(cls)

    from .data import DyntopoProPG
    register_class(DyntopoProPG)

    from bpy.types import Scene as scn
    from bpy.props import PointerProperty as Pointer
    scn.bas_dyntopo = Pointer(type=DyntopoProPG)

def unregister():
    from bpy.utils import unregister_class
    from bpy.types import Scene as scn
    del scn.bas_dyntopo

    from .data import DyntopoProPG
    unregister_class(DyntopoProPG)

    from .ui import BAS_PT_dyntopo_stages
    unregister_class(BAS_PT_dyntopo_stages)

    from .ops import classes
    for cls in reversed(classes):
        unregister_class(cls)
