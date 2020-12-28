def register():
    from .ops import classes
    from bpy.utils import register_class

    from .ui import BrushThumbnailerOptions
    register_class(BrushThumbnailerOptions)

    for cls in classes:
        register_class(cls)

    from .data import BrushThumbnailerPG
    register_class(BrushThumbnailerPG)

    from bpy.types import WindowManager as wm
    from bpy.props import PointerProperty as Pointer
    wm.bas_brush_thumbnailer = Pointer(type=BrushThumbnailerPG)

def unregister():
    from bpy.utils import unregister_class
    from bpy.types import WindowManager as wm
    del wm.bas_brush_thumbnailer

    from .data import BrushThumbnailerPG
    unregister_class(BrushThumbnailerPG)

    from .ui import BrushThumbnailerOptions
    unregister_class(BrushThumbnailerOptions)

    from .ops import classes
    for cls in reversed(classes):
        unregister_class(cls)
