from .utilities.falloff import BAS_OT_falloff_curve_presets
from .utilities.brush_utils import BAS_OT_brush_remove
from .utilities.activator import BAS_OT_header_activator, BAS_OT_toolHeader_activator
from .edit import BAS_OT_edit_custom_ui
from .ui_blocks import classes as UI_BLOCKS_CLASSES
from .ui_presets import classes as UI_PRESETS_CLASSES

classes = [
    BAS_OT_falloff_curve_presets,
    BAS_OT_brush_remove,
    BAS_OT_edit_custom_ui,
    BAS_OT_header_activator,
    BAS_OT_toolHeader_activator
] + UI_BLOCKS_CLASSES + UI_PRESETS_CLASSES

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
