from bpy.types import Operator
import bpy
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty, EnumProperty
from ...utils.others import ShowMessageBox


class BAS_OT_mask_extractor_apply_changes(Operator):
    """Extracts the masked area to create a new mesh"""
    bl_idname = "bas.mask_extractor_apply_changes"
    bl_label = "Mask Extractor: Apply Changes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.window_manager.bas_extractor
        if not props.extracted:
            ShowMessageBox("No recent Extracted Mesh data was found", "Can't do this!" 'INFO')
            return {'CANCELLED'}
        obj = props.extracted
        act_obj = context.active_object
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
            #bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(state=True)
            context.view_layer.objects.active = obj
            if obj != None:
                for mod in obj.modifiers:
                    bpy.ops.object.modifier_apply(modifier=mod.name)
        except:
            ShowMessageBox("No recent Extracted Mesh data was found", "Can't do this!" 'INFO')
            pass

        props.extracted = None
        props.is_created = False

        act_obj.select_set(state=True)
        context.view_layer.objects.active = act_obj
        bpy.ops.object.mode_set(mode='SCULPT')

        return {'FINISHED'}

class BAS_OT_mask_extractor_quick(Operator):
    """Extracts the masked area to create a new mesh"""
    bl_idname = "bas.mask_extractor_quick"
    bl_label = "Quick Mask Extractor"
    bl_options = {'REGISTER', 'UNDO'}

    offset : FloatProperty(min = -10.0, max = 10.0, default = 0.1, name="Offset")
    thickness : FloatProperty(min = 0.0, max = 10.0, default = 0.5, name="Thickness")
    smoothPasses : IntProperty(min = 0, max = 30, default = 12, name="Smooth Passes")  
    mode : EnumProperty(name="Extract Mode",
                     items = (("SOLID","Solid",""),
                              ("SINGLE","One Sided",""),
                              ("FLAT","Flat","")),
                     default = "SOLID", description="Mode in how to apply the mesh extraction"
    )
    superSmooth : BoolProperty(default = False, name="Super Smooth")
    editNewMesh : BoolProperty(default = True, name="Edit New Mesh", description="Edit new mesh when extracting it from mask")
    keepMask : BoolProperty(default = False, name="Keep Mask", description="Keep Original Mask")
    postEdition : BoolProperty(default = False, name="Post-Edition", description="Be able to edit some values after extracting, the apply changes.")
    fails : IntProperty (default=0, name="Number of User Fails xD")
    smooth_borders : BoolProperty(default = True, name="Smooth Borders")

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.mode == 'SCULPT'
    
    def draw(self, context): 
        layout = self.layout
        layout.prop(self, "mode", text="Mode")
        layout.prop(self, "thickness", text="Thickness")
        layout.prop(self, "smoothPasses", text="Smooth Passes")
        layout.prop(self, "editNewMesh", text="Edit New Mesh")
        layout.prop(self, "keepMask", text="Keep Mask")
        layout.prop(self, "postEdition", text="Post-Edition")
    
    def execute(self, context):
        props = context.window_manager.bas_extractor
        activeObj = context.active_object # Referencia al objeto activo
        try:
            if activeObj.modifiers["Multires"]:
                ShowMessageBox("The extractor is not compatible with Multires Modifier", "Can't extract mask", 'ERROR')
                return {'FINISHED'}
        except:
            pass
        bpy.ops.paint.mask_flood_fill(mode='INVERT') # INVERTIMOS LA MÁSCARA
        bpy.ops.paint.hide_show(action='HIDE', area='MASKED') # ESCONDEMOS LA PARTE NO ENMASCARADA (LA AHORA ENMASCARADA)
        bpy.ops.object.mode_set(mode='EDIT') # Cambiamos a edit
        bpy.ops.mesh.select_all(action='SELECT') # SELECCIONAR TODOS LOS VERTICES VISIBLES (YA ESTAN POR DEFECTO, CASI TODOS, SINO: CAMBIAR TIPO SELECCION A VERT/EDGE)
        # Duplicado de la malla
        bpy.ops.mesh.duplicate_move(MESH_OT_duplicate={"mode":1}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
        try:
            bpy.ops.mesh.separate(type='SELECTED') # Separamos la malla duplicada
        except:
            if self.fails < 2:
                ShowMessageBox("Where is the mask? Please, create a mask before calling this!", "Can't do this!", 'ERROR')
            elif self.fails < 5:
                ShowMessageBox("As I tell you.... YOU CAN'T EXTRACT A MESH FROM A MASK IF YOU DON'T HAVE A MASK!!!!", "Can't do this!", 'ERROR')
            elif self.fails < 10:
                ShowMessageBox("I wonder why natural selection has not acted yet. OK. Create a mask or...", "Can't do this!", 'ERROR')
            elif self.fails == 10:
                ShowMessageBox("...I will format your computer you bad boy/girl!", "Who dare me!", 'ERROR')
            else:
                ShowMessageBox("Where is the mask? Please, create a mask before calling this!", "Can't do this!", 'ERROR')
            self.fails += 1
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            activeObj.select_set(state=True)
            context.view_layer.objects.active = activeObj # context.selected_objects[0]
            bpy.ops.object.mode_set(mode='SCULPT') # volvemos a Sculpt
            bpy.ops.paint.hide_show(action='SHOW', area='ALL') # mostrar todo
            bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0) # borrar mascara si no se quiere mantener
            return {'FINISHED'}
        if self.fails > 9:
            ShowMessageBox("You got it!", "ALELUYA!", 'FUND')
        self.fails = 0
        bpy.ops.object.mode_set(mode='OBJECT') # Cambiamos a Object
        n = len(context.selected_objects)
        context.view_layer.objects.active = context.selected_objects[0] if n == 1 else context.selected_objects[1] if n > 1 else activeObj # Seleccionamos la malla extraida

        props.is_created = True

        # TRUCO PARA BORRAR GEOMETRIA SUELTA, BORDES ETC
        bpy.ops.object.mode_set(mode='EDIT') # trick
        bpy.ops.mesh.select_mode(type='VERT', action='TOGGLE')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.delete_loose() # borrar vertices sueltos para cada malla
        bpy.ops.object.mode_set(mode='OBJECT') # Cambiamos a Object

        extractedMesh = context.active_object # Guardamos referencia a la malla extraida
        props.extracted = extractedMesh
        bpy.ops.object.select_all(action='DESELECT') # deseleccionar todo # QUITANDO ESTA LINEA PUEDES VER EL OUTLINE DE LA MALLA EXTRAIDA MIENTARS ESCULPES EN LA MALLA BASE, UTIL EN ALGUNOS CASOS
        # Solid mode, doble cara
        if self.mode == 'SOLID':
            bpy.ops.object.mode_set(mode='OBJECT')
            obj = context.active_object
            if self.smoothPasses > 0: # aplicar smooth inicial solo si los pases son mayores a 0
                smooth = obj.modifiers.new(name="Smooth", type='SMOOTH')
                smooth.iterations = self.smoothPasses
                if not self.postEdition:
                    bpy.ops.object.modifier_apply(modifier="Smooth")
            solidi = obj.modifiers.new(name="Solid", type='SOLIDIFY')
            solidi.thickness = self.thickness
            solidi.offset = 1 # add later
            solidi.thickness_clamp = 0
            solidi.use_rim = True
            solidi.use_rim_only = False
            if not self.postEdition:
                bpy.ops.object.modifier_apply(modifier="Solid")
            if self.superSmooth: # post-smooth para suavizarlo mucho más
                co_smooth = obj.modifiers.new(name="Co_Smooth", type='CORRECTIVE_SMOOTH')
                co_smooth.iterations = 30
                co_smooth.smooth_type = 'LENGTH_WEIGHTED'
                co_smooth.use_only_smooth = True
                if not self.postEdition:
                    bpy.ops.object.modifier_apply(modifier="Co_Smooth")
        # Modo Single, sólo una cara
        elif self.mode == 'SINGLE':
            bpy.ops.object.mode_set(mode='OBJECT')
            obj = context.active_object
            if self.smoothPasses > 0 and self.superSmooth==False:
                smooth = obj.modifiers.new(name="Smooth", type='SMOOTH')
                smooth.iterations = self.smoothPasses
                if not self.postEdition:
                    bpy.ops.object.modifier_apply(modifier="Smooth")
            solidi = obj.modifiers.new(name="Solid", type='SOLIDIFY')
            solidi.thickness = self.thickness
            solidi.offset = 1 # add later
            solidi.thickness_clamp = 0
            solidi.use_rim = True
            solidi.use_rim_only = True # only one sided
            if not self.postEdition:
                bpy.ops.object.modifier_apply(modifier="Solid")
            if self.superSmooth: # post-smooth para suavizarlo mucho más
                # Seleccion de borde entre malla extraida y malla original
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT', action='TOGGLE')    
                bpy.ops.mesh.select_non_manifold()
                # Invertir
                bpy.ops.mesh.select_all(action='INVERT')
                # Añadir al vertex group 
                bpy.ops.object.vertex_group_add()
                bpy.ops.object.vertex_group_assign()
                # Aplica smooth
                bpy.ops.object.mode_set(mode='OBJECT')
                smooth = obj.modifiers.new(name="Co_Smooth", type='SMOOTH')
                smooth.factor = 1.5
                smooth.iterations = 30 # valor máximo
                smooth.vertex_group = context.object.vertex_groups.active.name # usa vertex group
                if not self.postEdition:
                    bpy.ops.object.modifier_apply(modifier="Co_Smooth")
                if self.smooth_borders:
                    smooth = obj.modifiers.new(name="Lap_Smooth", type='LAPLACIANSMOOTH')
                    smooth.invert_vertex_group = True
                    smooth.vertex_group = context.object.vertex_groups.active.name
                    smooth.use_normalized = False
                    smooth.use_volume_preserve = False
                    smooth.iterations = 100
                    if not self.postEdition:
                        bpy.ops.object.modifier_apply(modifier="Lap_Smooth")
        
        # Flat mode. Sólo un plano
        elif self.mode == 'FLAT':
            pass
        # Dependiendo si queremos editar la nueva malla o no
        if self.editNewMesh: # Si vamos a la malla a editar, primero tenemos que pasar por la malla de origen para mostrarla al completo
            context.view_layer.objects.active = activeObj # objeto origen como activo
            bpy.ops.object.mode_set(mode='SCULPT') # Cambiamos a Sculpt
            bpy.ops.paint.hide_show(action='SHOW', area='ALL') # mostrar todo
            if self.keepMask == False:
                bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0) # borrar mascara si no se quiere mantener
            else:
                bpy.ops.paint.mask_flood_fill(mode='INVERT') # invertir máscara para dejarla tal cual estaba en un inicio
            bpy.ops.object.mode_set(mode='OBJECT') # volver a object mode
            context.view_layer.objects.active = extractedMesh # malla extraida marcada como activa
            bpy.ops.object.mode_set(mode='SCULPT') # Cambiamos a Sculpt de nuevo
            bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0) # quitar mascara de la malla extraida
        else:
            context.view_layer.objects.active = activeObj # context.selected_objects[0]
            bpy.ops.object.mode_set(mode='SCULPT') # volvemos a Sculpt
            bpy.ops.paint.hide_show(action='SHOW', area='ALL') # mostrar todo
            if self.keepMask == False:
                bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0) # borrar mascara si no se quiere mantener
            else:
                bpy.ops.paint.mask_flood_fill(mode='INVERT') # invertir máscara para dejarla tal cual estaba en un inicio

        if not props.post_edition:
            props.is_created = False
        if props.mode == 'FLAT':
            props.is_created = False

        return {'FINISHED'}


