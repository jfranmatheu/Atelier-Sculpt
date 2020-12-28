from bpy.types import Panel


class BAS_PT_mirror_plane_options(Panel):
    bl_label = "Mirror Plane Options"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "NONE"
    bl_category = 'Sculpt'
    bl_options = {'DEFAULT_CLOSED'}
    bl_ui_units_x = 16

    def draw(self, context):
        mirror = context.scene.bas_mirrorplane
        layout = self.layout
        split = layout.split()

        col = split.box().column(align=True)
        col.box().label(text="Mirror Plane Settings")
        col.separator(factor=2)
        col.scale_y = 1.1

        row = col.row(align=True)
        row.prop(mirror, "offset")

        col.separator()
        
        col.prop(mirror, "color")

        col.separator()

        if mirror.created:
            col.operator("bas.mirror_plane_delete", text="Delete Mirror Plane")
        else:
            col.prop(mirror, "use_world_origin")
            col.separator()
            row = col.row(align=True)
            row.scale_y = 1.2
            _props = row.operator("bas.mirror_plane", text="Create Mirror Plane")
            _props.useWorldOrigin = mirror.use_world_origin


        col = split.box().column()

        sculpt = context.tool_settings.sculpt

        #col.alignment = 'RIGHT'
        col.label(text="Lock")

        #col = split.column()

        row = col.row(align=True)
        row.prop(sculpt, "lock_x", text="X", toggle=True)
        row.prop(sculpt, "lock_y", text="Y", toggle=True)
        row.prop(sculpt, "lock_z", text="Z", toggle=True)

        #split = layout.split()

        #col = split.column()
        #col.alignment = 'RIGHT'
        col.label(text="Tiling")

        #col = split.column()

        row = col.row(align=True)
        row.prop(sculpt, "tile_x", text="X", toggle=True)
        row.prop(sculpt, "tile_y", text="Y", toggle=True)
        row.prop(sculpt, "tile_z", text="Z", toggle=True)

        #layout.use_property_split = True
        #layout.use_property_decorate = False
        row = col.row(align=True)
        row.prop(sculpt, "use_symmetry_feather", text="Feather")
        row = col.row(align=True)
        row.column().prop(sculpt, "radial_symmetry", text="Radial")
        row.column().prop(sculpt, "tile_offset", text="Tile Offset")
