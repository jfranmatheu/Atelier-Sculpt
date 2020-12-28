from bpy.types import Panel


def draw_mesh_extractor(layout, context):
    row = layout.row(align=True)
    row.ui_units_x = 6.2 # 5.8
    if not context.window_manager.bas_extractor.created:
        props = context.window_manager.bas_extractor
        if props.mode == 'BLENDER':
            mesh = context.active_object.data
            _props = row.operator("mesh.paint_mask_extract", text="Mask Extract", icon='CLIPUV_HLT')
        else:
            _props = row.operator("bas.mask_extractor_quick", text="Mask Extractor", icon='CLIPUV_HLT')
            _props.thickness = props.thickness
            _props.offset = props.offset
            _props.smoothPasses = props.smooth_passes
            _props.mode = props.mode
            _props.superSmooth = props.super_smooth
            _props.keepMask = props.keep_mask
            _props.editNewMesh = props.edit_new_mesh
            _props.postEdition = props.post_edition
        row.popover(panel="BAS_PT_Mask_Extractor_Options", text="")
    else:
        row.popover(panel="BAS_PT_Mask_Extractor_Options", text="Mask Extractor", icon='MODIFIER_ON')
        #row.operator("bas.mask_extractor_quick", text="Mask Extractor", icon='CLIPUV_HLT')

class BAS_PT_Mask_Extractor_Options(Panel):
    bl_label = "Options"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "NONE"
    bl_category = 'Sculpt'
    bl_description = "Mask Extractor options"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        props = context.window_manager.bas_extractor
        layout = self.layout
        row = layout.row()
        if not props.is_created:
            row.prop(props, 'mode', expand=True, text="Solid")
            _row = layout.column()
            if props.mode == 'BLENDER':
                mesh = context.active_object.data
                props = _row.operator("mesh.paint_mask_extract", text="Mask Extract")
                return

            elif props.mode == 'FLAT':
                _row.active = False
            else:
                _row.active = True
            row = _row.row()
            row.prop(props, 'thickness', slider=True)
            row = _row.row()
            row.prop(props, 'super_smooth', slider=True)
            row = _row.row()
            row.prop(props, 'smooth_passes')
            row = _row.row()
            row.prop(props, 'edit_new_mesh', text="Sculpt new mesh when extracted")
            row = _row.row()
            row.prop(props, 'keep_mask', text="Keep original mask")
            row = _row.row()
            row.prop(props, "post_edition", text="Post-Edition")
            row = _row.row()
            row.scale_y = 1.5
            _props = row.operator("bas.mask_extractor_quick", text="Extract Mask !")
            _props.thickness = props.thickness
            _props.offset = props.offset
            _props.smoothPasses = props.smooth_passes
            _props.mode = props.mode
            _props.superSmooth = props.super_smooth
            _props.keepMask = props.keep_mask
            _props.editNewMesh = props.edit_new_mesh
            _props.postEdition = props.post_edition
        else:
            if props.post_edition:
                col = layout.column()
                col.scale_y = 1.1
                if props.extracted:
                    obj = props.extracted
                    row = col.row()
                    solid = obj.modifiers["Solid"]
                    row.prop(solid, "thickness", text="Thickness")
                    row = col.row()
                    if props.mode == 'SOLID':
                        smooth = obj.modifiers["Smooth"]
                        row.prop(smooth, "iterations", text="Smooth Passes")
                    if props.super_smooth:
                        row = col.row()
                        superSmooth = obj.modifiers["Co_Smooth"]
                        row.prop(superSmooth, "iterations", text="Super Smooth Passes")
                row = col.row()
                row.alert = True
                row.scale_y = 1.3
                row.operator("bas.mask_extractor_apply", text="> APPLY CHANGES <")
