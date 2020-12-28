from ... import __package__ as main_package
from bpy.types import Panel


# --------------------------------------------- #
# REMESH OPTIONS
# --------------------------------------------- #
class BAS_PT_remesh_options(Panel):
    bl_label = "Remesh Options"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "NONE"
    bl_category = 'Sculpt'
    bl_description = "Remesh options for each remesh method"
    bl_options = {'DEFAULT_CLOSED'}
    bl_ui_units_x = 11

    def draw(self, context):
        t_props = context.window_manager.bas_remesh
        prefs = context.preferences.addons[main_package].preferences
        layout = self.layout
        row = layout.row()
        col = row.column()

    #   QUADRIFLOW
        if t_props.remesher == 'QUADRIFLOW':
            col.operator('object.quadriflow_remesh', icon='PLAY', text="Quadriflow Remesh")

        #   DECIMATION
        elif t_props.remesher == 'DECIMATE':
            col.prop(t_props, 'decimate_ratio')
            col.prop(t_props, 'decimate_triangulate')
            row = col.row(align=True)
            row.prop(t_props, 'decimate_symmetry')
            row.prop(t_props, 'decimate_symmetry_axis')

            col.separator()
            col = layout.column()
            col.scale_y = 2
            col.operator('bas.decimate_remesh', text="Remesh")

        #   DYNTOPO REMESH
        elif t_props.remesher == 'DYNTOPO':
            _col = col.row()
            if t_props.dyntopo_resolution > 150:
                _col.alert=True
                icon = 'ERROR'
            else:
                _col.alert=False
                icon = 'MONKEY'
            _col.label(icon=icon, text="")
            _col.prop(t_props, 'dyntopo_resolution')
            row = col.row()
            row.alert=False
            row.prop(t_props, 'dyntopo_symmetry')
            _row = row.split()
            _row.ui_units_x = 7
            _row.prop(t_props, 'dyntopo_symmetry_axis', text="Axis")

            col.separator()
            col = layout.column()
            col.scale_y = 2
            col.operator('bas.dyntopo_remesh', text="Remesh")

        #   VOXELS
        elif t_props.remesher == 'VOXEL':
            col.use_property_split = True
            col.use_property_decorate = False
            mesh = context.active_object.data
            __col = col.row()
            __col.prop(mesh, "remesh_voxel_size")
            __col.scale_y = 1.2
            __col.scale_x = 2
            _row = col.row(align=True)
            if t_props.voxels_incremental_sign:
                iconSign = 'ADD'
                _row.alert = False
            else:
                iconSign = 'REMOVE'
                _row.alert = True
            _row.prop(t_props, "voxels_incremental_sign", icon=iconSign, text="")
            _row = _row.split().row(align=True)
            _row.alert = False
            sign = 1 if t_props.voxels_incremental_sign else -1
            prop = _row.operator("bas.voxel_size_increment", text=".05")
            prop.value = 0.05 * sign
            prop = _row.operator("bas.voxel_size_increment", text=".01")
            prop.value = 0.01 * sign
            prop = _row.operator("bas.voxel_size_increment", text=".005")
            prop.value = 0.005 * sign
            prop = _row.operator("bas.voxel_size_increment", text=".001")
            prop.value = 0.001 * sign

            col.separator()
            row = layout.row(align=True)
            row.split().prop(t_props, "voxel_edit_size_presets", text="", icon='OUTLINER_DATA_GP_LAYER')
            if t_props.voxel_edit_size_presets:
                layout.grid_flow(row_major=True, columns=1, even_columns=True).prop(prefs, "voxel_size_presets", text="")
            else:
                presets = prefs.voxel_size_presets
                for valor in presets: # Creamos boton por valor
                    row.operator('bas.voxel_size_change', text=str(round(valor, 5))[1:6]).value = valor # AQUI LLAMAMOS A NUESTRO OPERADOR

            col.separator()
            col.prop(mesh, "remesh_voxel_adaptivity")
            col.prop(mesh, "use_remesh_fix_poles")
            col.prop(mesh, "use_remesh_smooth_normals")
            col.prop(mesh, "use_remesh_preserve_volume")
            col.prop(mesh, "use_remesh_preserve_paint_mask")
            col.prop(mesh, "use_remesh_preserve_sculpt_face_sets")

            col.separator()
            col.prop(t_props, "voxel_join_object")
            col.separator()
            _row = col.box()
            row = _row.column().row(align=True)
            row.alignment = 'LEFT'
            row.active = True if t_props.voxel_join_object == None else False
            row.prop(t_props, 'voxel_reprojection')

            col.separator()
            col = layout.column()
            col.scale_y = 2
            if t_props.voxel_join_object != None:
                col.operator('bas.voxel_remesh_join', text="Remesh (Join)")
            elif t_props.voxel_reprojection != 'NONE':
                col.operator('bas.voxel_remesh_reproject', text="Remesh (Reproject)")
            elif context.sculpt_object.use_dynamic_topology_sculpting:
                col.operator('bas.voxel_remesh', text="Remesh (Dyn)")
            else:
                col.operator('object.voxel_remesh', text="Remesh")