class BAS_OT_mask_extractor(Operator):
    """Extracts the masked area to create a new mesh"""
    bl_idname = "bas.mask_extractor"
    bl_label = "Mask Extractor"
    bl_options = {'REGISTER', 'UNDO'}

    offset : FloatProperty(min = -10.0, max = 10.0, default = 0.1, name="Offset")
    thickness : FloatProperty(min = 0.0, max = 10.0, default = 0.5, name="Thickness")
    smoothPasses : IntProperty(min = 0, max = 30, default = 4, name="Smooth Passes")  
    mode : EnumProperty(name="Extract Mode",
                     items = (("SOLID","Solid",""),
                              ("SINGLE","One Sided",""),
                              ("FLAT","Flat","")),
                     default = "SOLID", description="Mode in how to apply the mesh extraction"
    )
    superSmooth : BoolProperty(default = False, name="Super Smooth")
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.mode == 'SCULPT'
    
    def draw(self, context): 
        layout = self.layout
        layout.prop(self, "mode", text="Mode")
        layout.prop(self, "thickness", text="Thickness")
        #layout.prop(self, "offset", text="Offset")
        layout.prop(self, "smoothPasses", text="Smooth Passes")
    
    def execute(self, context):
        activeObj = context.active_object
        
        # This is a hackish way to support redo functionality despite sculpt mode having its own undo system.
        # The set of conditions here is not something the user can create manually from the UI.
        # Unfortunately I haven't found a way to make Undo itself work
        if  2>len(bpy.context.selected_objects)>0 and \
            context.selected_objects[0] != activeObj and \
            context.selected_objects[0].name.startswith("Extracted_"):
            rem = context.selected_objects[0]
            remname = rem.data.name
            bpy.data.scenes.get(context.scene.name).objects.unlink(rem) # checkear esto
            bpy.data.objects.remove(rem)
            # remove mesh to prevent memory being cluttered up with hundreds of high-poly objects
            bpy.data.meshes.remove(bpy.data.meshes[remname])
        
        # For multires we need to copy the object and apply the modifiers
        try:
            if activeObj.modifiers["Multires"]:
                use_multires = True
                objCopy = helper.objDuplicate(activeObj)
                context.view_layer.objects.active = objCopy
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.boolean.mod_apply()
        except:
            use_multires = False
            pass
            
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Automerge will collapse the mesh so we need it off.
        if context.scene.tool_settings.use_mesh_automerge:
            automerge = True
            bpy.data.scenes[context.scene.name].tool_settings.use_mesh_automerge = False
        else:
            automerge = False

        # Until python can read sculpt mask data properly we need to rely on the hiding trick
        #bpy.ops.mesh.select_all(action='SELECT')
        #bpy.ops.mesh.normals_make_consistent()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.paint.hide_show(action='HIDE', area='MASKED')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.duplicate_move(MESH_OT_duplicate=None, TRANSFORM_OT_translate=None)
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode='EDIT')

        #print(context.active_object)
        #print(context.view_layer.objects.active)

        # For multires we already have a copy, so lets use that instead of separate.
        if use_multires == True:
            bpy.ops.mesh.select_all(action='INVERT')
            bpy.ops.mesh.delete(type='FACE')
            context.view_layer.objects.active = objCopy
        else:
            try:
                bpy.ops.mesh.separate(type="SELECTED")
                context.view_layer.objects.active = context.selected_objects[0] #bpy.context.window.scene.objects[0] #context.selected_objects[0]
            except:
                bpy.ops.object.mode_set(mode='SCULPT')
                bpy.ops.paint.hide_show(action='SHOW', area='ALL')
                return {'FINISHED'}
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Rename the object for disambiguation
        context.view_layer.objects.active.name = "Extracted_" + context.view_layer.objects.active.name
        #bpy.ops.object.mode_set(mode='EDIT')
        #print(context.active_object)
        #print(context.view_layer.objects.active)
        
        # Solid mode should create a two-sided mesh
        if self.mode == 'SOLID':
            '''
            if self.superSmooth:
                # Seleccion de borde entre malla extraida y malla original
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE', action='TOGGLE')
                bpy.ops.mesh.select_non_manifold()
                # Aumentar seleccion en 1
                bpy.ops.mesh.select_more()
                # Invertir
                bpy.ops.mesh.select_all(action='INVERT')
                # Añadir al vertex group 
                bpy.ops.object.vertex_group_add()
                bpy.ops.object.vertex_group_assign()
                # Guardar referencia para más tarde
                ob = context.object
                group = ob.vertex_groups.active
            '''
            bpy.ops.object.mode_set(mode='OBJECT')
            obj = context.active_object
            if self.smoothPasses > 0: # aplicar smooth inicial solo si los pases son mayores a 0
                smooth = obj.modifiers.new(name="Smooth", type='SMOOTH')
                smooth.iterations = self.smoothPasses
                bpy.ops.object.modifier_apply(modifier="Smooth")
            solidi = obj.modifiers.new(name="Solid", type='SOLIDIFY')
            solidi.thickness = self.thickness
            solidi.offset = 1 # add later
            solidi.thickness_clamp = 0
            solidi.use_rim = True
            solidi.use_rim_only = False
            bpy.ops.object.modifier_apply(modifier="Solid")
            if self.superSmooth: # post-smooth para suavizarlo mucho más
                #bpy.ops.object.vertex_group_select()
                #smooth = obj.modifiers.new(name="Smooth", type='SMOOTH')
                #smooth.iterations = self.smoothPasses
                #smooth.vertex_group = group.name
                #bpy.ops.object.modifier_apply(modifier="Smooth")
                co_smooth = obj.modifiers.new(name="Co_Smooth", type='CORRECTIVE_SMOOTH')
                co_smooth.iterations = 30
                co_smooth.smooth_type = 'LENGTH_WEIGHTED'
                co_smooth.use_only_smooth = True
                bpy.ops.object.modifier_apply(modifier="Co_Smooth")

        elif self.mode == 'SINGLE':
            bpy.ops.object.mode_set(mode='OBJECT')
            obj = context.active_object
            if self.smoothPasses > 0 and self.superSmooth==False:
                smooth = obj.modifiers.new(name="Smooth", type='SMOOTH')
                smooth.iterations = self.smoothPasses
                bpy.ops.object.modifier_apply(modifier="Smooth")
            solidi = obj.modifiers.new(name="Solid", type='SOLIDIFY')
            solidi.thickness = self.thickness
            solidi.offset = 1 # add later
            solidi.thickness_clamp = 0
            solidi.use_rim = True
            solidi.use_rim_only = True # only one sided
            bpy.ops.object.modifier_apply(modifier="Solid")
            if self.superSmooth: # post-smooth para suavizarlo mucho más
                # Seleccion de borde entre malla extraida y malla original
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT', action='TOGGLE')    
                bpy.ops.mesh.select_non_manifold()
                # Invertir
                bpy.ops.mesh.select_all(action='INVERT')
                # Añadir al vertex group 
                bpy.ops.object.vertex_group_add()
                bpy.ops.object.vertex_group_assign()
                # Aplica smooth
                bpy.ops.object.mode_set(mode='OBJECT')
                smooth = obj.modifiers.new(name="Smooth", type='SMOOTH')
                smooth.factor = 1.5
                smooth.iterations = 30 # valor máximo
                smooth.vertex_group = context.object.vertex_groups.active.name # usa vertex group
                bpy.ops.object.modifier_apply(modifier="Smooth")
                # trick scale to close up the extracted mesh to original mesh due to smooth # not necessary now

            
        elif self.mode == 'FLAT':
            pass
            ''' OLD
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            n = 0
            while n < self.smoothPasses:
                bpy.ops.mesh.vertices_smooth()
                n+=1
            #bpy.ops.mesh.solidify(thickness=0)
            '''

            # later will add close mesh bool
            
        # clear mask on the extracted mesh
        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0)
        
        bpy.ops.object.mode_set(mode='OBJECT')

        # make sure to recreate the odd selection situation for redo
        if use_multires:
            bpy.ops.object.select_pattern(pattern=context.active_object.name, case_sensitive=True, extend=False)

        #bpy.ops.object.select_all(action = 'DESELECT')

        #context.view_layer.objects.active = activeObj
        
        # restore automerge
        if automerge:
            bpy.data.scenes[context.scene.name].tool_settings.use_mesh_automerge = True

        # restore mode for original object
        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.paint.hide_show(action='SHOW', area='ALL')
        #if(usingDyntopo):
        #    bpy.ops.sculpt.dynamic_topology_toggle()
        return {'FINISHED'}


classes = (
    BAS_OT_mask_extractor_apply_changes,
    BAS_OT_mask_extractor_quick,
    BAS_OT_mask_extractor
)