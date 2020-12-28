import bpy
from bpy.types import Operator
from ...utils.others import ShowMessageBox
import random
from mathutils import Vector
import numpy as npy
import bmesh


class BAS_OT_sculpt_notes_curve_to_mesh(Operator):
    bl_idname = "bas.sculpt_notes_curve_to_mesh"
    bl_label = "Sculpt Notes: Curve to Mesh"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):
        act_obj = context.active_object
        act_obj_name = act_obj.name
        SN = context.window_manager.bas_sculptnotes
        obj = SN.curve
        if not obj or obj.name not in context.view_layer.objects:
            ShowMessageBox("Can convert note to mesh! Curve not found!", "Ops! Something happened!")
            SN.isCreated = False
            SN.curve = None
            SN.curveShape = None
            SN.path_object = None
            return {'CANCELLED'}
        bpy.ops.object.mode_set(mode='OBJECT')

    ##########

        if   SN.path_object != None:
            objPath =   SN.path_object
            objPath.select_set(state=True)
            context.view_layer.objects.active = objPath
            bpy.ops.object.convert(target='MESH')
            for mod in objPath.modifiers:
                bpy.ops.object.modifier_apply(modifier=mod.name)

            # selecciono la curve path para convertirla (siempre después de aplicar los modificadores dependientes de esta)
            objPath.select_set(state=False)
            obj.select_set(state=True)
            context.view_layer.objects.active = obj
            bpy.ops.object.convert(target='MESH')

            # volvemos a seleccionar el obj path
            objPath.select_set(state=True)

            bpy.ops.object.join() # join, y el master será el objeto de curve path

            if SN.mirror:
                mirror = obj.modifiers.new(name="_Mirror", type='MIRROR')
                mirror.mirror_object = act_obj
                mirror.use_mirror_vertex_groups = False
                mirror.use_clip = True
            if   SN.remeshIt:
                if   SN.mirror:
                    bpy.ops.object.modifier_apply(modifier="_Mirror")
                bpy.ops.object.mode_set(mode='SCULPT')
                if  SN.reproject:
                    bpy.ops.bas.voxel_remesh_reproject()
                else:
                    bpy.ops.object.voxel_remesh()

            bpy.ops.object.mode_set(mode='OBJECT')

        else:
            #bpy.ops.object.select_all(action='DESELECT')
            if bpy.data.curves[obj.name].bevel_object == None:
                closeGaps = True
            else:
                closeGaps = False
            obj.select_set(state=True)
            context.view_layer.objects.active = obj
            bpy.ops.object.convert(target='MESH')

            if closeGaps:
                bpy.ops.object.mode_set(mode='SCULPT')
                bpy.ops.bas.close_gaps()
                bpy.ops.object.mode_set(mode='OBJECT')
            if   SN.mirror:
                mirror = obj.modifiers.new(name="_Mirror", type='MIRROR')
                mirror.mirror_object = act_obj
                mirror.use_mirror_vertex_groups = False
                mirror.use_clip = True
            if   SN.remeshIt:
                if   SN.mirror:
                    bpy.ops.object.modifier_apply(modifier="_Mirror")
                bpy.ops.object.mode_set(mode='SCULPT')
                if  SN.reproject:
                    bpy.ops.bas.voxel_remesh_reproject()
                else:
                    bpy.ops.object.voxel_remesh()
                bpy.ops.object.mode_set(mode='OBJECT')

        obj.select_set(state=False)

        if not act_obj:
            act_obj = bpy.data.objects.get(act_obj_name, None)
            if not act_obj:
                SN.isCreated = False
                SN.curve = None
                SN.curveShape = None
                SN.path_object = None
                return {'FINISHED'}
        act_obj.select_set(state=True)
        context.view_layer.objects.active = act_obj
        bpy.ops.object.mode_set(mode='SCULPT')

        SN.isCreated = False

        #obj.mode = 'SCULPT' # TEST

        SN.curve = None
        SN.curveShape = None
        SN.path_object = None
        return {'FINISHED'}
    
