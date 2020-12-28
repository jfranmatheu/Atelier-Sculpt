def register():
    from bpy.utils import register_class as REGISTER
    from . ui import BAS_PT_mesh_filter as UI
    from . data import MeshFilter_Sliders as DATA
    from bpy.types import WindowManager as wm
    from bpy.props import PointerProperty as Pointer
    REGISTER(DATA)
    REGISTER(UI)
    wm.bas_meshfilter_sliders = Pointer(type=DATA)

def unregister():
    from bpy.utils import unregister_class as UNREGISTER
    from . ui import BAS_PT_mesh_filter as UI
    from . data import MeshFilter_Sliders as DATA
    from bpy.types import WindowManager as wm
    del wm.bas_meshfilter_sliders
    UNREGISTER(UI)
    UNREGISTER(DATA)
