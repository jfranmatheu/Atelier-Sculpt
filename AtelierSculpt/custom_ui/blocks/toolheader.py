from ...icons import Icon, get_icon

# NOTE #######################
'''
To add new block that can be added to tool header:

1. Add a function here in BAS_HT_toolheader_blocks with ONLY a 'th' argument.

2. 'th' is for toolheader.py > BAS_HT_toolHeader,
    from 'th' you can access context, brush, custom ui properties, addon preferences, etc.

3. Copy your function name and go to custom_ui_ids_func.py and
    create a new entry with an *identifier* followed by draw.{your_function_name}.

4. Now go to custom_ui_menu_cats.py and creta a new entry in the desired category,
    add the identifier and a name (to be shown in the sub-menu).

5. To add properties to your UI block so you can change how it looks by RMB over it in edit mode:*
    5.1: In ui_data.py > ToolHeader_PG_custom_ui add your properties.
    5.2: Go to custom_ui_ids_ppts.py and create a new entry with the identifier of your block and
        add a dictionary with each property as key and the type of the property as value.
        To add property in preferences instead, write an '_' before the property as well as add the property
        in addon__utils > prefs.py > BAS_Preferences.
    5.3: In your ui block, access to props via th.props and if it's in preferences, via th.prefs.
    * Note: In case you don't want properties, just let an empty dictionary or write None.

6. (Optional) If you want to create new category, add it in custom_ui_menu_cats.py as a list,
    also add the name to the categories tuple a the top of custom_ui_menu_cats.py,
    then go to toolheader_dropdowns.py create new class (see 'DefaultMenu' as example) and add the class
    to the submenus list over the same place.
'''

# GLOBAL VARS
dynStage_Active = 0 # 1 = SKETCH; 2 = DETAIL; 3 = POLISH; 0 = "NONE" # Por defecto ningún 'stage' está activado
dynMethod_Active = "NONE"
dyn_values_ui = [] # valores mostrados en la UI # DEFECTO # Cambiarán al cambiar de stage o detailing (method aquí)

class BAS_HT_toolheader_blocks():
#   SPACING // SPACER
    def separator(th):
        split = th.layout.split()
        col = split.column()
        col.label(text="", icon_value=Icon.SEPARATOR())

        return 1

#   CUSTOM BRUSH ICON
    def render_brush_icon(th):
        row = th.layout.row(align=True)
        row.operator("bas.brush_render_icon", text="", icon='RESTRICT_RENDER_OFF')
        return 1

#   BRUSH SELECTOR
    def brush_selector(th):
        rows_cols = th.prefs.brush_selector_grid_size
        row = th.layout.row(align=True)
        row.ui_units_x = 8
        row.template_ID_preview(th.sculpt, "brush", new="brush.add", rows=rows_cols[0], cols=rows_cols[1], hide_buttons=True)
        return row.ui_units_x

#   BRUSH options COLLAPSED // ADD / RESET // REMOVE
    def brush_options_collapsed(th):
        row = th.layout.row(align=True)
        row.popover(
            panel="BAS_PT_brush_options_dropdown",
            text="")
        return 1

#   BRUSH options // ADD / RESET // REMOVE
    def brush_options(th):
        row = th.layout.row(align=True)
        row.ui_units_x = 1
        if th.props.brush_options_show_add:
            row.operator("brush.add", text="", icon_value=Icon.BRUSH_ADD())
        # RESET BRUSH BUTTON
        if th.props.brush_options_show_reset:
            row.ui_units_x += 1
            row.operator("brush.reset", text="", icon_value=Icon.BRUSH_RESET()) # RESET BRUSH
        # DELETE BRUSH BUTTON
        if th.props.brush_options_show_remove:
            row.ui_units_x += 1
            row.operator("bas.brush_remove", text="", icon_value=Icon.BRUSH_REMOVE()) # DELETE BRUSH
        return row.ui_units_x

#   BRUSH SIZE
    def slider_radius(th):
        row = th.layout.row(align=True)
        row.ui_units_x = 4.5
        # row.prop(ups, "use_unified_size", text="Size") # CHECKBOX PARA MARCAR EL UNIFIED SIZE
        if(th.ups.use_unified_size):
            row.prop(th.ups, "size", slider=True, text="R") # Size
        else:
            row.prop(th.brush, "size", slider=True, text="R") # Size
        row.prop(th.brush, "use_pressure_size", toggle=True, text="")

        return row.ui_units_x