class BAS_OT_sculpt_notes_Convert(Operator):
    bl_idname = "bas.sculpt_notes_convert_to_3d"
    bl_label = "Convert Notes to 3D"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        SN = context.window_manager.bas_sculptnotes
    #   USING ANNOTATIONS # CONVERTING ANNOTATIONS TO GP IS NOT WORKING PROPERLY NOW / NO SUPPORT, PROBABLY IN A FUTURE?
        if SN.use == 'NOTES':
            #notes = bpy.data.grease_pencils['Annotations']
        #   GET NOTES DATA
            noteData = context.scene.grease_pencil
        #   CHECK IF THERE ARE STROKES
            try:
                if len(noteData.layers.active.active_frame.strokes) == 0: # if len(noteData.layers.active.active_frame.strokes) == 0:
                    ShowMessageBox("No annotation strokes! Make some strokes before!", "Can't do this", 'ERROR')
                    return {'FINISHED'}
            except:
                ShowMessageBox("No annotation strokes! Make some strokes before!", "Can't do this", 'ERROR')
                return {'FINISHED'}
        #   QUICK CHANGE TO OBJECT
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
        #   GET NOTES LAYER # access with name '' or with index
            noteLayer = noteData.layers.active # noteData.layers[0]
        #   GET NOTES FRAME # access with index # opacity, thickness, select... # add/remove frame
            noteFrame = noteLayer.active_frame # noteLayer.frames[0]
        #   GET NOTES STROKES # acess with index # display-mode, line-width, material index... # add/remove stroke
            noteStrokes = noteFrame.strokes
            numStrokes = len(noteStrokes)
        #   GET NOTES POINTS # access with index # location, pressure, strength, uv-rotation... ('foreach_get()') # add/remove point
            # notePoints[numStrokes][]
            noteObjs = []
            note_id = str(random.randint(0,500) + random.randint(0,500))

            if SN.mergeStrokes:
                # Default
                vertices = []
                edges = []
                faces = []
                face = ()
                oldPoint = None

                meshName = "SculptNotes_" + note_id + "_MergedStroke"
                mesh = bpy.data.meshes.new(meshName)   # create a new mesh
                ob = bpy.data.objects.new(meshName, mesh)      # create an object with that mesh
                ob.location = Vector((0,0,0)) #by.context.scene.cursor_location   # position object at 3d-cursor
                # Link light object to the active collection of current view layer,
                # so that it'll appear in the current scene.
                context.view_layer.active_layer_collection.collection.objects.link(ob)
                p = 0
                for n in range(0, numStrokes):
                #   FOR EACH POINT IN THE ACTUAL STROKE
                    strPoints = noteStrokes[n].points
                    #numPoints = len(strPoints)
                    #x = 0
                    for point in strPoints:
                        # first stroke and first point
                        if n == 0 and p == 0:
                            vertices.append(point.co)
                            face = face + (p,)
                            primVert = p
                            primPoint = point
                            oldPoint = point
                            p += 1 # Increment for next point
                        else:
                            a = npy.array((point.co[0] ,point.co[1], point.co[2]))
                            b = npy.array((oldPoint.co[0], oldPoint.co[1], oldPoint.co[2]))
                            d = npy.linalg.norm(a-b)
                            if d > SN.mergeDistThreshold:
                                vertices.append(point.co)
                                face = face + (p,)
                                edges.append((p-1, p))
                                p += 1 # Increment for next point
                                #x += 1
                                oldPoint = point
            #   UPDATE AND VALIDATE NEW MESH
                #face = face + (primVert,)
                #edges.append((p-1, 0))
                edges.append((p-1, 0))
                faces.append(face)
                mesh.from_pydata(vertices,edges,faces) # [] (empty) #   Fill the mesh with verts, edges, faces
                mesh.validate(verbose=True) # clean_customdata=True
                noteObjs.append(ob)
                mesh.remesh_voxel_size = 0.01
            #   BMESH # no es estrictamente necesario
                '''
                bm = bmesh.new()
                bm.from_mesh(mesh)
                # bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001) # ya no con los pases de comp con numpy
                bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
                bm.to_mesh(mesh)
                mesh.update() # Update mesh with new data # calc_edges=True
                '''
            # NO MERGE
            else:
            #   FOR EACH STROKE
                for n in range(0, numStrokes):
                    # Default
                    vertices = []
                    edges = []
                    faces = []
                    face = ()
                    oldPoint = None
                    # Create next mesh for next stroke
                    meshName = "SculptNotes_" + note_id + "_Stroke_" + str(n)
                    mesh = bpy.data.meshes.new(meshName)   # create a new mesh
                    ob = bpy.data.objects.new(meshName, mesh)      # create an object with that mesh
                    ob.location = Vector((0,0,0)) #by.context.scene.cursor_location   # position object at 3d-cursor
                    # Link light object to the active collection of current view layer,
                    # so that it'll appear in the current scene.
                    context.view_layer.active_layer_collection.collection.objects.link(ob)
                #   FOR EACH POINT IN THE ACTUAL STROKE
                    strPoints = noteStrokes[n].points
                    numPoints = len(strPoints)
                    p = 0 # RESET FOR NEXT STROKE
                    for point in strPoints:
                        # notePoints[numStrokes][p] = point
                        if p == 0 or p == numPoints:
                            if p == 0:
                                vertices.append(point.co)
                                face = face + (p,)
                                primVert = p
                                oldPoint = point
                            else:
                                # para cerrar el loop si el primer y ultimo están muy cerca
                                a = npy.array((point.co[0] ,point.co[1], point.co[2]))
                                b = npy.array((primVert.co[0], primVert.co[1], primVert.co[2]))
                                d = npy.linalg.norm(a-b)
                                if d > SN.mergeDistThreshold:
                                    vertices.append(point.co)
                                    edges.append((p-1, 0)) # movido de abajo, sólo se crea con el ultimo si estan cerca
                                    face = face + (p)
                                else:
                                    edges.append((p-2, 0)) # sino se obvia el ultimo vertice y se une con el anterior
                            p += 1 # Increment for next point
                        else:
                            a = npy.array((point.co[0] ,point.co[1], point.co[2]))
                            b = npy.array((oldPoint.co[0], oldPoint.co[1], oldPoint.co[2]))
                            d = npy.linalg.norm(a-b)
                            if d > SN.mergeDistThreshold:
                                vertices.append(point.co)
                                face = face + (p,)
                                edges.append((p-1, p))
                                p += 1 # Increment for next point
                                oldPoint = point
                #   UPDATE AND VALIDATE NEW MESH
                    #face = face + (primVert,)
                    #edges.append((p-1, 0))
                    faces.append(face)
                    mesh.from_pydata(vertices,edges,faces) # [] (empty) #   Fill the mesh with verts, edges, faces
                    mesh.validate(verbose=False) # clean_customdata=True
                    noteObjs.append(ob)
                    mesh.remesh_voxel_size = 0.01
                #   BMESH # no es estrictamente necesario

                    bm = bmesh.new()
                    bm.from_mesh(mesh)
                    # bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001) # ya no con los pases de comp con numpy
                    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
                    bm.to_mesh(mesh)
                    mesh.update() # Update mesh with new data # calc_edges=True

            SN.isCreated = True

            if SN.joinStrokes or SN.mergeStrokes:
                if len(noteObjs) > 1:
                    for o in noteObjs:
                        o.select_set(state=True)
                    context.view_layer.objects.active = noteObjs[0]
                    bpy.ops.object.join()
                    noteObjs = []
                    noteObjs.append(context.active_object)
                if SN.method_type == 'FLAT':
                    bpy.ops.object.select_all(action='DESELECT')
                    obj.select_set(state=True)
                    context.view_layer.objects.active = obj
                    bpy.ops.object.mode_set(mode='SCULPT')
                    SN.isCreated = False
                    return {'FINISHED'}
            else:
                SN.applyModifiersDirectly = True

            SN.gp = noteObjs[0]
            print("NOTE OBJECTS", noteObjs)

            obj.select_set(state=False)
            for o in noteObjs:
                o.select_set(state=True)
                context.view_layer.objects.active = o
                if not SN.ngon:
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
                    if SN.reproject:
                        bpy.ops.mesh.subdivide(number_cuts=2, ngon=False)
                        #bpy.ops.mesh.tris_convert_to_quads()
                        bpy.ops.object.mode_set(mode='OBJECT')
                        sw = o.modifiers.new(name="SW", type='SHRINKWRAP')
                        sw.wrap_method = 'NEAREST_SURFACEPOINT' # PROJECT # NEAREST_VERTEX # TARGET_PROJECT # NEAREST_SURFACEPOINT
                        sw.wrap_mode = 'ABOVE_SURFACE' # ABOVE_SURFACE # ON_SURFACE
                        sw.target = obj
                        bpy.ops.object.modifier_apply(modifier="SW")
                    else:
                        bpy.ops.mesh.tris_convert_to_quads()
                        bpy.ops.object.mode_set(mode='OBJECT')

                # *1 MOVED
                if SN.reproject and not SN.ngon:
                    bpy.ops.object.mode_set(mode='EDIT')
                    bpy.ops.mesh.tris_convert_to_quads()
                    bpy.ops.mesh.decimate(ratio=0.25)
                    bpy.ops.mesh.tris_convert_to_quads()
                    if SN.mergeDistThreshold < 0.09 and SN.mergeDistThreshold > 0.001:
                        # ESTO NO HACE FALTA YA, SÓLO SI ERA DESPUÉS DEL SOLIDIFY HACIA MEJOR RESULTADO CON DIFERENCIA
                        #bpy.ops.mesh.dissolve_limited(angle_limit=0.122173, use_dissolve_boundaries=True, delimit={'NORMAL'})
                        bpy.ops.mesh.decimate(ratio=0.1+SN.mergeDistThreshold*10)
                        bpy.ops.mesh.tris_convert_to_quads()
                    bpy.ops.object.mode_set(mode='OBJECT')

                if SN.method_type == 'SOLID':
                    solidi = o.modifiers.new(name="Solid", type='SOLIDIFY')
                    solidi.thickness = SN.thickness
                    solidi.offset = 1 # add later # 1 si activase la parte de bmesh que arregla las normales
                    solidi.thickness_clamp = 0
                    solidi.use_rim = True
                    solidi.use_rim_only = False
                    if SN.applyModifiersDirectly:
                        bpy.ops.object.modifier_apply(modifier="Solid")

                # *1 # ANTES AQUÍ PERO LOS BLOQUES FLOTABAN SI ERAN PEQUES

                    if SN.smooth:
                        co_smooth = o.modifiers.new(name="Co_Smooth", type='CORRECTIVE_SMOOTH')
                        co_smooth.iterations = SN.smoothPasses
                        co_smooth.smooth_type = 'LENGTH_WEIGHTED'
                        co_smooth.use_only_smooth = True
                        if SN.applyModifiersDirectly:
                            bpy.ops.object.modifier_apply(modifier="Co_Smooth")
                        o.data.remesh_smooth_normals = True

                if SN.mirror:
                    mirror = o.modifiers.new(name="_Mirror", type='MIRROR')
                    mirror.mirror_object = obj
                    mirror.use_mirror_vertex_groups = False
                    mirror.use_clip = True
                    if SN.applyModifiersDirectly:
                        bpy.ops.object.modifier_apply(modifier="_Mirror")

                if SN.applyModifiersDirectly:
                    SN.isCreated = False # resetear, ya se aplicó todo
                    if SN.remeshIt:
                        bpy.ops.object.mode_set(mode='SCULPT')
                        if SN.reproject:
                            bpy.ops.bas.voxel_remesh_reproject()
                        else:
                            bpy.ops.object.voxel_remesh()

    #   USING GP
        elif SN.use == 'GP':
            #actLayer = bpy.context.object.data.layers.active_note
			#gp_obj = bpy.context.object


        #   SIMPLIFY DRAW
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.gpencil.stroke_simplify(factor=0.1)

        #   CONVERT TO CURVE
            bpy.ops.gpencil.convert(type='POLY', use_normalize_weights=True, radius_multiplier=1.0, use_link_strokes=False)

        #   CONVERT TO MESH

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(state=True)
        context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='SCULPT')

        if SN.autoClear:
            bpy.ops.bas.clear_note()

        return {'FINISHED'}

