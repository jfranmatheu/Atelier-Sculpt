from bpy.types import PropertyGroup, Image as img
from bpy.props import *
from . previews import enum_previews_from_directory_items
from . prop_fun import *


class ReferenceSystemTempPG(PropertyGroup):
    # REFERENCE PREVIEWS 
    previews_dir : StringProperty(
        name="Folder Path",
        subtype='DIR_PATH',
        default=""
    )
    previews : EnumProperty(
        items=enum_previews_from_directory_items,
    )
    get_references_from : EnumProperty(
        items=(
            ('SINGLE', "Single Image", ""),
            ('FOLDER', "Folder", "")
        ),
        default='FOLDER'
    )
    ###
    ui_show_label : BoolProperty(description="Show Label Settings", default=False)
    ui_show_outline : BoolProperty(description="Show Outline Settings", default=False)

    hide_all : BoolProperty(name="Hide All references", description="Hide references", default=False, update=update_references_hide_all)
    lock_all : BoolProperty(name="Lock All references", description="Lock references", default=False, update=update_references_lock_all)
    
    image : PointerProperty(name="Image Reference", type=img)
    moving_reference : BoolProperty(default=False)
    keep_in_actual_mode : BoolProperty(default=False, name="Keep reference image in actual mode", description="This will allow you to restrict your references to be just drawing in the actual mode") # not button prop, this is ALL or mode name if it's true
    name : StringProperty(name="Reference Name", default="Reference Name")
    image_path : StringProperty(name="Image Path", subtype='FILE_PATH')
    use_label : BoolProperty(default=False, name="Use Label")
    label_text : StringProperty(name="Label Text", default="Label Text")
    label_text_color : FloatVectorProperty(name="Label Text Color", subtype='COLOR', default=(1,1,1,1), size=4, min=0, max=1, description="Label Text Color")
    label_color : FloatVectorProperty(name="Label Color", subtype='COLOR', default=(0,0,0,.5), size=4, min=0, max=1, description="Label Color")
    outline_color : FloatVectorProperty(name="Label Color", subtype='COLOR', default=(0,0,0,.5), size=4, min=0, max=1, description="Label Color")
    use_outline : BoolProperty(default=False, name="Use Outline")
    label_text_size : IntProperty(default=20, min=0, max=128, name="Label Text Size", description="Size for label text")
    label_thickness : FloatProperty(default=20, min=0, max=100, name="Label Thickness", description="Thickness for image label")
    label_text_align : EnumProperty (
        items=(
            ('LEFT', "Left", "", 'ALIGN_LEFT', 0),
            ('CENTER', "Center", "", 'ALIGN_CENTER', 1),
            ('RIGHT', "Right", "", 'ALIGN_RIGHT', 2)
        ),
        default='CENTER', name="Label Text Alignment", description="Label Text Alignment"
    )
    label_align : EnumProperty (
        items=(
            ('TOP', "Top", "", 'ALIGN_TOP', 0),
            #('MIDDLE', "Middle", "", 'ALIGN_MIDDLE'),
            ('BOTTOM', "Bottom", "", 'ALIGN_BOTTOM', 1)
        ),
        default='TOP', name="Label Text Alignment", description="Label Text Alignment"
    )
    label_direction : EnumProperty (
        items=(
            ('HORIZONTAL', "Horizontal", ""),
            ('VERTICAL', "Vertical", "")
        ),
        default='HORIZONTAL', name="Label Direction", description="Label Direction"
    )
    label_text_padding : FloatProperty(default=10, min=0, max=50, name="Label Text Padding", description="Padding for label text")


class ReferenceSystemPG(PropertyGroup):
    data_base : StringProperty(name="References Data Base Path", subtype='FILE_PATH')
    is_using_references : BoolProperty(default=False, name="Is this project using references?")
    num_of_references : IntProperty(default=0, name="Number of references")
    save_references_mode : EnumProperty (items=(('INTERNAL', "Internally", ""),('EXTERNAL', "Externally", ""),), default='INTERNAL', name="Save References Mode")


# REFERENCE PROPERTIES
class ReferenceImagePG(PropertyGroup):
    uuid : StringProperty(default='') # Reference Unic ID
    is_reference : BoolProperty(default=False) # Is this image a reference image?
    mode : StringProperty(default='ALL') # ALL is visibility for all modes, if not it's 'OBJECT', 'EDIT', etc...
    signal : StringProperty(default='') # empty it's ok, visible, H is hidden, R is remove, etc...
    is_locked : BoolProperty(default=False)
    position : FloatVectorProperty(default=(0,0), size=2) # (X, Y)
    size : FloatVectorProperty(default=(0,0), size=2) # Width x Height
    use_transparency : BoolProperty(default=False)
    use_label : BoolProperty(default=False)
    label_color : FloatVectorProperty(default=(1, 1, 1, .5), size=4, subtype='COLOR', min=0, max=1)
    label_thickness : FloatProperty(default=20, min=10, max=100)
    label_align_to : StringProperty(default='TOP')
    label_text : StringProperty(default="Label Tetxt")
    label_text_size : IntProperty(default=20)
    label_text_align : StringProperty(default='CENTER')
    label_text_color : FloatVectorProperty(default=(0, 0, 0, 1), size=4, subtype='COLOR', min=0, max=1)
    use_outline : BoolProperty(default=False)
    outline_color : FloatVectorProperty(default=(1, 1, 1, .5), size=4, subtype='COLOR', min=0, max=1)
    name : StringProperty(default="Reference Name")
    in_front : BoolProperty(default=True)