#   BRUSH STRENTH
    def slider_strength(th):
        row = th.layout.row(align=True)
        row.ui_units_x = 4.3
        if(th.ups.use_unified_strength):
            row.prop(th.ups, "strength", slider=True, text="S") # Hardness
        else:
            row.prop(th.brush, "strength", slider=True, text="S") # Hardness
        row.prop(th.brush, "use_pressure_strength", toggle=True, text="")

        return row.ui_units_x

#   BRUSH AUTOSMOOTH SLIDER
    def slider_smooth(th):
        row = th.layout.row(align=True)
        # auto_smooth_factor and use_inverse_smooth_pressure
        row.ui_units_x = 5.8
        if (th.capabilities.has_auto_smooth):
            row.prop(th.brush, "auto_smooth_factor", slider=True, text="Smooth")
            row.prop(th.brush, "use_inverse_smooth_pressure", toggle=True, text="")

        return row.ui_units_x

#   BRUSH > STROKE > SPACING SLIDER
    def slider_spacing(th):
        row = th.layout.row(align=True)
        row.ui_units_x = 6
        # Airbrush
        if th.brush.use_airbrush:
            row.prop(th.brush, "rate", text="Rate", slider=True)
        # Space
        elif th.brush.use_space:
            row.prop(th.brush, "spacing", text="Spacing")
            row.prop(th.brush, "use_pressure_spacing", toggle=True, text="")
        # Line and Curve
        elif th.brush.use_line or th.brush.use_curve:
            row.prop(th.brush, "spacing", text="Spacing")

        return row.ui_units_x

#   SLIDER FOR NORMAL RADIUS AND AREA RADIUS (SCRAPE)
    def slider_normal_radius(th):
        row = th.layout.row(align=True)
        row.ui_units_x = 6.5
        row.prop(th.brush, "normal_radius_factor", slider=True)
        if th.brush.sculpt_tool == 'SCRAPE':
            row.ui_units_x = 10.5
            row.prop(th.brush, "area_radius_factor", slider=True)

        return row.ui_units_x

