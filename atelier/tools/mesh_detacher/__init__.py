def register():
    from .ops import classes
    from bpy.utils import register_class

    from .ui import BAS_PT_Mesh_Detacher_Options
    register_class(BAS_PT_Mesh_Detacher_Options)

    for cls in classes:
        register_class(cls)

    from .data import DetacherPG
    register_class(DetacherPG)

    from bpy.types import WindowManager as wm
    from bpy.props import PointerProperty as Pointer
    wm.bas_detacher = Pointer(type=DetacherPG)

def unregister():
    from bpy.utils import unregister_class
    from bpy.types import WindowManager as wm
    del wm.bas_detacher

    from .data import DetacherPG
    unregister_class(DetacherPG)

    from .ui import BAS_PT_Mesh_Detacher_Options
    unregister_class(BAS_PT_Mesh_Detacher_Options)

    from .ops import classes
    for cls in reversed(classes):
        unregister_class(cls)
