from bpy.types import Panel
from .. import bl_info, __package__ as main_package
from ..icons import Icon

# ----------------------------------------------------------------- #
#   DEV SUPPORT                                     #
# ----------------------------------------------------------------- #

class BAS_PT_dev_support(Panel):
    bl_label = "Updates"
    bl_description = "Check for updates. Support."
    bl_category = 'Sculpt'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "NONE"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        # LOAD COLLECTION OF ICONS
        prefs = context.preferences.addons[main_package].preferences
        row = self.layout.row()
        row.label(text="SUPPORT THE DEVELOPMENT :")

        box = self.layout.box().column()
        box.label(text="Report a Bug / Make a Proposal")
        _prop = box.operator('wm.url_open', text="GO !")
        _prop.url = "https://trello.com/invite/b/rGqXWJjA/78593a39edca80af604e0f2b62e0851d/blender-atelier-sculpt" # https://trello.com/b/rGqXWJjA/blender-atelier-sculpt


        box = self.layout.box()
        row = box.row()
        row.label(text="DONATION")
        row = box.row()
        prop = row.operator('wm.url_open', text="Paypal", icon_value=Icon.PAYPAL())
        prop.url = "https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=BA3UXNSDLE55E&source=url"

        row = box.row()
        row.label(text="DOWNLOAD / UPDATES")
        row = box.row()

        row.operator("bas.check_updates", text="Check for Updates", icon='RECOVER_LAST')
        row.scale_y = 1.3

        row = box.row()
        if prefs.need_updating:
            row.alert = True
            row.label(text="New Version !  -  " + prefs.last_version)

            row = box.row()
            row.alert = True
        else:
            _row = box.row()
            _row.label(text="Version is up to date !  -  " + str(bl_info['version']))

        _prop = row.operator('wm.url_open', text="Cubebrush", icon_value=Icon.CUBEBRUSH())
        _prop.url = "http://cbr.sh/qako92"
        __prop = row.operator('wm.url_open', text="B3d Market", icon_value=Icon.BMARKET())
        __prop.url = "https://blendermarket.com/products/advanced-new-sculpt-mode-ui"