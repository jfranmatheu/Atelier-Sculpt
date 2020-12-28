def register():
    from bpy.utils import register_class
    
    from .ops import classes as OPS_CLASSES
    for cls in OPS_CLASSES:
        register_class(cls)

    from .ui import classes as UI_CLASSES
    for cls in UI_CLASSES:
        register_class(cls)

    from .data import BrushManagementPG
    register_class(BrushManagementPG)

    from bpy.types import Scene as scn
    from bpy.props import PointerProperty as Pointer
    scn.bas_brush_management = Pointer(type=BrushManagementPG)

def unregister():
    from bpy.utils import unregister_class
    
    from bpy.types import Scene as scn
    del scn.bas_brush_management

    from .data import BrushManagementPG
    unregister_class(BrushManagementPG)

    from .ops import classes as OPS_CLASSES
    for cls in reversed(OPS_CLASSES):
        unregister_class(cls)

    from .ui import classes as UI_CLASSES
    for cls in reversed(UI_CLASSES):
        unregister_class(cls)
