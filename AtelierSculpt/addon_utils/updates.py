from bpy.types import Operator
from .. import bl_info, __package__ as main_package
from bpy.props import BoolProperty

# ----------------------------------------------------------------- #
#  UPDATES
# ----------------------------------------------------------------- #

def check_update():
    import urllib
    import re
    adress = 'https://raw.githubusercontent.com/jfranmatheu/b3d_addons/main/versions/AtelierSculpt.txt'
    response = urllib.request.urlopen(adress)
    html = str(response.read())
    result = re.search('version:(.*);', html)
    last_version = result.group(1)
    current_version = str(bl_info['version'])
    print("[Atelier Sculpt] Current Version :", current_version)
    print("[Atelier Sculpt] Last Version :", last_version)
    if last_version != current_version:
        return True, last_version
    else:
        return False, False
    
def update_auto_check_updates(self, context):
    if self.auto_check_updates:
        import bpy
        bpy.ops.bas.check_updates()

class BAS_OT_CheckUpdates(Operator):
    bl_idname = "bas.check_updates"
    bl_label = "Check for 'Atelier Sculpt' Updates"
    
    second_plane : BoolProperty(default=False)

    def error(self, ui, context):
        ui.layout.label(text="Do you have Internet Conection? If yes, please report it.")

    def nope(self, ui, context):
        ui.layout.label(text="You are up to date!")

    def success(self, ui, context):
        ui.layout.label(text="New Version Available!")

    def execute(self, context):
        prefs = context.preferences.addons[main_package].preferences
        try:
            prefs.need_updating, last = check_update()
            if not last:
                if not self.second_plane:
                    context.window_manager.popup_menu(self.nope, title = "Version " + str(bl_info['version']) + " is the last one", icon = 'INFO')
                return {'FINISHED'}
            else:
                prefs.last_version = last
            if prefs.need_updating:
                if not self.second_plane:
                    context.window_manager.popup_menu(self.success, title = "Version " + prefs.last_version + " was found", icon = 'INFO')
                else:
                    self.report({'INFO'}, "Atelier Sculpt: new update available - " + last)
        except:
            if not self.second_plane:
                context.window_manager.popup_menu(self.error, title = "Can't Check for Updates!", icon = 'ERROR')
            print("[ATELIER SCULPT] WARNING: Can't Check for updates! Please Report it!")
        return {'FINISHED'}


update_properties = '''
need_updating : BoolProperty(
    description = "Need Updating",
    name        = "need_updating",
    default     = False
)

last_version : StringProperty(
    description = "Last Version",
    name        = "last_version",
    default     = "(2.0.0)"
)

auto_check_updates : BoolProperty(default=True, name="Auto-Check for Updates", update=update_auto_check_updates)
'''
