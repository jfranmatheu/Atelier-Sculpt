def register():
    from bpy.utils import register_class
    
    from .previews import register_previews
    register_previews()
    
    from .data import ReferenceSystemPG, ReferenceSystemTempPG, ReferenceImagePG
    register_class(ReferenceSystemPG)
    register_class(ReferenceSystemTempPG)
    register_class(ReferenceImagePG)

    from bpy.types import WindowManager as wm, Scene as scn, Image as img
    from bpy.props import PointerProperty as Pointer
    wm.bas_references = Pointer(type=ReferenceSystemTempPG)
    scn.bas_references = Pointer(type=ReferenceSystemPG)
    img.ref = Pointer(type=ReferenceImagePG)

    from .ui import classes as UI_CLASSES
    for cls in UI_CLASSES:
        register_class(cls)

    from .ops import classes as OPS_CLASSES
    for cls in OPS_CLASSES:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class

    from .ops import classes as OPS_CLASSES
    for cls in reversed(OPS_CLASSES):
        unregister_class(cls)
        
    from .ui import classes as UI_CLASSES
    for cls in reversed(UI_CLASSES):
        unregister_class(cls)
    
    from bpy.types import WindowManager as wm, Scene as scn, Image as img
    del wm.bas_references
    del scn.bas_references
    del img.ref

    from .data import ReferenceSystemPG, ReferenceSystemTempPG, ReferenceImagePG
    unregister_class(ReferenceSystemTempPG)
    unregister_class(ReferenceSystemPG)
    unregister_class(ReferenceImagePG)
    
    from .previews import unregister_previews
    unregister_previews()
