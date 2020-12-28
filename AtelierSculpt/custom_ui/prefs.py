from os.path import dirname, abspath, join, exists, isdir
from os import listdir

root = dirname(dirname(abspath(__file__)))
saved_custom_ui_folder_path = join(root, "user_data", "saved_custom_ui")


custom_ui_presets_list = [('NONE', "NONE", "")]
def custom_ui_preset_items(self, context):
    if not exists(self.saved_custom_ui_folder) or not isdir(self.saved_custom_ui_folder):
        return [('NONE', "NONE", "")]
    preset_paths = [f[:-5] for f in listdir(self.saved_custom_ui_folder) if f.endswith(".json")]
    custom_ui_presets_list.clear()
    for path in preset_paths:
        custom_ui_presets_list.append((path.replace(' ', '_'), path, ""))
    if custom_ui_presets_list:
        return custom_ui_presets_list
    else:
        return [('NONE', "NONE", "")]

# WRAPPER FOR LOAD CUSTOM UI PRESET METHOD.
def update_custom_ui_preset(self, context):
    from ..custom_ui.io import load_custom_ui_preset
    load_custom_ui_preset(context)

'''
custom_ui_properties = {
    # UI block specific.
    'brush_selector_grid_size' : (
        'IntVectorProperty',
        {
            'size'        :   2,
            'default'     :   [4, 10],
            'subtype'     :   'XYZ',
            'min'         :   2,
            'max'         :   16,
            'name'        :   "Grid Size",
            'description' :   "Set the number of rows and columns for the brush popover selector"
        }
    ),
    'texture_selector_grid_size' : (
        'IntVectorProperty',
        {
            'size'        :   2,
            'default'     :   [4, 10],
            'subtype'     :   'XYZ',
            'min'         :   2,
            'max'         :   16,
            'name'        :   "Grid Size",
            'description' :   "Set the number of rows and columns for the texture popover selector"
        }
    ),
    'image_selector_grid_size' : (
        'IntVectorProperty',
        {
            'size'        :   2,
            'default'     :   [4, 10],
            'subtype'     :   'XYZ',
            'min'         :   2,
            'max'         :   16,
            'name'        :   "Grid Size",
            'description' :   "Set the number of rows and columns for the image popover selector"
        }
    ),
    # General.
    'saved_custom_ui_folder' : (
        'StringProperty',
        {
            'subtype'     :   'DIR_PATH',
            'name'        :   "Saved Custom UI Folder path",
            'description' :   "",
            'default'     :   saved_custom_ui_folder_path
        }
    ),
    'custom_ui_presets' : (
        'EnumProperty',
        {
            'name'        :   "Preset list",
            'description' :   "",
            'items'       :   custom_ui_preset_items,
            'update'      :   update_custom_ui_preset
        }
    ),
    # Other UI Block specific properties.
    'voxel_size_presets' : (
        'FloatVectorProperty',
        {
            'size'        :   5,
            'default'     :   [.1, .05, .01, .005, .001],
            'subtype'     :   'NONE',
            'min'         :   .0001,
            'max'         :   1,
            'precision'   :   4,
            'step'        :   .005,
            'unit'        :   'LENGTH',
            'name'        :   "Voxel Size Presets",
            'description' :   "Preset Values for Voxel Size"
        }
    )
}
'''


custom_ui_properties = '''
brush_selector_grid_size : IntVectorProperty (
    size=2, default=[4, 10], subtype='XYZ', min=2, max=16,
    name="Grid Size", description="Set the number of rows and columns for the brush popover selector"
)
texture_selector_grid_size : IntVectorProperty (
    size=2, default=[4, 10], subtype='XYZ', min=2, max=16,
    name="Grid Size", description="Set the number of rows and columns for the texture popover selector"
)
image_selector_grid_size : IntVectorProperty (
    size=2, default=[4, 10], subtype='XYZ', min=2, max=16,
    name="Grid Size", description="Set the number of rows and columns for the image popover selector"
)

saved_custom_ui_folder : StringProperty (
    name="Saved Custom UI Folder path",
    subtype='DIR_PATH',
    default=saved_custom_ui_folder_path
)
custom_ui_presets : EnumProperty (
    items=custom_ui_preset_items, name="Preset list",
    update=update_custom_ui_preset
)

voxel_size_presets : FloatVectorProperty(
    name="Voxel Size Presets", description="Preset Values for Voxel Size",
    subtype='NONE', default=[.1, .05, .01, .005, .001], min=0.0001, max=1,
    size=5, step=.005, precision=4, unit='LENGTH'
)
'''