#   SLIDERS SPECIFICALLY PER EACH BRUSH TYPE
    def slider_others(th):
        sculpt_tool = th.brush.sculpt_tool
        # normal_weight
        if th.capabilities.has_normal_weight:
            row = th.layout.row(align=True)
            ui_units_x = row.ui_units_x = 6.2
            row.prop(th.brush, "normal_weight", slider=True)

        # crease_pinch_factor
        elif th.capabilities.has_pinch_factor:
            row = th.layout.row(align=True)
            ui_units_x = row.ui_units_x = 6
            row.prop(th.brush, "crease_pinch_factor", slider=True, text="Pinch")

        # rake_factor
        elif th.capabilities.has_rake_factor:
            row = th.layout.row(align=True)
            ui_units_x = row.ui_units_x = 6
            row.prop(th.brush, "rake_factor", slider=True)

        elif sculpt_tool == 'MASK':
            row = th.layout.row(align=True)
            ui_units_x = row.ui_units_x = 6
            row.prop(th.brush, "mask_tool", text="Tool")

        # plane_offset, use_offset_pressure, use_plane_trim, plane_trim
        elif th.capabilities.has_plane_offset:
            row = th.layout.row(align=True)
            ui_units_x = row.ui_units_x = 6
            row.prop(th.brush, "plane_offset", slider=True, text="Offset")
            row.prop(th.brush, "use_offset_pressure", text="")
            row = th.layout.row()
            # row.ui_units_x = 2.7
            ui_units_x += 3.04
            row.prop(th.brush, "use_plane_trim", text="Trim")
            if th.brush.use_plane_trim:
                row = th.layout.row()
                row.ui_units_x = 4.5
                row = th.layout.row()
                row.prop(th.brush, "plane_trim", slider=True, text="Distance")
                ui_units_x += 7.36

        # height
        elif th.capabilities.has_height:
            row = th.layout.row(align=True)
            ui_units_x = row.ui_units_x = 6
            row.prop(th.brush, "height", slider=True, text="Height")
        else:
            ui_units_x = 0

        '''
        [‘DRAW’, ‘DRAW_SHARP’, ‘CLAY’, ‘CLAY_STRIPS’, ‘CLAY_THUMB’, ‘LAYER’, ‘INFLATE’,
        ‘BLOB’, ‘CREASE’, ‘SMOOTH’, ‘FLATTEN’, ‘FILL’, ‘SCRAPE’, ‘MULTIPLANE_SCRAPE’,
        ‘PINCH’, ‘GRAB’, ‘ELASTIC_DEFORM’, ‘SNAKE_HOOK’, ‘THUMB’, ‘POSE’, ‘NUDGE’,
        ‘ROTATE’, ‘TOPOLOGY’, ‘CLOTH’, ‘SIMPLIFY’, ‘MASK’, ‘DRAW_FACE_SETS’],
        '''

        if sculpt_tool == 'CLAY_STRIPS':
            row = th.layout.row()
            row.ui_units_x = 5.6
            ui_units_x += 5.83
            row.prop(th.brush, "tip_roundness", slider=True, text="Roundnesss")
        elif sculpt_tool == 'LAYER':
            row = th.layout.row(align=True)
            row.ui_units_x = 6.5
            ui_units_x += 6.73
            row.prop(th.brush, "use_persistent", slider=True, text="Persistent")
            row.operator('sculpt.set_persistent_base', text="Set")
        elif sculpt_tool == 'SMOOTH':
            row = th.layout.row()
            row.ui_units_x = 7
            ui_units_x += 8.26
            row.prop(th.brush, "smooth_deform_type", text="Deformation")
        elif sculpt_tool in {'SCRAPE', 'FILL'}:
            row = th.layout.row()
            row.ui_units_x = 6.2
            ui_units_x += 6.48
            row.prop(th.brush, "area_radius_factor", text="Area Radius", slider=True)
        elif sculpt_tool == 'MULTIPLANE_SCRAPE':
            row = th.layout.row()
            row.ui_units_x = 5
            ui_units_x += 5
            row.prop(th.brush, "multiplane_scrape_angle", text="Angle", slider=True)
        elif sculpt_tool == 'GRAB':
            row = th.layout.row()
            ui_units_x += 6.71
            row.prop(th.brush, "use_grab_active_vertex", text="Grab Active Vertex", toggle=False)
        elif sculpt_tool == 'ELASTIC_DEFORM':
            row = th.layout.row(align=True)
            row.ui_units_x = 16
            ui_units_x += 16.26
            row.prop(th.brush, "elastic_deform_type", text="Deformation")
            row.prop(th.brush, "elastic_deform_volume_preservation", text="Volume Preservation", slider=True)
        elif sculpt_tool == 'SNAKE_HOOK':
            row = th.layout.row(align=True)
            row.ui_units_x = 4.2
            ui_units_x += 4.44
            row.prop(th.brush, "rake_factor", text="Rake", slider=True)
        elif sculpt_tool == 'POSE':
            row = th.layout.row(align=True)
            row.ui_units_x = 21
            ui_units_x += 21
            row.prop(th.brush, "pose_origin_type", text="Type")
            row.prop(th.brush, "pose_offset", text="Offset")
            row.prop(th.brush, "pose_smooth_iterations", text="Smooth")
            row.prop(th.brush, "pose_ik_segments", text="IK Segments")
        elif sculpt_tool == 'CLOTH':
            # TODO: change to a dropdown panel. (popover)
            row = th.layout.row(align=True)
            row.ui_units_x = 23
            ui_units_x += 23
            row.prop(th.brush, "cloth_deform_type", text="Deformation")
            row.prop(th.brush, "cloth_force_falloff_type", text="Falloff")
            row.prop(th.brush, "cloth_mass", text="Mass", slider=True)
            row.prop(th.brush, "cloth_damping", text="Damping")
        # print("UI_UNITS_X:", ui_units_x)
        return ui_units_x if ui_units_x != 0 else -1

        # use_persistent, set_persistent_base
        '''
        if capabilities.has_persistence:
            ob = context.sculpt_object
            do_persistent = True

            # not supported yet for this case
            for md in ob.modifiers:
                if md.type == 'MULTIRES':
                    do_persistent = False
                    break

            if do_persistent:
                row = col.row(align=True)
                row.prop(brush, "use_persistent")
                row.operator("sculpt.set_persistent_base")
        '''

#   BRUSH SETTINGS (DROPDOWN)
    def brush_settings(th):
        row = th.layout.row()
        row.ui_units_x = 1.5
        row.popover(
            panel="VIEW3D_PT_tools_brush_settings", # b283 from *_brush to *_brush_settings
            icon_value=Icon.BRUSH(),
            text="")
        #VIEW3D_PT_sculpt_options_unified
        return row.ui_units_x

