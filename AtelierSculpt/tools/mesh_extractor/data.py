from bpy.types import PropertyGroup, Object
from bpy.props import EnumProperty, BoolProperty, FloatProperty, PointerProperty, IntProperty, StringProperty


class ExtractorPG(PropertyGroup):
    ''' MASK EXTRACTOR '''
    is_created : BoolProperty(default=False)
    super_smooth : BoolProperty(default = True, name="Super Smooth")
    offset : FloatProperty(min = -10.0, max = 10.0, default = 0.1, name="Offset")
    thickness : FloatProperty(min = 0.0, max = 1.0, default = 0.05, name="Thickness")
    smooth_passes : IntProperty(min = 0, max = 30, default = 15, name="Smooth Passes")
    smooth_borders : BoolProperty(default = True, name="Smooth Borders")
    mode : EnumProperty(name="Extract Mode",
                     items = (("SOLID","Solid","Solid, two sided"),
                              ("SINGLE","One Side","Like Solid mode but only one sided (front)"),
                              ("FLAT","Flat","Just a flat copy of the mask selection"),
                              ("BLENDER","Blender","New Extract Mask method from Blender by Pablo Dobarro")),
                     default = "SOLID", description="Mode in how to apply the mask extraction"
    )
    edit_new_mesh : BoolProperty(default = True, name="Sculpt New Mesh", description="Sculpt new mesh when extracting it from mask")
    keep_mask : BoolProperty(default = False, name="Keep Mask", description="Keep Original Mask")
    post_edition : BoolProperty(default = False, name="Post-Edition", description="Be able to edit some values after extracting, the apply changes.")
    extracted : PointerProperty(type=Object, name="Mesh Extracted", description="Object extracted by the mask extractor")
