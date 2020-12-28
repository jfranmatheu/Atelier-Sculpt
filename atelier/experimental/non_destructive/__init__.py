def register():
    from .ops import classes
    from bpy.utils import register_class

    from .ui import BAS_PT_non_destructive_sculpting
    register_class(BAS_PT_non_destructive_sculpting)

    for cls in classes:
        register_class(cls)

    from .data import NonDestructiveSculptingPG, SculptLayer, Stroke
    register_class(Stroke)
    register_class(SculptLayer)
    register_class(NonDestructiveSculptingPG)

    from bpy.types import WindowManager as wm
    from bpy.props import PointerProperty as Pointer
    wm.bas_nondestructive = Pointer(type=NonDestructiveSculptingPG)

def unregister():
    from bpy.utils import unregister_class
    from bpy.types import WindowManager as wm
    del wm.bas_nondestructive

    from .data import NonDestructiveSculptingPG, SculptLayer, Stroke
    unregister_class(NonDestructiveSculptingPG)
    unregister_class(SculptLayer)
    unregister_class(Stroke)

    from .ui import BAS_PT_non_destructive_sculpting
    unregister_class(BAS_PT_non_destructive_sculpting)

    from .ops import classes
    for cls in reversed(classes):
        unregister_class(cls)
