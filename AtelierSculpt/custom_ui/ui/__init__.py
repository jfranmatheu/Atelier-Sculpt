from .add_menu import classes as ADD_MENU_CLASSES
from .context_menu import classes as CONTEXT_MENU_CLASSES
from .toolheader_dropdowns import classes as TOOLHEADER_DROPDOWN_CLASSES
from .header import BAS_HT_header
from .toolheader import BAS_HT_toolHeader

classes = [
    BAS_HT_header,
    BAS_HT_toolHeader
] + ADD_MENU_CLASSES + CONTEXT_MENU_CLASSES + TOOLHEADER_DROPDOWN_CLASSES

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
