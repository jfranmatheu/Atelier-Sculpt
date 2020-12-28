class BAS_HT_header_blocks():
    def draw_shading(self, context):
        view = context.space_data
        shading = view.shading
        overlay = view.overlay
        layout = self.layout

        # Viewport Settings
        layout.popover(
            panel="VIEW3D_PT_object_type_visibility",
            icon_value=view.icon_from_show_object_viewport,
            text="",
        )

        # Gizmo toggle & popover.
        row = layout.row(align=True)
        # FIXME: place-holder icon.
        row.prop(view, "show_gizmo", text="", toggle=True, icon='GIZMO')
        sub = row.row(align=True)
        sub.active = view.show_gizmo
        sub.popover(
            panel="VIEW3D_PT_gizmo_display",
            text="",
        )

        # Overlay toggle & popover.
        row = layout.row(align=True)
        row.prop(overlay, "show_overlays", icon='OVERLAY', text="")
        sub = row.row(align=True)
        sub.active = overlay.show_overlays
        sub.popover(panel="VIEW3D_PT_overlay", text="")

        row = layout.row()
        #row.active = (object_mode == 'EDIT') or (shading.type in {'WIREFRAME', 'SOLID'})

        if shading.type == 'WIREFRAME':
            row.prop(shading, "show_xray_wireframe", text="", icon='XRAY')
        else:
            row.prop(shading, "show_xray", text="", icon='XRAY')

        row = layout.row(align=True)
        row.prop(shading, "type", text="", expand=True)
        sub = row.row(align=True)
        # TODO, currently render shading type ignores mesh two-side, until it's supported
        # show the shading popover which shows double-sided option.

        # sub.enabled = shading.type != 'RENDERED'
        sub.popover(panel="VIEW3D_PT_shading", text="")
    
    def draw_close_gaps(self, props):
        row = self.layout.row(align=True)
        row.ui_units_x = 5.4
        prop = row.operator("bas.close_gaps", text="Close Gaps", icon='RESTRICT_INSTANCED_ON')
        prop.use = props.use
        prop.smooth_passes = props.smooth_passes
        prop.keep_dyntopo = props.keep_dyntopo
        row.popover (
            panel="BAS_PT_Close_Gaps_Options",
            text=""
        )
