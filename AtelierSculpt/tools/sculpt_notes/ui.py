from bpy.types import Panel


class BAS_PT_sculpt_notes(Panel):
    bl_label = "Sculpt Notes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = ".paint_common"
    bl_category = 'Sculpt'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'SCULPT'

    def draw_curve_SN(self, context, layout, curve, name, drawMasterBox):
        if drawMasterBox:
            curveProps = layout.box()
            curveProps.label(text=name)
            curveProps = curveProps.box()
        else:
            layout.label(text=name)
            curveProps = layout.box()
        curveProps.use_property_split = True

        _col = curveProps.column()

        if curve.bevel_object is None:
            
            #col.prop(curve, "offset")
            sub = _col.column()
            #sub.active = (curve.bevel_object is None)
            sub.prop(curve, "extrude")

            #col.prop(curve, "taper_object", text="Taper Curve")

            #col = curveProps.column()
            #sub = col.column()
            #sub.active = (curve.bevel_object is None)
            sub.prop(curve, "bevel_depth", text="Depth")
            sub.prop(curve, "bevel_resolution", text="Resolution")

        else:
            bevelObj = curve.bevel_object
            _col.prop(bevelObj, "scale", text="Scale    ")

        _col.prop(curve, "bevel_object", text="Bevel Curve")

        sub = _col.column()
        sub.active = curve.bevel_object is not None
        sub.prop(curve, "use_fill_caps")

        _col = curveProps.column()
        _col.active = (
            (curve.bevel_depth > 0.0) or
            (curve.extrude > 0.0) or
            (curve.bevel_object is not None)
        )
        sub = _col.column(align=True)
        sub.prop(curve, "bevel_factor_start", text="Bevel Start")
        sub.prop(curve, "bevel_factor_end", text="End")

    def draw(self, context):
        SN = context.window_manager.bas_sculptnotes
        tool_settings = context.tool_settings
        view = context.space_data
        overlay = view.overlay
        layout = self.layout
        layout.scale_y = 1.1
        col = layout.column().box()
        row = col.row()
        row.scale_y = 1.2

    #   SYSTEM SELECTION
        #row.prop( SN, 'use', text="Annotations", expand=True) # GREASEPENCIL
    #   ANNOTATION OPTIONS
        #if   SN.use == 'NOTES':
        _row = col.row()
        _row = _row.grid_flow(row_major=True, columns=3, align=False)
        if overlay.show_annotation:
            icon_show_annot = 'HIDE_OFF'
        else:
            icon_show_annot = 'HIDE_ON'
        _row.scale_x = 1.2
        _row.prop(overlay, "show_annotation", text="", icon=icon_show_annot)
        placement = _row.row(align=True)
        placement.scale_x = 1.2
        placement.prop(tool_settings, "annotation_stroke_placement_view3d", text="", expand=True)
        _row = _row.row(align=True)
        _row.operator("bas.undo_note", text="", icon='LOOP_BACK')
        _row.operator("bas.clear_note", text="Clear Notes", icon='PANEL_CLOSE')
        if not   SN.isCreated:
            col.row().prop( SN, 'autoClear')
    #   GREASE PENCIL
        #else:
        #    col.label(text="Work In Progress !")
        #    return

        if not SN.isCreated:
        #   AJUSTES GENERALES DE CONVERSION
            col = layout.column().box()
            col.prop( SN, 'mergeDistThreshold', slider=True)
            col = layout.column().box()
        #   METHOD + OPTIONS ####################
            row = col.row()
            row.grid_flow(columns=3, align=True).prop( SN, "method_type", expand=True)
        #   JOIN STROKES
            if  SN.canJoinStrokes:
                row = col.row()
                row.prop( SN, 'joinStrokes')
        #   MERGE STROKES
            if  SN.canMergeStrokes:
                row = col.row()
                row.prop( SN, 'mergeStrokes', text="Merge strokes into one")
        #   REPROJECT
            _row = col.row(align=True)
            if  SN.canReproject:
                _col = _row.column()
                _col.enabled = not   SN.ngon
                _col.prop( SN, 'reproject', text="Re-project?")
        #   NGONS
            if  SN.canNgon:
                _col = _row.column()
                _col.prop( SN, 'ngon', text="N-gon?")   

        #   FILTER OF OPTIONS
        method =  SN.method
        if method == 1:
            usingCurves = False
            col.prop( SN, 'thickness', text="Thickness", slider=True)
        elif method == 2:
            usingCurves = False
            pass
        elif method == 3 or method == 4:
            usingCurves = True
            '''
            if not   SN.isCreated:
                if   SN.curve_useCurveMapForSplinePointsRadius:
                    if  SN.method == 3:
                        _row = col.row()
                        _row.prop( SN, 'radiusMultiplier', text="Radius Multiplier", slider=True)
                else:
                    _row = col.row()
                    _row.prop( SN, 'radius', text="Radius", slider=True)
            '''
        elif method == 5:
            usingCurves = True
            box = col.box()
            box.label(text="Follow-Path Object :")
            _row = box.row()
            #_row.use_property_split = True
            _row.prop( SN, 'path_object', text="Object")
            _row = box.split(align=True, factor=0.48)
            _row.prop( SN, 'path_object_makeCopy', text="Make a Copy")
            _row.prop( SN, 'path_object_pivotToCenter', text="Pivot to Center")
        elif method == 6:
            usingCurves = False
            box = col.box()
            box.label(text="Strip Settings :")
            _row = box.column()
            #_row.prop( SN, 'strips_thicknessForSize', text="Note Thickness for Quad Size?")
            _row.prop( SN, 'strips_makeSolid')
            _row = _row.row()
            _row.enabled =   SN.strips_makeSolid
            _row.prop( SN, 'strips_makeBevel')
        else:
            usingCurves = False
            pass
        
        if usingCurves:
            _row = col.row()
            _row.alert=True
            _row.prop( SN, "curve_postEdit", text="Post Edition")
            _row.alert=False
            # CURVE PROPERTIES
            if SN.isCreated:
                from bpy import data as D

                if method == 5: # PATH
                    objPath =   SN.path_object
                    pathProps = layout.box()
                    pathProps.label(text="Path Properties :")
                    pathProps = pathProps.box()
                    _col = pathProps.column()

                    # _col.prop( SN, "path_object", text="Path Object")
                    array = objPath.modifiers["_Array"]
                    #offset = array.constant_offset_displace[0]
                    _col.prop(array, "constant_offset_displace", text="Offset")
                    _row = _col.row(align=True)
                    _row.prop(array, "use_merge_vertices", text="Merge")
                    _row.prop(array, "merge_threshold", text="Distance")
                    _col.prop(array, "start_cap")
                    _col.prop(array, "end_cap")

                    if objPath.type == 'CURVE':
                        objPathCurve = D.curves[objPath.name]
                        self.draw_curve_SN(context, pathProps, objPathCurve, "Sub-Curve Properties :", False)


                curve = D.curves[SN.curve.name]
                self.draw_curve_SN(context, layout, curve, "Curve Properties :", True)

                if curve.bevel_object != None and method != 5:
                    pivotProps = layout.box()
                    pivotProps.label(text="Curve-Shape Pivot :")
                    pivotProps = pivotProps.box()
                    _col = pivotProps.column()
                    _col.prop( SN, 'curveShape_pivot_mode', text="Mode")
                    if   SN.curveShape_pivot_mode == 'NODE':
                        _col.prop( SN, 'curveShape_pivot_index', text="Index")
                
                
            else:
                col.prop( SN, 'curve_useCurveMapForSplinePointsRadius')
                _row = col.row(align=True)
                _row.prop( SN, 'curve_isCyclic', text="Is Cyclic?")
                _row.prop( SN, 'curve_simplify', text="Simplify Curve")

                #if method == 5:
                    

                
            #   CURVE MAP EDITOR
                
                if   SN.curve_curveMap_isCreated:
                    boxCol = col.column(align=True)
                    curveBox = boxCol.box()
                    curveBox.emboss = 'NONE'
                    arrowIcon = 'DOWNARROW_HLT' if  SN.showCurveMapEditor else 'RIGHTARROW'
                    curveBox.row().prop( SN, 'showCurveMapEditor', icon=arrowIcon)
                    curveBox.scale_y = 0.7
                    if  SN.showCurveMapEditor:
                        from bpy import data as D
                        curveBox = boxCol.box()
                        try:
                            curveBox.enabled =   SN.curve_useCurveMapForSplinePointsRadius
                            #curveBox.template_curve_mapping(CurveData('CurveData'), "mapping", type='NONE') # types: vector (tiene 3 curvas/canales: para x,y,z) # none (normal, 1 curva/canal solamente), COLOR (tiene 4 canales/curvas)
                            node = D.node_groups['NodeGroup'].nodes['CurveData']   
                            curveBox.template_curve_mapping(node, "mapping", type='NONE')
                        except:
                            curveBox.operator("bas.sculpt_notes_create_curve_map", text="Create Curve Map")
                            curveBox.label(text="An error has been ocurred. Please report it", icon='ERROR')
                            pass
                        curveBox.separator(factor=0.1)
                
        if not usingCurves or   SN.isCreated:
            '''
            # MIRROR
            if  SN.canMirror:
                _row = col.row(align=True) # col to row
                _row = _row.split(factor=0.5, align=True)
                _row.prop( SN, 'mirror', icon='MOD_MIRROR')
                _row = _row.grid_flow(columns=4, align=True)
                _row.prop( SN, "decimation_symmetry_axis", expand=True)
            # SMOOTH
            if  SN.canSmooth: 
                _row = col.row(align=True)
                _row.prop( SN, 'smooth', icon='SMOOTHCURVE')
                if   SN.smooth:
                    _row.prop( SN, 'smoothPasses')
            '''
            # REMESH
            if  SN.canRemesh:
                _row = col.row(align=True)
                _row.prop( SN, 'remeshIt', icon='OUTLINER_OB_META')
                if   SN.remeshIt:
                    mesh = context.active_object.data
                    _row.prop(mesh, "remesh_voxel_size")

    #   OPCIONES PARA CONVERTIR / DIRECTA / APLICAR / BORRAR / CANCELAR
        col = layout.column()
        _col = layout.column_flow()
        _col.scale_y = 1.3
        if SN.method_type in {'WRAP', 'PATH'}:
            _col.alert = True
            _col.label(text="May not be working in this version")
        __row = _col.row()
        _row = __row.split(factor=0.3, align=True)
        if not SN.live:
            if SN.applyModifiersDirectly and not SN.isCreated:
                if usingCurves:
                    __row.operator("bas.sculpt_notes_convert_to_curve", text="> Convert To Curve <")
                elif method == 6:
                    __row.operator("bas.sculpt_notes_convert_to_strip", text="> Convert To Strip <")
                else:
                    if SN.joinStrokes or SN.mergeStrokes:
                        col.prop( SN, 'applyModifiersDirectly')
                        __row.operator("bas.sculpt_notes_convert_to_3d", text="> Convert To Mesh <")
                    #_row.prop( SN, 'live', text="LIVE", icon='REC')
                    else:
                        __row.operator("bas.sculpt_notes_convert_to_3d", text="> Convert To Mesh <")
            else:
                _row = __row
                if SN.isCreated:
                    if usingCurves:
                        _row.operator("bas.sculpt_notes_cancel", text="Apply")
                        _row.operator("bas.sculpt_notes_curve_to_mesh", text="To Mesh")
                        _row.operator("bas.sculpt_notes_remove_curve", text="Remove")
                    else:
                        _row.operator("bas.sculpt_notes_apply_modifiers", text="Apply")
                        _row.operator("bas.sculpt_notes_cancel", text="Cancel")
                        _row.operator("bas.sculpt_notes_remove_mesh", text="Remove")
                else:
                    if usingCurves:
                        __row.operator("bas.sculpt_notes_convert_to_curve", text="> Convert To Curve <")
                    elif method == 6:
                        __row.operator("bas.sculpt_notes_convert_to_strip", text="> Convert To Strip <")
                    else:
                        if SN.joinStrokes:
                            col.prop( SN, 'applyModifiersDirectly')
                        _row.operator("bas.sculpt_notes_convert_to_3d", text="> Convert To Mesh <")
                    
        else:
            _row = __row
            _row.alert=True
            _row.prop( SN, 'live', text="LIVE", icon='REC')
            row = _row.row()
            row.label(text="Coming Soon!")