import bpy


def ShowMessageBox(_message = "", _title = "Message Box", _icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text=_message)
    bpy.context.window_manager.popup_menu(draw, title = _title, icon = _icon)


def override_context(area_type, region_type):
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == area_type:
                for region in area.regions:
                    if region.type == region_type:
                        return {
                            'window' : window,
                            #'screen' : window.screen,
                            'area' : area,
                            'region' : region
                        }
    return None

def blender_version() -> tuple:
    version = bpy.app.version
    return (version[0], version[1])

import uuid
def Generate_UUID():
    return str(uuid.uuid4())