#   BRUSH SETTINGS (DROPDOWN)
    def brush_settings_advanced(th):
        row = th.layout.row()
        row.ui_units_x = 1.5
        row.popover(
            panel="VIEW3D_PT_tools_brush_settings_advanced", # b283 from *_brush to *_brush_settings
            icon_value=Icon.BRUSH(),
            text="")
        #VIEW3D_PT_sculpt_options_unified
        return row.ui_units_x

#   BRUSH STROKE SETTINGS (DROPDOWN)
    def stroke(th):
        row = th.layout.row()
        row.ui_units_x = 1.5
        row.popover(
            panel="VIEW3D_PT_tools_brush_stroke",
            icon_value=Icon.STROKE(),
            text="")
        return row.ui_units_x

#   BRUSH STROKE METHOD
    def stroke_method(th, only_icons=True):
        row = th.layout.row()
        if only_icons:
            ui_units_x = row.ui_units_x = 1.5
        else:
            ui_units_x = row.ui_units_x = 2.5 + len(th.brush.stroke_method)/4
        row.prop(th.brush, "stroke_method", text="", icon_value=Icon.STROKE())

        return ui_units_x

#   BRUSH FALLOFF SETTINGS/CURVES (DROPDOWN)
    def falloff(th):
        row = th.layout.row()
        row.ui_units_x = 1.5
        row.popover(
            panel="VIEW3D_PT_tools_brush_falloff",
            icon_value=Icon.FALLOFF(),
            text="")

        return row.ui_units_x

#   BRUSH FALLOFF CURVE PRESETS
    def falloff_presets(th):
        props = th.props
        row = th.layout.row(align=True)
        row.ui_units_x = 6

        row.operator("bas.falloff_curve_presets", icon='SMOOTHCURVE', depress=(not props.depress_smooth)).shape = 'SMOOTH'
        row.operator("bas.falloff_curve_presets", icon='SPHERECURVE', depress=(not props.depress_round)).shape = 'SPHERE'
        row.operator("bas.falloff_curve_presets", icon='ROOTCURVE', depress=(not props.depress_root)).shape = 'ROOT'
        row.operator("bas.falloff_curve_presets", icon='SHARPCURVE', depress=(not props.depress_sharp)).shape = 'SHARP'
        row.operator("bas.falloff_curve_presets", icon='LINCURVE', depress=(not props.depress_line)).shape = 'LIN'
        row.operator("bas.falloff_curve_presets", icon='NOCURVE', depress=(not props.depress_max)).shape = 'CONSTANT'

        return row.ui_units_x

    def falloff_presets_collapse(th):
        row = th.layout.row(align=True)
        row.ui_units_x = 1.5
        row.prop(th.brush, "curve_preset", text="")

        return row.ui_units_x

#   FRONT FACES ONLY (TOGGLE)
    def front_faces(th):
        split = th.layout.row()
        #col = split.row()
        split.prop(th.brush, "use_frontface", text="", icon_value=Icon.FRONTFACES())

        return 1

#   AUTOMASK BY TOPOLOGY
    def mask_topology(th):
        split = th.layout.row()
        split.prop(th.brush, "use_automasking_topology", text="", icon_value=Icon.MASK_TOPOLOGY())

        return 1

#   MASK SETTINGS / INVERT / CLEAR
    def mask(th):
        # MASK MENU
        row = th.layout.row(align=True)
        row.ui_units_x = 2
        #row.menu("VIEW3D_MT_hide_mask", text=" Mask ", icon_value=Icon.MASK())
        # MASK -> INVERT
        props = row.operator("paint.mask_flood_fill", text="", icon_value=Icon.MASK_INVERT())
        props.mode = 'INVERT'
        # MASK -> CLEAR
        props = row.operator("paint.mask_flood_fill", text="", icon_value=Icon.MASK_CLEAR())
        props.mode = 'VALUE'
        props.value = 0

        return row.ui_units_x