class BAS_OT_sculpt_notes_apply_modifiers(Operator):
    bl_idname = "bas.sculpt_notes_apply_modifiers"
    bl_label = "Sculpt Notes: Apply Modifiers"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        act_obj = context.active_object
        SN = context.window_manager.bas_sculptnotes
        obj = SN.gp

        if not obj:
            ShowMessageBox("No recent SculptNote mesh was found", "Can't do this!" 'INFO')
            SN.isCreated = False
            SN.curve = None
            SN.curveShape = None
            SN.path_object = None
            return {'CANCELLED'}
            
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
            #bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(state=True)
            context.view_layer.objects.active = obj
            if obj != None:
                for mod in obj.modifiers:
                    bpy.ops.object.modifier_apply(modifier=mod.name)
        except:
            ShowMessageBox("No recent SculptNote mesh was found", "Can't do this!" 'INFO')
            pass
        if SN.remeshIt:
            bpy.ops.object.mode_set(mode='SCULPT')
            if SN.reproject:
                bpy.ops.bas.voxel_remesh_reproject()
                
            else:
                bpy.ops.object.voxel_remesh()
            bpy.ops.object.mode_set(mode='OBJECT')
        obj.select_set(state=False)
        act_obj.select_set(state=True)
        context.view_layer.objects.active = act_obj
        bpy.ops.object.mode_set(mode='SCULPT')

        SN.isCreated = False
        SN.gp = None
        return {'FINISHED'}

classes = (
    BAS_OT_sculpt_notes_curve_to_mesh,
    BAS_OT_sculpt_notes_Convert,
    BAS_OT_sculpt_notes_apply_modifiers
)