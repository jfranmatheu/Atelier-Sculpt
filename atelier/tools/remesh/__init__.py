def register():
    from .utils import utils_classes
    from .ops import classes
    from bpy.utils import register_class

    from .ui import BAS_PT_remesh_options
    register_class(BAS_PT_remesh_options)

    for cls in utils_classes:
        register_class(cls)

    for cls in classes:
        register_class(cls)

    from .data import RemeshPG
    register_class(RemeshPG)

    from bpy.types import WindowManager as wm
    from bpy.props import PointerProperty as Pointer
    wm.bas_remesh = Pointer(type=RemeshPG)

def unregister():
    from bpy.utils import unregister_class
    from bpy.types import WindowManager as wm
    del wm.bas_remesh

    from .data import RemeshPG
    unregister_class(RemeshPG)

    from .ui import BAS_PT_remesh_options
    unregister_class(BAS_PT_remesh_options)

    from .ops import classes
    for cls in reversed(classes):
        unregister_class(cls)

    from .utils import utils_classes
    for cls in reversed(utils_classes):
        unregister_class(cls)
