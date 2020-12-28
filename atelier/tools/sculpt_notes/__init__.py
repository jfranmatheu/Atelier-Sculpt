def register():
    from .ops import classes
    from bpy.utils import register_class

    from .ui import BAS_PT_sculpt_notes
    register_class(BAS_PT_sculpt_notes)
    
    from .utils import utils_classes
    for cls in utils_classes:
        register_class(cls)
        
    from .ops_curves import curve_classes
    for cls in curve_classes:
        register_class(cls)

    for cls in classes:
        register_class(cls)

    from .data import SculptNotesPG
    register_class(SculptNotesPG)

    from bpy.types import WindowManager as wm
    from bpy.props import PointerProperty as Pointer
    wm.bas_sculptnotes = Pointer(type=SculptNotesPG)

def unregister():
    from bpy.utils import unregister_class
    from bpy.types import WindowManager as wm
    del wm.bas_sculptnotes

    from .data import SculptNotesPG
    unregister_class(SculptNotesPG)

    from .ui import BAS_PT_sculpt_notes
    unregister_class(BAS_PT_sculpt_notes)

    from .ops import classes
    for cls in reversed(classes):
        unregister_class(cls)
        
    from .ops_curves import curve_classes
    for cls in reversed(curve_classes):
        unregister_class(cls)
    
    from .utils import utils_classes
    for cls in reversed(utils_classes):
        unregister_class(cls)
