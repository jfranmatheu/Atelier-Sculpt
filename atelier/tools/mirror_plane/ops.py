# Copyright (C) 2019 Juan Fran Matheu G.
# Contact: jfmatheug@gmail.com 

import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, PointerProperty, BoolProperty, FloatProperty
import numpy as npy
import mathutils
from mathutils import Vector


class BAS_OT_mirror_plane_delete(Operator):
    bl_idname = "bas.mirror_plane_delete"
    bl_label = "Delete Mirror Plane"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        mirror = context.scene.bas_mirrorplane
        mirror_object = mirror.mirror_object
        if not mirror_object:
            mirror.created = False
            mirror.show = False
            return {'FINISHED'}
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        mirror_object.select_set(state=True)
        context.view_layer.objects.active = mirror_object
        bpy.data.objects.remove(mirror_object)
        mirror.created = False
        mirror.show = False
        obj.select_set(state=True)
        context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='SCULPT')
        return {'FINISHED'}

from ...utils.others import ShowMessageBox
class BAS_OT_mirror_plane(Operator):
    bl_idname = "bas.mirror_plane"
    bl_label = "Mirror Plane"
    bl_options = {'REGISTER', 'UNDO'}

    oldDim : FloatVectorProperty(default=[0 , 0, 0], size=3)
    #auto_update : BoolProperty(default = True, name="Auto Update", description="Update mirror plane in real time")
    useWorldOrigin : BoolProperty(default = False, name="Use World Origin")
    #maxLoops : FloatProperty(default=24)
    #loop : FloatProperty(default=0)
    #color = FloatVectorProperty(name="Color for the mirror plane", subtype='COLOR', min=0, max=1, description="Change Color of the mirror plane")
    #mirror_plane : PointerProperty(type=bpy.types.Object, name="Mirrow Plane Object")
    #source_model : PointerProperty(type=bpy.types.Object, name="Mirrow Plane Object")

    @classmethod
    def poll(cls, context):
        return context.active_object != None and context.mode == 'SCULPT'

    def modal(self, context, event):
        mirror = context.scene.bas_mirrorplane
        if not mirror.show:
            #context.window_manager.event_timer_remove(self._timer)
            # OCULTAR MIRROR
            try:
                mirror.mirror_object.hide_viewport = True
            except:
                pass
            return {'FINISHED'}
        if(context.mode == "SCULPT"):
            sculpt = context.tool_settings.sculpt
            if not sculpt.use_symmetry_x: # or not context.scene.created
                mirror.show = False
                try:
                    mirror.mirror_object.hide_viewport = True
                except:
                    pass
                ShowMessageBox("You need to turn ON the X symmetry", "Can't do this!", 'ERROR')
                return {"CANCELLED"}
            
            #if self.loop > self.maxLoops:
            obj = mirror.source_model
            dim = obj.dimensions

            if self.oldDim[1] != dim[1] or self.oldDim[2] != dim[2]:
                #print(dim)
                #print(self.oldDim)
                #print("running")
                self.oldDim = dim
                offset = mirror.offset
                bb = obj.bound_box
                
                if self.useWorldOrigin:
                    loc = (0, 0, 0)
                else:
                    loc = obj.location

                bb = obj.bound_box
                #mw = obj.matrix_world
                A = npy.array(bb[0]) # [x, y, z]
                B = npy.array(bb[1]) # [x, y, z]
                C = npy.array(bb[2]) # [x, y, z]
                D = npy.array(bb[3]) # [x, y, z]
                E = npy.array(bb[4]) # [x, y, z]
                F = npy.array(bb[5]) # [x, y, z]
                G = npy.array(bb[6]) # [x, y, z]
                H = npy.array(bb[7]) # [x, y, z]

                v = (A+B+C+D+E+F+G+H)/8

                mirror.mirror_object.location   = (loc[0], v[1], v[2])
                mirror.mirror_object.dimensions = (0, dim[1] + offset[0], dim[2] + offset[1])
                #self.loop = 0

                if mirror.mirror_object.hide_viewport:
                    mirror.mirror_object.hide_viewport = False

            #self.loop += 1

            #mirror.mirror_plane.dimensions = mirror.source_model.dimensions + self.offset
            #mirror.mirror_plane.dimensions = (0, dim[1] * 2 + offset[1], dim[2] * 2 + offset[2])
        else:
            if not mirror.mirror_object.hide_viewport:
                mirror.mirror_object.hide_viewport = True
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        mirror = context.scene.bas_mirrorplane
        if mirror.mirror_object is None:
            self.execute(context)
            return {'FINISHED'}

        try:
            mirror.mirror_object.hide_viewport = False
        except:
            pass
        # ACTIVAR HANDLER
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
        
    def execute(self, context):
        mirror = context.scene.bas_mirrorplane
        #self.offset = mathutils.Vector(self.offset)

        try: # Si ya existe
            if mirror.mirror_object:
                # Sólamente activar y actualizar tamaño
                #plane.dimensions = obj.dimensions + self.offset
                #if context.scene.show:
                #    self.mirror_object.
                #    pass
                #else:
                #    pass
                return {'FINISHED'}
        except:
            pass
            
        # Crear plano
        obj = context.active_object
        mirror.source_model = obj
        bpy.ops.object.mode_set(mode='OBJECT')
        #col = bpy.ops.outliner.collection_new(nested=True)
        if mirror.use_world_origin:
            loc = (0, 0, 0)
        else:
            loc = obj.location

        bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, align='WORLD', location=loc, rotation=(0, 1.5708, 0))
        plane = context.active_object
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        plane.scale[0] = 0
        
        plane.name = "Mirror_Plane"
        plane.color =  mirror.color # (0.2,0.3,1,0.1) #
        plane.display.show_shadows = False
        offset = mirror.offset

        '''
        bb = obj.bound_box
        top     = npy.array((bb[0][0] , bb[0][1], bb[0][2])) # -1, -1, 0  [x, y, z] (local, escala aplicada)
        bottom  = npy.array((bb[1][0], bb[1][1], bb[1][2])) # 1, -1, 0 [x, y, z] (local, escala aplicada)
        back    = npy.array((bb[3][0] , bb[3][1], bb[3][2])) # -1, -1, 0  [x, y, z] (local, escala aplicada)
        height  = npy.linalg.norm(top-bottom)
        depth   = npy.linalg.norm(top-back)
        plane.dimensions = (0, depth + offset[1], height + offset[2])
        '''
        '''
        mesh = obj.data
        verts = mesh.vertices
        verts[0].co = top
        verts[1].co = bottom
        verts[3].co = back
        '''
        bb = obj.bound_box
        #mw = obj.matrix_world

        A = npy.array(bb[0]) # [x, y, z]
        B = npy.array(bb[1]) # [x, y, z]
        C = npy.array(bb[2]) # [x, y, z]
        D = npy.array(bb[3]) # [x, y, z]
        E = npy.array(bb[4]) # [x, y, z]
        F = npy.array(bb[5]) # [x, y, z]
        G = npy.array(bb[6]) # [x, y, z]
        H = npy.array(bb[7]) # [x, y, z]

        v = (A+B+C+D+E+F+G+H)/8

        plane.location   = (loc[0], v[1], v[2])
        plane.dimensions = (0, obj.dimensions[1] + offset[0], obj.dimensions[2] + offset[1])
        self.oldDim = obj.dimensions
        

        #plane.parent = obj
        plane.hide_select = True
        plane.hide_viewport = False
        mirror.mirror_object = plane

        context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='SCULPT')

        if mirror.show == False:
            mirror.show = True

        context.space_data.shading.color_type = 'OBJECT'
        mirror.created = True
 

        #bb = obj.bound_box
        #top = npy.array((bb[1][0] , bb[1][1], bb[1][2])) # -1, -1, 0  [x, y, z] (local, escala aplicada)
        #bottom = npy.array((bb[5][0], bb[5][1], bb[5][2])) # 1, -1, 0 [x, y, z] (local, escala aplicada)
    #   Primera forma de calcular la distancia
        #import numpy as npy
        #dist = npy.linalg.norm(top-bottom)
    #   Segunda forma de calcular la distancia
        #import numpy as npy
        #a = npy.array((xa ,ya, za))
        #b = npy.array((xb, yb, zb))
        #dist = npy.linalg.norm(a-b)
    #   Tercera forma de calcular la distancia
        #from math import dist
        #dist([xa, ya, za], [xb, yb, zb])

        # Al calcular la distancia aplicar esta sobre las dimensiones del plano

        return {'FINISHED'}


classes = (
    BAS_OT_mirror_plane,
    BAS_OT_mirror_plane_delete
)
