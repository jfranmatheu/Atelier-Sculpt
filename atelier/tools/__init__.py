def register():
    from .mesh_close_gaps import register as REGISTER_CLOSEGAPS
    from .remesh import register as REGISTER_REMESH
    from .sculpt_notes import register as REGISTER_SCULPTNOTES
    from .mesh_extractor import register as REGISTER_EXTRACTOR
    from .mesh_detacher import register as REGISTER_DETACHER
    from .mask import register as REGISTER_MASK
    from .brush_thumbnailer import register as REGISTER_BRUSH_THUMBNAILER
    from .dyntopo_pro import register as REGISTER_DYNTOPO
    from .rmb import register as REGISTER_RMB
    from .mirror_plane import register as REGISTER_MIRRORPLANE
    from .brush_management import register as REGISTER_BRUSH_MANAGEMENT
    from .reference_system import register as REGISTER_REFERENCE_SYSTEM
    from .texture_management import register as REGISTER_TEXTURE_MANAGEMENT
    REGISTER_CLOSEGAPS()
    REGISTER_REMESH()
    REGISTER_SCULPTNOTES()
    REGISTER_EXTRACTOR()
    REGISTER_DETACHER()
    REGISTER_MASK()
    REGISTER_BRUSH_THUMBNAILER()
    REGISTER_DYNTOPO()
    REGISTER_RMB()
    REGISTER_MIRRORPLANE()
    REGISTER_BRUSH_MANAGEMENT()
    REGISTER_REFERENCE_SYSTEM()
    REGISTER_TEXTURE_MANAGEMENT()

def unregister():
    from .mesh_close_gaps import unregister as UNREGISTER_CLOSEGAPS
    from .sculpt_notes import unregister as UNREGISTER_SCULPTNOTES
    from .remesh import unregister as UNREGISTER_REMESH
    from .mesh_extractor import unregister as UNREGISTER_EXTRACTOR
    from .mesh_detacher import unregister as UNREGISTER_DETACHER
    from .mask import unregister as UNREGISTER_MASK
    from .brush_thumbnailer import unregister as UNREGISTER_BRUSH_THUMBNAILER
    from .dyntopo_pro import unregister as UNREGISTER_DYNTOPO
    from .rmb import unregister as UNREGISTER_RMB
    from .mirror_plane import unregister as UNREGISTER_MIRRORPLANE
    from .brush_management import unregister as UNREGISTER_BRUSH_MANAGEMENT
    from .reference_system import unregister as UNREGISTER_REFERENCE_SYSTEM
    from .texture_management import unregister as UNREGISTER_TEXTURE_MANAGEMENT
    UNREGISTER_SCULPTNOTES()
    UNREGISTER_REMESH()
    UNREGISTER_CLOSEGAPS()
    UNREGISTER_EXTRACTOR()
    UNREGISTER_DETACHER()
    UNREGISTER_MASK()
    UNREGISTER_BRUSH_THUMBNAILER()
    UNREGISTER_DYNTOPO()
    UNREGISTER_RMB()
    UNREGISTER_MIRRORPLANE()
    UNREGISTER_BRUSH_MANAGEMENT()
    UNREGISTER_REFERENCE_SYSTEM()
    UNREGISTER_TEXTURE_MANAGEMENT()
