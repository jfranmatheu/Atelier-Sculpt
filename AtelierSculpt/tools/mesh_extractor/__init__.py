def register():
    from .ops import classes
    from bpy.utils import register_class

    from .ui import BAS_PT_Mask_Extractor_Options
    register_class(BAS_PT_Mask_Extractor_Options)

    for cls in classes:
        register_class(cls)

    from .data import ExtractorPG
    register_class(ExtractorPG)

    from bpy.types import WindowManager as wm
    from bpy.props import PointerProperty as Pointer
    wm.bas_extractor = Pointer(type=ExtractorPG)

def unregister():
    from bpy.utils import unregister_class
    from bpy.types import WindowManager as wm
    del wm.bas_extractor

    from .data import ExtractorPG
    unregister_class(ExtractorPG)

    from .ui import BAS_PT_Mask_Extractor_Options
    unregister_class(BAS_PT_Mask_Extractor_Options)

    from .ops import classes
    for cls in reversed(classes):
        unregister_class(cls)
