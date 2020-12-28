def register():
    from bpy.utils import register_class as REGISTER
    from . panel import BAS_PT_experimental_panel as Experimental_Base_Panel
    from . non_destructive import register as REGISTER_NONDESTRUCTIVE
    from . mesh_filters import register as REGISTER_MESHFILTERS
    REGISTER(Experimental_Base_Panel)
    REGISTER_NONDESTRUCTIVE()
    #REGISTER_MESHFILTERS()

def unregister():
    from bpy.utils import unregister_class as UNREGISTER
    from . panel import BAS_PT_experimental_panel as Experimental_Base_Panel
    from . non_destructive import unregister as UNREGISTER_NONDESTRUCTIVE
    from . mesh_filters import unregister as UNREGISTER_MESHFILTERS
    UNREGISTER_NONDESTRUCTIVE()
    #UNREGISTER_MESHFILTERS()
    UNREGISTER(Experimental_Base_Panel)
