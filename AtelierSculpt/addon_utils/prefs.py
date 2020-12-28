from os.path import dirname
import platform
platform = platform.system()

from bpy.types import AddonPreferences, UILayout
from bpy.props import StringProperty, FloatVectorProperty, BoolProperty, BoolVectorProperty, EnumProperty, IntVectorProperty
from ..icons import preview_collections
from ..import __package__ as main_package
from os.path import join

### PREFERENCES DATA SOURCES ###

from ..tools.dyntopo_pro.prefs import *
from ..custom_ui.prefs import *
from .updates import update_properties, update_auto_check_updates

prefs_properties = (
    dyntopo_properties,
    custom_ui_properties,
    update_properties
)

# ----------------------------------------------------------------- #
#   ADDON PREFERENCES                                               #
# ----------------------------------------------------------------- #

class BAS_Preferences(AddonPreferences):
    bl_idname = main_package
    
    '''
    prefs_properties = {}
    prefs_properties.update(dyntopo_properties)
    prefs_properties.update(custom_ui_properties)

    for key, value in prefs_properties.items():
        code = key + ' : ' + value[0] + '('
        for pptkey, pptvalue in value[1].items():
            # isinstance(pptvalue, str) and not pptvalue.startswith('update_') and not pptvalue.endswith('_items')
            val = '"' + str(pptvalue) + '"' if isinstance(pptvalue, str) and not pptvalue.startswith('x_') else str(pptvalue)
            code += pptkey + '=' + val + ','
        code = code[:-1] + ')'
        exec(code)
    '''
    
    for props in prefs_properties: exec(props)

    def get_custom_ui_presets(self, with_extension=True):
        real_name = UILayout.enum_item_name(self, 'custom_ui_presets', self.custom_ui_presets)
        return join(self.saved_custom_ui_folder,  (real_name + ".json") if with_extension else real_name)

    is_custom_tool_header_active : BoolProperty(name="Is Custom Tool Header Active", description="", default=True)
    is_custom_header_active : BoolProperty(name="Is Custom Header Active", description="", default=True)

    # FILE SAVE
    file_incremental_notation : StringProperty(
		description = "Incremental save notation for file",
		name        = "Incremental Notation",
		default     = "_v"
	)

    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        row = box.row()
        row.operator("bas.check_updates", text="Check for Updates", icon='RECOVER_LAST')
        row.prop(self, 'auto_check_updates', text="Auto-Check updates")
        row.scale_y = 1.3
        if self.need_updating:
            pcoll = preview_collections["main"]
            box.label(text="The version " + self.last_version + " is available !", icon='ERROR')
            row = box.row()
            prop = row.operator('wm.url_open', text="Cubebrush", icon_value=pcoll["cubebrush_icon"].icon_id)
            prop.url = "http://cbr.sh/qako92"
            prop = row.operator('wm.url_open', text="B3D Market", icon_value=pcoll["bMarket_icon"].icon_id)
            prop.url = "https://blendermarket.com/products/advanced-new-sculpt-mode-ui"

        box = layout.box()
        box.scale_y = 1.2
        box.active_default = self.is_custom_tool_header_active
        box.operator('bas.toolheader_activator', text="Use custom sculpt Tool Header")

        col = box.column(align=True)
        col.enabled = self.is_custom_tool_header_active
        col.prop(self, 'saved_custom_ui_folder')
        col.prop(self, 'custom_ui_presets')

        box = layout.box()
        box.scale_y = 1.2
        box.active_default = self.is_custom_header_active
        box.operator('bas.header_activator', text="Use custom sculpt Header")


        
        

        '''
        layout = self.layout
        layout.prop(self, "dyntopo_UseCustomValues", text="Use Custom Values for Dyntopo")
        box = layout.box()
        box.label(text="DYNTOPO: PER STAGES")
        box.active = self.dyntopo_UseCustomValues

        col = box.column(align=True)
        row = col.row(align=True)
        row.separator(factor=6)
        row.label(text="SKETCH")
        row.label(text="DETAIL")
        row.label(text="POLISH")

        _col = col.split().column(align=True)
        #col.label(text="Relative Values")
        _row = _col.row(align=False)
        _row.prop(self, "relative_Low", text="Relative")
        _row.prop(self, "relative_Mid", text="")
        _row.prop(self, "relative_High", text="")

        _col = col.split().column(align=True)
        #_col.label(text="Constant Values")
        _row = _col.row(align=False)
        _row.prop(self, "constant_Low", text="Constant")
        _row.prop(self, "constant_Mid", text="")
        _row.prop(self, "constant_High", text="")

        _col = col.split().column(align=True)
        #_col.label(text="Brush")
        _row = _col.row(align=False)
        _row.prop(self, "brush_Low", text="Brush")
        _row.prop(self, "brush_Mid", text="")
        _row.prop(self, "brush_High", text="")

        layout.separator()
        box = layout.box()
        col = box.column(align=True)
        col.label(text="CUSTOM UI PRESETS : ")
        row = col.row(align=True)
        row.prop(self, "create_custom_UI_Slot_1", text="Slot 1")
        #row = col.row(align=True)
        #row.prop(self, "custom_UI_Slot_1", text="UI Toggles")
        row = col.row(align=True)
        row.prop(self, "create_custom_UI_Slot_2", text="Slot 2")

        #layout.separator()
        #box = layout.box()
        #col = box.column()
        #row = col.row(align=True)
        #row.operator("bas.check_updates", text="Check for Updates")
        #row.operator("bas.update", text="Update")
        '''

    #def invoke(self, context, event):
    #    adress = 'https://newsmui-check-version.blogspot.com/p/recent-version.html' #https://newsmui-check-version.blogspot.com/
    #    response = urllib.request.urlopen(adress)
    #    html = str(response.read())
    #    version = html[536:545]

        #layout.label(text="PER LEVELS (BY DEFAULT MODE) : ")

