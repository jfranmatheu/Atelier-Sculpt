def register():
    from bpy.utils import register_class
    from bpy.types import WindowManager as wm
    from bpy.props import PointerProperty as Pointer
    from . data import MaskPG
    
    register_class(MaskPG)
    wm.bas_mask = Pointer(type=MaskPG)
    
    from . cavity import register as REGISTER_CAVITY
    REGISTER_CAVITY(register_class)

def unregister():
    from bpy.utils import unregister_class
    from . cavity import unregister as UNREGISTER_CAVITY
    UNREGISTER_CAVITY(unregister_class)

    from bpy.types import WindowManager as wm
    from . data import MaskPG
    del wm.bas_mask
    unregister_class(MaskPG)
