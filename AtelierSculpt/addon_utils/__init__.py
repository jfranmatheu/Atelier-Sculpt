from .prefs import BAS_Preferences
from .updates import BAS_OT_CheckUpdates
from .save import FILE_OT_incremental_save
from .support import BAS_PT_dev_support

classes = [
    BAS_Preferences,
    BAS_OT_CheckUpdates,
    FILE_OT_incremental_save,
    BAS_PT_dev_support
]

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)