
from enum import Enum
# OLD
# float / tuple or None / float tuple / dict or None
# IDENTIFIER                = [DEF_WIDTH, MIN_MAX_WIDTH, PROPERTIES]

class UI_BLOCK_PPTS(Enum):
    # IDENTIFIER                # None -> No properties
                                # Dict with property name followed by its type ('_' if is prefs property)
    SEPARATOR                   =   None
    B3D_PREFERENCES             =   ()
    SUPPORT                     =   ()
    BRUSH_SELECTOR              =   {
        '_brush_selector_grid_size': int
    }
    BRUSH_OPTIONS               =   {
        'brush_options_show_reset': bool,
        'brush_options_show_remove': bool
    }
    BRUSH_OPTIONS_COLL          =   None
    RENDER_BRUSH_ICON           =   None
    BAS_PREFERENCES             =   None
    SETTINGS                    =   None
    TEXTURE_MANAGER             =   {
        '_texture_selector_grid_size': int,
        '_image_selector_grid_size': int
    }
    TEXTURE_OPTIONS             =   {
        'texture_options_show_new_texture': bool,
        'texture_options_show_open_image': bool
    }
    DYNTOPO_MULTIRES            =   None
    MIRROR                      =   None
    MIRROR_PLANE                =   None
    MASK                        =   None
    MASK_TOPOLOGY               =   None
    FRONTFACES                  =   None
    FALLOFF                     =   None
    FALLOFF_PRESETS             =   None
    FALLOFF_PRESETS_COLL        =   None
    STROKE                      =   None
    STROKE_METHOD               =   None
    BRUSH_SETTINGS              =   None
    SLIDER_RADIUS               =   None
    SLIDER_STRENGTH             =   None
    SLIDER_SMOOTH               =   None
    SLIDER_SPACING              =   None
    SLIDER_NORMAL_RADIUS        =   None
    SLIDER_OTHERS               =   None
    INCREMENTAL_SAVE            =   {
        '_file_incremental_notation': str,
    }

    DEF_SEPARATOR_SPACER        =   None
    DEF_BRUSH_SELECTOR          =   {
        '_brush_selector_grid_size': int
    }
    DEF_BRUSH_SETTINGS          =   None
    DEF_OTHER_BRUSH_SETTINGS    =   None
    DEF_DIRECTION               =   None
    DEF_BRUSH_RADIUS            =   None
    DEF_BRUSH_STRENGTH          =   None
    DEF_MIRROR                  =   None
    DEF_STROKE_CURVE_SNAP       =   None

    DEF_SWITCH_MODE             =   None


    def __call__(self):
        return self.value