#   MIRROR TOGGLES
    def mirror(th):
        # MIRRORS X, Y, Z
        _row = th.layout.row(align=True)
        _row.ui_units_x = 3.5
        # Blender <= 2.90
        #_row.prop(th.sculpt, "use_symmetry_x", text="X", toggle=True)
        #_row.prop(th.sculpt, "use_symmetry_y", text="Y", toggle=True)
        #_row.prop(th.sculpt, "use_symmetry_z", text="Z", toggle=True)
        # Blender >= 2.91
        mesh = th.act_obj.data
        _row.prop(mesh, "use_mirror_x", text="X", toggle=True)
        _row.prop(mesh, "use_mirror_y", text="Y", toggle=True)
        _row.prop(mesh, "use_mirror_z", text="Z", toggle=True)
        
        #row = th.layout.row(align=True)
        #row.popover(panel="BAS_PT_mirror_plane_options", text="", icon_value=Icon.MIRROR())
        #if mirror_plane:
        #    _icon = 'HIDE_OFF' if scn.show else 'HIDE_ON'
        #    row.prop(scn, 'show', text="", icon=_icon, toggle=True)

        return _row.ui_units_x
    
#   MIRROR + MIRROR PLANE TOGGLES
    def mirror_plane(th):
        units = BAS_HT_toolheader_blocks.symmetry(th)
        _row = th.layout.row(align=True)
        _row.ui_units_x = 2
        mirror = th.context.scene.bas_mirrorplane
        _row.popover(panel="BAS_PT_mirror_plane_options", text="", icon_value=Icon.MIRROR())
        if mirror.created:
            _row.ui_units_x = 3
            _icon = 'HIDE_OFF' if mirror.show else 'HIDE_ON'
            _row.prop(mirror, 'show', text="", icon=_icon, toggle=True)

        return _row.ui_units_x + units

#   TOPOLOGY SETTINGS / DYNTOPO / MULTIRES
    def dyntopo_multires(th):
        layout = th.layout
        context = th.context
        props = th.props

        mods = context.active_object.modifiers
        # SCULPT --> MULTIRES
        if mods != None:
            for modifier in mods:
            # Si el modificador 'modifier' es de tipo Multires
                if modifier.type == 'MULTIRES':
                    row = layout.row(align=True)
                    row.label(text="", icon="MOD_MULTIRES")
                    row.ui_units_x = 5
                    row.prop(modifier, "sculpt_levels", text="Sculpt")
                    row = layout.row(align=True)
                    row.ui_units_x = 3.6
                    row.operator("object.multires_subdivide", text="Subdivide").modifier = "Multires"
                    row = layout.row(align=True)
                    row.ui_units_x = 3.8
                    row.prop(sculpt, "show_low_resolution", text="Fast Nav", toggle=False)
                    return 13

        sub = layout.row(align=True)
        sub.popover(panel="VIEW3D_PT_sculpt_dyntopo", text="")

        # SCULPT --> DYNAMIC TOPOLOGY
        if(context.sculpt_object.use_dynamic_topology_sculpting):
            dyntopo = context.scene.bas_dyntopo
            dynStage_Active = dyntopo.stage
            useStage = dyntopo.toggle_stages

            # Si hay stage
            if not useStage:
                from ..tools.dyntopo_pro.ui import dyntopoStages
                dynMethod_Active = dyntopo.detailing
                n = int(dynStage_Active) - 1 # CHIVATO PARA EL STAGE

                # LOOK FOR ACTUAL DYN METHOD
                if(dynMethod_Active == "RELATIVE"):
                    dyn_values_ui = dyntopoStages[n].relative_Values
                    icon = Icon.DYNTOPO_RELATIVE()
                elif(dynMethod_Active == "CONSTANT"):
                    dyn_values_ui = dyntopoStages[n].constant_Values
                    icon = Icon.DYNTOPO_CONSTANT()
                elif(dynMethod_Active == "BRUSH"):
                    dyn_values_ui = dyntopoStages[n].brush_Values
                    icon = Icon.DYNTOPO_BRUSH()
                elif(dynMethod_Active == "MANUAL"):
                    dyn_values_ui = dyntopoStages[n].relative_Values
                    icon = Icon.DYNTOPO_MANUAL()

                # PANEL DESPLEGABLE
                sub.popover(panel="BAS_PT_dyntopo_stages", text="", icon_value=icon)
                row = layout.row(align=True)

                # BOTONES PARA OPCIONES/VALORES PARA DETAIL SIZE DE DYNTOPO SEGUN EL METHOD Y STAGE
                detail_icon = [Icon.DYNTOPO_LOW(), Icon.DYNTOPO_MEDIUM(), Icon.DYNTOPO_HIGH()]
                detail_level = context.scene.bas_dyntopo.detail_level
                for i in range(1, 4):
                    op = row.operator("bas.dyntopo_change_value", text="", icon_value=detail_icon[i-1], depress=(i == detail_level))
                    op.value = dyn_values_ui[i-1] # LOW DETAIL
                    op.detail = i
                return 6.83
            # Si no hay ningún 'Stage' activado
            else:
                sub.popover(panel="BAS_PT_dyntopo_stages", text="", icon='STYLUS_PRESSURE') # NUEVO PANEL PARA LOS 'STAGES'

                col = layout.column()
                row = col.row(align=True)
                row.ui_units_x = 6

                active = dyntopo.levels_active
                for lvl in range(1, 7):
                    row.operator("bas.dyntopo_change_level", text=str(lvl), depress=(lvl == active)).lvl = lvl
                return 9.83
        return 1.93


