from bpy.types import Operator
import bpy
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty, EnumProperty
from ...utils.others import ShowMessageBox


class BAS_OT_mask_detacher(Operator):
    """Cut your sculpt as you want! Take care it cuts!"""
    bl_idname = "bas.mask_detacher"
    bl_label = "From Mask Detacher"
    bl_options = {'REGISTER', 'UNDO'}

    solidify : BoolProperty(default = False, name="Solidify", description="Apply solidify to detached meshes")
    offset : FloatProperty(min = -10.0, max = 10.0, default = 0.1, name="Offset")
    thickness : FloatProperty(min = 0.0, max = 10.0, default = 0.5, name="Thickness")
    smoothPasses : IntProperty(min = 0, max = 30, default = 15, name="Smooth Passes")  
    mode : EnumProperty(name="Extract Mode",
                     items = (("SOLID","Solid",""),

                              ("SINGLE","One Sided",""),
                              ("FLAT","Flat","")),
                     default = "SOLID", description="Mode in how to apply the mesh extraction"
    )
    smoothBorders : BoolProperty(default = False, name="Smooth Borders", description="Smooth borders from all detached parts")
    sculptMaskedMesh : BoolProperty(default = False, name="Sculpt Masked Mesh", description="Go to sculpt new mesh when detaching it from mask")
    detachInDifferentObjects : BoolProperty(default = True, name="Detach in Different Objects", description="Detach meshes into different objects")
    separateLooseParts : BoolProperty(default = False, name="Separate Loose Parts", description="Detach all loose parts, those that are separate meshes")
    closeDetachedMeshes : BoolProperty(default = True, name="Close Detached Meshes", description="Close hooles in the meshes made by the detacher")
    closeOnlyMasked : BoolProperty(default = False, name="Only Masked", description="Closes only masked mesh")
    doRemesh : BoolProperty(default = True, name="Remesh it", description="Remesh it just when you activate close detached meshes")

    def execute(self, context):
        activeObj = context.active_object # Referencia al objeto activo
        try:
            # NO HAY COMPATIBILIDAD CON MULTIRES, EL PROCESO SE HACE MÁS COMPLEJO Y SOBRETODO LENTO,
            # POR LO QUE NO SALE RENTABLE TRABAJAR CON MULTIRES Y CUALQUIER HERRAMIENTA DE ESTE ESTILO
            if activeObj.modifiers["Multires"]:
                ShowMessageBox("The detacher is not compatible with Multires Modifier. Anyway, It will be a so slow process.", "Can't detach from mask", 'ERROR')
                return {'FINISHED'}
        except:
            pass

        bpy.ops.paint.mask_flood_fill(mode='INVERT') # INVERTIMOS LA MÁSCARA
        bpy.ops.paint.hide_show(action='HIDE', area='MASKED') # ESCONDEMOS LA PARTE NO ENMASCARADA (LA AHORA ENMASCARADA)
        bpy.ops.object.mode_set(mode='EDIT') # Cambiamos a edit
        bpy.ops.mesh.select_mode(type='FACE', action='TOGGLE')
        bpy.ops.mesh.select_all(action='SELECT') # SELECCIONAR TODOS LOS VERTICES VISIBLES (YA ESTAN POR DEFECTO, CASI TODOS, SINO: CAMBIAR TIPO SELECCION A VERT/EDGE)
        try:
            bpy.ops.mesh.separate(type='SELECTED') # Separamos los vertices separados
        except:
            ShowMessageBox("Where is the mask? Please, create a mask before calling this!", "Can't do this!", 'ERROR')
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            activeObj.select_set(state=True)
            context.view_layer.objects.active = activeObj # context.selected_objects[0]
            bpy.ops.object.mode_set(mode='SCULPT') # volvemos a Sculpt
            bpy.ops.paint.hide_show(action='SHOW', area='ALL') # mostrar todo
            bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0) # borrar mascara si no se quiere mantener
            return {'FINISHED'}
        bpy.ops.object.mode_set(mode='OBJECT') # trick
        bpy.ops.object.mode_set(mode='EDIT') # trick
        bpy.ops.mesh.select_mode(type='VERT', action='TOGGLE')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.delete_loose() # borrar vertices sueltos para cada malla
        bpy.ops.object.mode_set(mode='OBJECT') # Cambiamos a Object
        context.view_layer.objects.active = context.selected_objects[1] # Seleccionamos la malla extraida
        maskedObj = context.active_object # Guardamos referencia a la malla extraida
        bpy.ops.object.select_all(action='DESELECT') # deseleccionar todo # QUITANDO ESTA LINEA PUEDES VER EL OUTLINE DE LA MALLA EXTRAIDA MIENTARS ESCULPES EN LA MALLA BASE, UTIL EN ALGUNOS CASOS
        
        if self.detachInDifferentObjects == False: # SAME OBJECT
            activeObj.select_set(state=True) # AÑADIMOS EL OBJETO INICIAL A LA SELECCION
            maskedObj.select_set(state=True) # AÑADIMOS EL OBJETO SEPARADO A LA SELECCION
            bpy.ops.object.join() # JOIN PARA AMBOS OBJ

        else: # DIFERRENT OBJECTS
            if self.separateLooseParts: # SEPARAR EN DIFERENTES PARTES
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_mode(type='FACE', action='TOGGLE')
                bpy.ops.mesh.select_all(action='SELECT') # seleccionar todos los vertices
                bpy.ops.mesh.separate(type='LOOSE') # separar cada malla separada
                #bpy.ops.mesh.select_mode(type='VERT', action='TOGGLE')
                #bpy.ops.object.mode_set(mode='OBJECT')
                #bpy.ops.object.mode_set(mode='EDIT')
                #bpy.ops.mesh.select_all(action='SELECT') # seleccionar todos los vertices
                #bpy.ops.mesh.delete_loose() # borrar vertices sueltos para cada malla
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.object.select_all(action='DESELECT') # Ver si es op
                context.view_layer.objects.active = activeObj
            else:
                #bpy.ops.object.mode_set(mode='OBJECT')
                #bpy.ops.object.select_all(action='DESELECT') # Ver si es op
                
                if self.closeDetachedMeshes:
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_all(action='DESELECT')
                    bpy.ops.mesh.select_mode(type='EDGE', action='TOGGLE')
                    bpy.ops.mesh.select_non_manifold()
                    bpy.ops.mesh.edge_face_add()
                    #bpy.ops.mesh.fill()
                    '''
                    bpy.ops.mesh.select_more()
                    bpy.ops.mesh.select_more()
                    bpy.ops.mesh.select_more()
                    bpy.ops.mesh.vertices_smooth(repeat=10)
                    bpy.ops.mesh.select_all(action='DESELECT')
                    bpy.ops.mesh.select_non_manifold()
                    bpy.ops.mesh.fill()
                    bpy.ops.mesh.select_more()
                    bpy.ops.mesh.select_more()
                    bpy.ops.mesh.select_more()
                    bpy.ops.mesh.vertices_smooth(repeat=5)
                    '''
                    if self.doRemesh:
                        bpy.ops.object.mode_set(mode='SCULPT')
                        bpy.ops.object.voxel_remesh()

                    bpy.ops.object.mode_set(mode='OBJECT')

                    #bpy.ops.object.select_all(action='DESELECT') # Ver si es op
                    #activeObj.select_set(state=True) # AÑADIMOS EL OBJETO INICIAL A LA SELECCION
                    context.view_layer.objects.active = activeObj
                    #bpy.ops.object.mode_set(mode='SCULPT')
                    #bpy.ops.bas.close_gaps(use='TRIS', smooth_passes=3, keep_dyntopo=True)

                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_all(action='DESELECT')
                    bpy.ops.mesh.select_non_manifold()
                    bpy.ops.mesh.edge_face_add()
                    #bpy.ops.mesh.fill()    

                    if self.doRemesh and self.closeOnlyMasked==False:
                        bpy.ops.object.mode_set(mode='SCULPT')
                        bpy.ops.object.voxel_remesh()
                        
                    bpy.ops.object.mode_set(mode='OBJECT')
                    

                if self.sculptMaskedMesh: # SE QUEDA LA PARTE ENMASCARADA Y VA A SCULPT PARA EDITARLA
                    context.view_layer.objects.active = activeObj
                    bpy.ops.object.mode_set(mode='SCULPT')
                    bpy.ops.paint.hide_show(action='SHOW', area='ALL') # mostrar todo
                    bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0) # borrar mascara
                    bpy.ops.object.mode_set(mode='OBJECT')
                    activeObj.select_set(state=False)
                    context.view_layer.objects.active = maskedObj
                    bpy.ops.object.mode_set(mode='SCULPT')
                    return {'FINISHED'}
                    
                else:
                    maskedObj.select_set(state=False)
                    context.view_layer.objects.active = activeObj
        
        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.paint.hide_show(action='SHOW', area='ALL') # mostrar todo
        bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0) # borrar mascara
        
        activeObj.select_set(state=True)
        context.view_layer.objects.active = activeObj
        return {'FINISHED'}


classes = (
    BAS_OT_mask_detacher,
)