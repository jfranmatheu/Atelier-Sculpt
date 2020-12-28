from bl_ui.properties_paint_common import UnifiedPaintPanel
from bpy.types import ToolSettings

class DEFAULT_SCULPT_MODE_UI_BLOCKS:
    #   SPACING // SEPARATOR_SPACING
    def separator_spacer(parent):
        parent.layout.separator_spacer()
        return 0

    def switch_mode(parent):
        row = parent.layout.row(align=True)
        row.ui_units_x = 1.6
        row.template_header()
        return row.ui_units_x

    def brush_type_icon(parent):
        return 3

    def brush_selector(parent):
        paint_settings = UnifiedPaintPanel.paint_settings(parent.context)
        if paint_settings:
            rows_cols = parent.prefs.brush_selector_grid_size
            parent.layout.template_ID_preview(paint_settings, "brush", rows=rows_cols[0], cols=rows_cols[1], hide_buttons=True)
            return 7.6
        return -1

    def brush_settings(parent):
        row = parent.layout.row()
        row.popover("VIEW3D_PT_tools_brush_settings_advanced", text="Brush")
        row.popover("VIEW3D_PT_tools_brush_stroke")
        row.popover("VIEW3D_PT_tools_brush_falloff")
        row.popover("VIEW3D_PT_tools_brush_display")

        return 12.3

    def slider_radius(parent):
        size = "size"
        size_owner = parent.ups if parent.ups.use_unified_size else parent.brush
        if size_owner.use_locked_size == 'SCENE':
            size = "unprojected_radius"

        UnifiedPaintPanel.prop_unified(
            parent.layout,
            parent.context,
            parent.brush,
            size,
            pressure_name="use_pressure_size",
            unified_name="use_unified_size",
            text="Radius",
            slider=True,
            header=True
        )
        return 7.3

    def slider_strength(parent):
        # strength, use_strength_pressure
        pressure_name = "use_pressure_strength" if parent.capabilities.has_strength_pressure else None
        UnifiedPaintPanel.prop_unified(
            parent.layout,
            parent.context,
            parent.brush,
            "strength",
            pressure_name=pressure_name,
            unified_name="use_unified_strength",
            text="Strength",
            header=True
        )
        return 7.75

    def direction(parent):
        # direction
        if not parent.capabilities.has_direction:
            row = parent.layout.row()
            row.ui_units_x = 1.9
            row.prop(parent.brush, "direction", expand=True, text="")
            return row.ui_units_x
        return -1

    def mirror(parent):
        row = parent.layout.row(align=True)
        row.ui_units_x = 4.5
        row.label(icon='MOD_MIRROR')
        sub = row.row(align=True)
        sub.scale_x = 0.6
        sculpt = parent.sculpt
        sub.prop(sculpt, "use_symmetry_x", text="X", toggle=True)
        sub.prop(sculpt, "use_symmetry_y", text="Y", toggle=True)
        sub.prop(sculpt, "use_symmetry_z", text="Z", toggle=True)
        row.popover(panel="VIEW3D_PT_sculpt_symmetry_for_topbar", text="")

        return 4.5 # sub.scale_x * 3 + 2.66

    def other_brush_settings(parent):
        # Expand panels from the side-bar as popovers.
        popover_kw = {"space_type": 'VIEW_3D', "region_type": 'UI', "category": "Tool"}
        parent.layout.popover_group(context=".sculpt_mode", **popover_kw)
        return 11.25

    def stroke_curve_snap(parent):
        paint_settings = UnifiedPaintPanel.paint_settings(parent.context)
        if paint_settings:
            brush = paint_settings.brush
            if brush and hasattr(brush, "stroke_method") and brush.stroke_method == 'CURVE':
                snap_items = ToolSettings.bl_rna.properties["snap_elements"].enum_items
                tool_settings = parent.context.tool_settings
                snap_elements = tool_settings.snap_elements
                if len(snap_elements) == 1:
                    text = ""
                    for elem in snap_elements:
                        icon = snap_items[elem].icon
                        break
                else:
                    text = "Mix"
                    icon = 'NONE'
                del snap_items, snap_elements

                row = parent.layout.row(align=True)
                row.prop(tool_settings, "use_snap", text="")

                sub = row.row(align=True)
                sub.popover(
                    panel="VIEW3D_PT_snapping",
                    icon=icon,
                    text=text,
                )
                return 2.6
        return -1 # Invalid