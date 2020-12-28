from bpy.utils import register_class, unregister_class
from bpy.app.handlers import persistent, load_post, load_factory_startup_post
from .. import __package__ as main_package

# CLASSES
from .ui.toolheader import BAS_HT_toolHeader, ToolHeader
from .ui.header import BAS_HT_header
from .ui.header_append import temporal_tool_header_buttons
from bl_ui.space_view3d import VIEW3D_HT_header as Header
from .ops.utilities.activator import BAS_OT_header_activator, BAS_OT_toolHeader_activator
from .ui.toolheader_dropdowns import classes as DROPDOWN_CLASSES
from .ui.context_menu import menu_ctx_tool_header, WM_MT_button_context

# INTERFACE RELATED
from .ui import register as REGISTER_UI, unregister as UNREGISTER_UI

# DATA RELATED
from .data import (
    classes as UI_DATA_CLASSES,
    ToolHeader_PG_custom_ui as CustomUIPG,
)

def register_data():
    for cls in UI_DATA_CLASSES:
        register_class(cls)
    from bpy.types import Scene as scn, WindowManager as wm
    from bpy.props import PointerProperty as Pointer
    scn.bas_custom_ui = Pointer(type=CustomUIPG)

def unregister_data():
    for cls in reversed(UI_DATA_CLASSES):
        unregister_class(cls)
    from bpy.types import Scene as scn, WindowManager as wm
    del scn.bas_custom_ui

# OPS RELATED
from .ops import register as REGISTER_OPS, unregister as UNREGISTER_OPS

# LOADER.
@persistent
def on_load_handler(dummy):
    from bpy import context as C

    prefs = C.preferences.addons[main_package].preferences

    from os.path import exists
    if prefs.saved_custom_ui_folder == '' or not exists(prefs.saved_custom_ui_folder):
        from os.path import dirname, abspath, join
        root = dirname(dirname(abspath(__file__)))
        prefs.saved_custom_ui_folder = join(root, "user_data", "saved_custom_ui")

    from .io import load_custom_ui_preset
    load_custom_ui_preset(C)
    
    if prefs.auto_check_updates:
        from bpy import ops as OP
        print("[ATELIER SCULPT] Auto-checking for updates...")
        OP.bas.check_updates(second_plane=True)

def register():
    REGISTER_OPS()

    Header.append(temporal_tool_header_buttons)

    try:
        unregister_class(ToolHeader)
    except:
        print("[ATELIER SCULPT] ERROR: TOOL HEADER NOT REGISTERED !")
    try:
        unregister_class(Header)
    except:
        print("[ATELIER SCULPT] ERROR: HEADER NOT REGISTERED !")
    REGISTER_UI()

    register_data()

    load_post.append(on_load_handler)
    load_factory_startup_post.append(on_load_handler)

    try:
        from bpy.types import WM_MT_button_context
        WM_MT_button_context.prepend(menu_ctx_tool_header)
    except RuntimeError as e:
        print(e)

    BAS_HT_header.append(temporal_tool_header_buttons)

def unregister():
    try:
        from bpy.types import WM_MT_button_context
        WM_MT_button_context.remove(menu_ctx_tool_header)
    except RuntimeError as e:
        print(e)

    BAS_HT_header.remove(temporal_tool_header_buttons)

    UNREGISTER_UI()
    register_class(ToolHeader)
    register_class(Header)

    unregister_data()

    load_post.remove(on_load_handler)

    Header.remove(temporal_tool_header_buttons)

    UNREGISTER_OPS()
