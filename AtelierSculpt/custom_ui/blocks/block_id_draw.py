from enum import Enum, IntEnum
#from functools import partial
from .toolheader import BAS_HT_toolheader_blocks as draw
from .toolheader_default import DEFAULT_SCULPT_MODE_UI_BLOCKS as default


# NOTE: Only draw function call in enum (maybe with id) and ui_units_x is returned by
#       function, so when iter each value is stored for when editing is enabled.
class UI_BLOCK_DRAW(Enum):
    SEPARATOR                   = draw.separator
    B3D_PREFERENCES             = draw.blender_preferences
    SUPPORT                     = draw.dev_support
    BRUSH_SELECTOR              = draw.brush_selector
    BRUSH_OPTIONS               = draw.brush_options
    BRUSH_OPTIONS_COLL          = draw.brush_options_collapsed
    RENDER_BRUSH_ICON           = draw.render_brush_icon
    BAS_PREFERENCES             = draw.bas_preferences
    SETTINGS                    = draw.settings
    TEXTURE_MANAGER             = draw.texture_manager
    TEXTURE_OPTIONS             = draw.texture_options
    DYNTOPO_MULTIRES            = draw.dyntopo_multires
    SYMMETRY                    = draw.symmetry
    MIRROR_PLANE                = draw.mirror_plane
    MASK                        = draw.mask
    MASK_TOPOLOGY               = draw.mask_topology
    FRONTFACES                  = draw.front_faces
    FALLOFF                     = draw.falloff
    FALLOFF_PRESETS             = draw.falloff_presets
    FALLOFF_PRESETS_COLL        = draw.falloff_presets_collapse
    STROKE                      = draw.stroke
    STROKE_METHOD               = draw.stroke_method
    BRUSH_SETTINGS              = draw.brush_settings
    BRUSH_SETTINGS_ADVANCED     = draw.brush_settings_advanced
    SLIDER_RADIUS               = draw.slider_radius
    SLIDER_STRENGTH             = draw.slider_strength
    SLIDER_SMOOTH               = draw.slider_smooth
    SLIDER_SPACING              = draw.slider_spacing
    SLIDER_NORMAL_RADIUS        = draw.slider_normal_radius
    SLIDER_OTHERS               = draw.slider_others

    INCREMENTAL_SAVE            = draw.incremental_save

    DEF_SEPARATOR_SPACER        = default.separator_spacer

    DEF_BRUSH_SELECTOR          = default.brush_selector
    DEF_BRUSH_SETTINGS          = default.brush_settings
    DEF_OTHER_BRUSH_SETTINGS    = default.other_brush_settings
    DEF_DIRECTION               = default.direction
    DEF_BRUSH_RADIUS            = default.slider_radius
    DEF_BRUSH_STRENGTH          = default.slider_strength
    DEF_MIRROR                  = default.mirror
    DEF_STROKE_CURVE_SNAP       = default.stroke_curve_snap

    DEF_SWITCH_MODE             = default.switch_mode

    def __call__(self, *args):
        return self.value(*args)