#   TEXTURE SETTINGS (DROPDOWN) / NEW TEXTURE / OPEN IMAGE
    def texture_options(th):
        row = th.layout.row(align=True)
        row.popover(panel="VIEW3D_PT_tools_brush_texture", icon_value=Icon.TEXTURE(), text="")
        x = 1.6
        if th.props.texture_options_show_new_texture:
            x += 1
            row.operator("texture.new", text="", icon_value=Icon.TEXTURE_NEW()) # NEW TEXTURE
        if th.props.texture_options_show_open_image:
            x += 1
            row.operator("image.open", text="", icon_value=Icon.TEXTURE_OPEN()) # OPEN IMAGE TEXTURE

        return x

#   TEXTURE QUICK SELECTOR
    def texture_manager(th):
        brush = th.brush
        texture = brush.texture
        tex_rows_cols = th.prefs.texture_selector_grid_size
        img_rows_cols = th.prefs.image_selector_grid_size
        row = th.layout.row(align=True)
        ## TEXTURES AND IMAGES
        if texture != None: # HAY TEXTURA
            if texture.image != None: # image_user -> image # LA TEXTURA TIENE IMAGEN
                if th.props.texture_manager_collapse:
                    row.ui_units_x = 4
                    row.prop(brush, "texture", text="")
                    row.prop(texture, "image", text="") # open="image.open"
                else:
                    row.ui_units_x = 14
                    row.template_ID_preview(brush, "texture", rows=tex_rows_cols[0], cols=tex_rows_cols[1], hide_buttons=True)
                    row.template_ID_preview(texture, "image", rows=img_rows_cols[0], cols=img_rows_cols[1], hide_buttons=True) # open="image.open"
            else: # LA TEXTURA NOO TIENE IMAGEN
                row.ui_units_x = 5
                row.template_ID_preview(texture, "image", rows=img_rows_cols[0], cols=img_rows_cols[1], open="image.open", hide_buttons=False) # open="image.open"
        else: # NO HAY TEXTURA
            row.ui_units_x = 5
            row.template_ID_preview(brush, "texture", rows=tex_rows_cols[0], cols=tex_rows_cols[1], new="texture.new", hide_buttons=False)

        return row.ui_units_x

#   INCREMENTAL SAVE
    def incremental_save(th):
        th.layout.operator('file.incremental_save', text="", icon_value=get_icon(Icon.BRUSH_SAVE))
        return 1

#   PANEL FOR TOGGLE UI ELEMENTS
    def settings(layout):
        sub = layout.split().column(align=True)
        sub.popover(panel="NSMUI_PT_th_settings",icon='HIDE_OFF',text="")

#   PREFERENCES PANEL
    def bas_preferences(layout):
        sub = layout.split().column(align=True)
        sub.popover(panel="NSMUI_PT_Addon_Prefs",icon='PREFERENCES',text="")

#   BLENDER QUICK PREFERENCES FOR SCULPT
    def blender_preferences(layout):
        sub = layout.split().column(align=True)
        sub.popover(panel="BAS_PT_Blender_QuickPrefs",icon='BLENDER',text="")

    def dev_support(layout):
        prefs = context.preferences.addons["BlenderAtelier_Sculpt"].preferences
        sub = layout.split().column(align=True)
        if prefs.need_updating:
            text="Update Available!"
        else:
            text=""
        sub.popover(panel="NSMUI_PT_dev_support",icon='FUND',text=text)
