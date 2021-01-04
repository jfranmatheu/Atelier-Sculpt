from bpy.types import Panel


def draw_mesh_extractor(layout, context):
    row = layout.row(align=True)
    row.ui_units_x = 6.2 # 5.8
    if not context.window_manager.bas_extractor.created:
        extractor = context.window_manager.bas_extractor
        if extractor.mode == 'BLENDER':
            mesh = context.active_object.data
            _props = row.operator("mesh.paint_mask_extract", text="Mask Extract", icon='CLIPUV_HLT')
        else:
            _props = row.operator("bas.mask_extractor_quick", text="Mask Extractor", icon='CLIPUV_HLT')
            _props.thickness = extractor.thickness
            _props.offset = extractor.offset
            _props.smoothPasses = extractor.smooth_passes
            _props.mode = extractor.mode
            _props.superSmooth = extractor.super_smooth
            _props.keepMask = extractor.keep_mask
            _props.editNewMesh = extractor.edit_new_mesh
            _props.postEdition = extractor.post_edition
            _props.smooth_borders = extractor.smooth_borders
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
    
    def draw_properties(self, layout, extractor):
        # Modifier Properties.
        col = layout.column(align=True)
        
        header = col.box()
        header.label(text="Extract Properties:", icon='PROPERTIES')
        
        content = col.box()
        
        content.prop(extractor, 'thickness', slider=True)
        content.prop(extractor, 'super_smooth', slider=True)
        content.prop(extractor, 'smooth_passes')
        if extractor.mode == 'SINGLE' and self.superSmooth:
            content.prop(extractor, 'smooth_borders')
        
        #_col.separator()
        
        # Settings for after-extracting.
        col = layout.column(align=True)
        
        header = col.box()
        header.label(text="After Extract Settings:", icon='SETTINGS')
        
        content = col.box()
        
        content.prop(extractor, 'edit_new_mesh', text="Sculpt new mesh when extracted")
        content.prop(extractor, 'keep_mask', text="Keep original mask")
        content.prop(extractor, "post_edition", text="Post-Edition")
        
        #_col.separator()
    
    def draw(self, context):
        extractor = context.window_manager.bas_extractor
        layout = self.layout
        if not extractor.is_created:
            layout.prop(extractor, 'mode', expand=True, text="Solid")
            layout.scale_y = 1.3
            if extractor.mode == 'BLENDER':
                mesh = context.active_object.data
                extractor = layout.operator("mesh.paint_mask_extract", text="Mask Extract")
                return
            elif extractor.mode != 'FLAT':
                self.draw_properties(layout, extractor)
            
            _props = layout.operator("bas.mask_extractor_quick", text="Extract Mask !")
            _props.thickness = extractor.thickness
            _props.offset = extractor.offset
            _props.smoothPasses = extractor.smooth_passes
            _props.mode = extractor.mode
            _props.superSmooth = extractor.super_smooth
            _props.keepMask = extractor.keep_mask
            _props.editNewMesh = extractor.edit_new_mesh
            _props.postEdition = extractor.post_edition
            _props.smooth_borders = extractor.smooth_borders
            
        else:
            if extractor.post_edition:
                col = layout.column()
                col.scale_y = 1.1
                if extractor.extracted:
                    obj = extractor.extracted
                    row = col.row()
                    solid = obj.modifiers["Solid"]
                    row.prop(solid, "thickness", text="Thickness")
                    row = col.row()
                    if extractor.mode == 'SOLID':
                        smooth = obj.modifiers["Smooth"]
                        row.prop(smooth, "iterations", text="Smooth Passes")
                    if extractor.super_smooth:
                        row = col.row()
                        superSmooth = obj.modifiers["Co_Smooth"]
                        row.prop(superSmooth, "iterations", text="Super Smooth Passes")
                row = col.row()
                row.alert = True
                row.scale_y = 1.3
                row.operator("bas.mask_extractor_apply_changes", text="> APPLY CHANGES <")
