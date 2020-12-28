from ..blocks.header import BAS_HT_header_blocks
from bl_ui.space_view3d import VIEW3D_HT_header as Header
from ... icons import Icon
from bpy.types import Object


# --------------------------------------------- #
# HEADER UI
# --------------------------------------------- #
class BAS_HT_header(Header): # Header -> VIEW3D_HT_header
    bl_idname = "BAS_HT_header"
    bl_label = ""
    bl_space_type = "VIEW_3D"
    bl_region_type = "HEADER"
    #bl_context = ".paint_common"

    transformTools = {
        "builtin.move",
        "builtin.rotate",
        "builtin.scale",
        "builtin.transform",
        "builtin.box_hide" # exclude for mask tools
    }

    def draw(self, context):
        if context.mode == "SCULPT":
            layout = self.layout
            props_ui = context.scene.bas_custom_ui
            header = BAS_HT_header_blocks

            obj = context.active_object
            object_mode = 'OBJECT' if obj is None else obj.mode
            act_mode_item = Object.bl_rna.properties["mode"].enum_items[object_mode]
            #act_mode_i18n_context = bpy.types.Object.bl_rna.properties["mode"].translation_context
            sub = layout.row(align=True)
            sub.ui_units_x = 2
            sub.operator_menu_enum(
                "object.mode_set", "mode",
                text="", # bpy.app.translations.pgettext_iface(act_mode_item.name, act_mode_i18n_context),
                icon=act_mode_item.icon,
            )

            brush = context.tool_settings.sculpt.brush

            if (context.workspace.tools.from_space_view3d_mode("SCULPT", create=False).idname in self.transformTools):
                self.is_brush = False
            else:
                self.is_brush = True
                if brush.sculpt_tool == 'MASK' or brush.sculpt_tool == 'BOX_MASK': # context.workspace.tools.from_space_view3d_mode("SCULPT", create=False).idname == "builtin.box_mask":
                    row = layout.row(align=True)
                    row.operator("bas.mask_by_cavity", text='Cavity', icon_value=Icon.MASK_CAVITY())
                    row.popover(panel="BAS_PT_Mask_By_Cavity", text="")

                    row = layout.row(align=True)
                    props = row.operator("sculpt.mask_filter", text='Smooth', icon_value=Icon.MASK_SMOOTH())
                    props.filter_type = 'SMOOTH'
                    props.auto_iteration_count = True

                    props = row.operator("sculpt.mask_filter", text='Sharp', icon_value=Icon.MASK_SHARP()) # Sharper
                    props.filter_type = 'SHARPEN'
                    props.auto_iteration_count = True

                    row = layout.row(align=True)
                    row.label(text="Expand")
                    props = row.operator("sculpt.mask_filter", text='', icon='ADD') # Grow
                    props.filter_type = 'GROW'
                    props.auto_iteration_count = True

                    props = row.operator("sculpt.mask_filter", text='', icon='REMOVE') # Shrink
                    props.filter_type = 'SHRINK'
                    props.auto_iteration_count = True

                    row = layout.row(align=True)
                    row.label(text="Contrast")
                    props = row.operator("sculpt.mask_filter", text='', icon='ADD') # Contrast
                    props.filter_type = 'CONTRAST_INCREASE'
                    props.auto_iteration_count = False

                    props = row.operator("sculpt.mask_filter", text='', icon='REMOVE') # Decrease Contrast
                    props.filter_type = 'CONTRAST_DECREASE'
                    props.auto_iteration_count = False

                    layout.separator()

            layout.separator_spacer()

        #   REMESHERS
            #if props_ui.show_mesh_tools:
            col = layout.column()
            row = col.row(align=True)
            row.ui_units_x = 6.8
            #row.label(text="Remesher :")
            remesher = context.window_manager.bas_remesh
            row.popover(
                panel="BAS_PT_remesh_options",
                icon='MODIFIER_ON', # EXPERIMENTAL
                text=""
            )
            row.prop(remesher, 'remesher', text="", toggle=True, expand=False)

        #   QUADRIFLOW
            if remesher.remesher == 'QUADRIFLOW':
                remesh = row.operator('object.quadriflow_remesh', icon='PLAY', text="")

        #   DECIMATION
            elif remesher.remesher == 'DECIMATE':
                remesh = row.operator('bas.decimate_remesh', icon='PLAY', text="")
                remesh.ratio = remesher.decimate_ratio
                remesh.triangulate = remesher.decimate_triangulate
                remesh.symmetry = remesher.decimate_symmetry
                remesh.symmetry_axis = remesher.decimate_symmetry_axis

        #   DYNTOPO'S FLOOD FILL
            elif remesher.remesher == 'DYNTOPO':
                remesh = row.operator('bas.dyntopo_remesh', icon='PLAY', text="")
                remesh.resolution = remesher.dyntopo_resolution
                remesh.force_symmetry = remesher.dyntopo_symmetry
                remesh.symmetry_axis = remesher.dyntopo_symmetry_axis
                remesh.only_masked = remesher.dyntopo_only_masked

        #   OPEN VDB - VOXEL
            elif remesher.remesher == 'VOXEL':
                row.ui_units_x = 5.4
                if remesher.voxel_join_object != None:
                    row.operator('bas.voxel_remesh_join', icon='PLAY', text="")
                elif remesher.voxel_reprojection != 'NONE':
                    row.operator('bas.voxel_remesh_reproject', icon='PLAY', text="")
                elif context.sculpt_object.use_dynamic_topology_sculpting:
                    row.operator('bas.voxel_remesh', icon='PLAY', text="")
                else:
                    row.operator('object.voxel_remesh', icon='PLAY', text="")

            #   SEPARATOR
            row = layout.row()
            row.label(text="", icon_value=Icon.SEPARATOR())

        #   MESH TOOLS
            if props_ui.show_mesh_tools:
                text = ""
            else:
                text = "Tools"
            row = layout.row()
            row.prop(props_ui, 'show_mesh_tools', icon='COLLAPSEMENU', text=text)
            if props_ui.show_mesh_tools:
            #   QUICK MASK EXTRACTOR
                row = layout.row(align=True)
                row.ui_units_x = 6.2 # 5.8
                extractor = context.window_manager.bas_extractor
                if not extractor.is_created:
                    if extractor.mode == 'BLENDER':
                        mesh = context.active_object.data
                        _props = row.operator("mesh.paint_mask_extract", text="Mask Extract", icon='CLIPUV_HLT')
                    else:
                        _props = row.operator("bas.mask_extractor_quick", text="Mask Extractor", icon='CLIPUV_HLT')
                        _props.thickness    =   extractor.thickness
                        _props.offset       =   extractor.offset
                        _props.smoothPasses =   extractor.smooth_passes
                        _props.mode         =   extractor.mode
                        _props.superSmooth  =   extractor.super_smooth
                        _props.keepMask     =   extractor.keep_mask
                        _props.editNewMesh  =   extractor.edit_new_mesh
                        _props.postEdition  =   extractor.post_edition
                    row.popover(panel="BAS_PT_Mask_Extractor_Options", text="")
                else:
                    row.popover(panel="BAS_PT_Mask_Extractor_Options", text="Mask Extractor", icon='MODIFIER_ON')
                    #row.operator("bas.mask_extractor_quick", text="Mask Extractor", icon='CLIPUV_HLT')

            #   DETACH FROM MASK, MESH DETACHER
                detacher = context.window_manager.bas_detacher
                row = layout.row(align=True)
                row.ui_units_x = 6.3
                _props = row.operator("bas.mask_detacher", text="Mesh Detacher", icon='LIBRARY_DATA_BROKEN') # OUTLINER_OB_META
                _props.detachInDifferentObjects = detacher.detach_multi_objects
                _props.separateLooseParts = detacher.separate_loose_parts
                _props.sculptMaskedMesh = detacher.go_sculpt_masked_mesh
                _props.closeDetachedMeshes = detacher.close_detached_meshes
                _props.closeOnlyMasked = detacher.close_only_masked
                _props.doRemesh = detacher.do_remesh
                row.popover(panel="BAS_PT_Mesh_Detacher_Options", text="")

            #   CLOSE GAPS
                header.draw_close_gaps(self, context.window_manager.bas_closegaps)

            layout.separator_spacer()
            #   QUICK ACCESS TO MODIFIERS
            # layout.column().popover(panel="NSMUI_PT_quick_modifiers", text="", icon='MODIFIER_ON')
            # row = layout.row()
            #row.label(text="Shading")
            header.draw_shading(self, context)

        else:
            Header.draw(self, context)
