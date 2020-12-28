from bpy.types import PropertyGroup, Brush
from bpy.props import (
    EnumProperty, BoolProperty, IntProperty, PointerProperty as Pointer
)


class BrushManagementPG(PropertyGroup):
    toggle_brush_preview : BoolProperty(default=True, name="Toggle Brush Preview")
    toggle_brush_favourites : BoolProperty(default=True, name="Toggle Favourite Brushes")
    toggle_brush_pertype : BoolProperty(default=True, name="Toggle Per Type Brushes")
    toggle_brush_recents : BoolProperty(default=True, name="Toggle Recent Brushes")
    
    show_brush_options : BoolProperty(default=True, name="Show Brush Options")
    show_brush_favourites : BoolProperty(default=True, name="Show Favourite Brushes")
    show_brush_pertype : BoolProperty(default=True, name="Show Per Type Brushes")
    show_brush_recents : BoolProperty(default=True, name="Show Recent Brushes")
    
    show_only_icons : BoolProperty(default=False, name="Show Only Brush Icons")
    recent_brushes_stay_in_place : BoolProperty(default=False, name="Recent Brushes: stay in place")
