from .ops import (
    npy, Vector, Operator, bpy, random, ShowMessageBox, bmesh
)
import blf


########## CURVES ####################


#curvePointsX = []
#curvePointsY = []
# SAVE POINT COORDS TO LIST
#curvePointsX.append(v[0])
#curvePointsY.append(v[1])

distThreshold = 55
prev = Vector((0, 0, 0))
def editableCurve_draw_callback_px(self, context):
    try:
        if not bpy.context.space_data.overlay.show_overlays or not self.spline:
            return
    except:
        return
    #fun.Draw_Button_2D_Rectangle(context, event, None, Vector((200, 200)), 500, 500, "Hola Mundo", 24)
    #fun.Draw_2D_Button(self.button_1)
    #fun.Draw_2D_Button(self.button_2)
    n = 0
    lastPointCo = None
    penultPointCo = None
    minDist = 2000
    numPoints = len(self.spline.bezier_points)
    #self.nearPoint = -1
    #self.nearCoord = Vector((0, 0))
    #if self.spline != None:
    if numPoints > 0:
        self.snapping = False
        #k = numPoints - 1
        for point in self.spline.bezier_points:
            # OBTENEMOS LAS COORDENADAS EN PANTALLA
            v = fun.Convert_3D_spaceCoords_to_2D_screenCoords(context, point.co)
            if v != None:
                if not self.scaling and not self.tilting:
                    # CALC DIST FROM MOUSE TO EVERY SINGLE POINT
                    dist = fun.DistanceBetween(v, self.mousePos) # ya es abs !
                    if (dist < minDist):
                        # SAVE SNAP POINT
                        if self.canSnap: # Si puede snapear a otros puntos
                            if self.nearBPoint != point: # Comprobar si no es el punto ya activo
                                if abs(dist) < self.snapThreshold: # Si está dentro del rango
                                    self.snapping = True
                                    self.nearestSnapPoint = point.co # guardar referencia coordenadas
                                #else:
                                #    self.snapping = False
                        minDist = dist
                        # NOT IF IT'S DRAGGING BUT YES FOR SNAP
                        if not self.dragging: # Keep active point if you are dragging
                            # UPDATE NEAREST POINT
                            self.nearPoint = n
                            self.nearCoord = Vector((v[0], v[1]))
                            self.nearBPoint = point

                # DIBUJAMOS CADA LINEA
                if n != 0:
                    fun.Draw_2D_Line(prev, v, (.7, .1, .2, .5))
                    #if n == k:
                    #    lastPointCo = v

                # DIBUJAMOS CADA PUNTO
                fun.Draw_Text(v[0]-6, v[1]-8, "•", 24, 0, .6, .8, 1, .8)
                prev = v
                n+=1

        # DIBUJAMOS EXTRUDE POINT
        if self.extruding: # OBVIAR # realizar extrude y cerrar
            #if lastPointCo != None:
            lastPointCo = fun.Convert_3D_spaceCoords_to_2D_screenCoords(context, self.spline.bezier_points[numPoints-1].co)
            #CALCULAR PUNTO # YA NO HACE FALTA EL CALCULO QUE HACIA, CAMBIO DE FORMA
            fun.Draw_2D_Line(lastPointCo, self.mousePos, (.4, .8, .5, .5))
            #fun.Draw_2D_Point(self.extrudePoint, (.2, .75, .35, .6))
            fun.Draw_Text(self.mousePos[0]-20, self.mousePos[1]-24, "•", 70, 0, .2, .75, .35, .8)
            fun.Draw_Text(self.mousePos[0]-9, self.mousePos[1]-6, "+", 24, 0, 1, 1, 1, .8)

            fun.Draw_Text(lastPointCo[0]-9, lastPointCo[1]-13, "•", 36, 0, 1, .6, .8, .8)
            fun.Draw_2D_Circle(lastPointCo, 10, 16, (1, 1, 0, .8))
            self.active = True
            self.nearPoint = numPoints - 1

            fun.Draw_Text(200, 150,  "Left Click to confirm extrude", 18, 0, 1, 0.75, 0.5, 1)
        # MARCAMOS PUNTO ACTIVO
        elif self.scaling or self.tilting:
            # DIBUJAMOS PUNTO
            fun.Draw_Text(self.nearCoord[0]-9, self.nearCoord[1]-13, "•", 36, 0, 1, .6, .8, .8)
            fun.Draw_2D_Circle(self.nearCoord, 10, 8, (1, 1, 0, .8))
            # SCALING
            if self.scaling:
                rad = str(self.nearBPoint.radius)[0:4]
                fun.Draw_Text(self.nearCoord[0]+20, self.nearCoord[1]-8, rad, 24, 0, 1, 1, 1, .8)
            # TILTING
            if self.tilting:
                til = str(math.degrees(self.nearBPoint.tilt))[0:4]
                fun.Draw_Text(self.nearCoord[0]+20, self.nearCoord[1]-8, til, 24, 0, 1, 1, 1, .8)
            fun.Draw_Text(200, 150,  "Left Click to confirm extrude", 18, 0, 1, 0.75, 0.5, 1)
        elif (self.nearPoint != -1):
            if (minDist < distThreshold):
                self.active = True
                if self.showHandlers:
                    self.hL = fun.Convert_3D_spaceCoords_to_2D_screenCoords(context, self.nearBPoint.handle_left)
                    self.hR = fun.Convert_3D_spaceCoords_to_2D_screenCoords(context, self.nearBPoint.handle_right)
                    # DIBUJAMOS LINEAS A HANDLERS
                    fun.Draw_2D_Line(self.hL, self.nearCoord, (.8, .8, .8, .5))
                    fun.Draw_2D_Line(self.hR, self.nearCoord, (.8, .8, .8, .5))
                    # DIBUJAMOS PUNTOS HANDLERS
                    fun.Draw_Text(self.hL[0]-6, self.hL[1]-8, "•", 24, 0, 1, 1, 0, .8)
                    fun.Draw_Text(self.hR[0]-6, self.hR[1]-8, "•", 24, 0, 1, 1, 0, .8)
                # DIBUJAMOS PUNTO
                if self.dragging:
                    if self.snapping:
                        snapPoint2D = fun.Convert_3D_spaceCoords_to_2D_screenCoords(context, self.nearestSnapPoint)
                        fun.Draw_Text(snapPoint2D[0]-9, snapPoint2D[1]-13, "•", 36, 0, 1, .6, .8, .8)
                        fun.Draw_2D_Circle(snapPoint2D, 10, 16, (1, 1, 0, .8))
                    else:
                        fun.Draw_Text(self.mousePos[0]-9, self.mousePos[1]-13, "•", 36, 0, 1, .6, .8, .8)
                        fun.Draw_2D_Circle(self.mousePos, 10, 16, (1, 1, 0, .8))
                else:
                    fun.Draw_Text(self.nearCoord[0]-9, self.nearCoord[1]-13, "•", 36, 0, 1, .6, .8, .8)
                    fun.Draw_2D_Circle(self.nearCoord, 10, 16, (1, 1, 0, .8))
            else:
                self.active = False

        # DRAW3 INFO
        fun.Draw_Text(200, 100, "Ctrl: Move Point    |   Shift: Extrude  |   Alt: Show handlers", 18)
        fun.Draw_Text(200, 50,  "Ctrl + Shift: Snap  |   S: Scale        |   D: Rotate", 18)

from bpy_extras import object_utils
class BAS_OT_Convert_Curves(Operator):
    bl_idname = "bas.sculpt_notes_convert_to_curve"
    bl_label = "Convert Notes to Curves"
    bl_options = {'REGISTER', 'UNDO', 'BLOCKING'}

    def modal(self, context, event):
        if not context or context == None:
            self.old_context.space_data.draw_handler_remove(self._handle, 'WINDOW')
            del self._handle
            args = (self, context)
            self._handle = bpy.types.SpaceView3D.draw_handler_add(editableCurve_draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
            self.old_context = context
        #fun.AlignObjectToView(context.active_object)
        #if event.type in {'J'}:
        if not hasattr(self, '_handle'):
            args = (self, context)
            self._handle = bpy.types.SpaceView3D.draw_handler_add(editableCurve_draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
        if self.spline == None:
            try:
                self.spline = bpy.data.curves[context.scene.curve.name].splines[0]
            except:
                context.space_data.draw_handler_remove(self._handle, 'WINDOW')
                del self._handle
                return {'CANCELLED'}
        self.mousePos = Vector((event.mouse_region_x, event.mouse_region_y))
        #fun.Button_Events(event, self.button_1, self.mousePos, bpy.ops.object.voxel_remesh) # mousePos is optional, func will take it from event if it's none, but more convenient like this if you have multiple buttons
        #fun.Button_Events(event, self.button_2, self.mousePos, None)
        if event.type in {'C'} and event.value in {'PRESS'}:
            fun.Curve_CloseSpline(self.spline)
        if self.scaling:
            if event.type in {'ESC', 'RIGHTMOUSE', 'LEFTMOUSE'}:
                self.scaling = False
                self.scalingPoint = -1
            dist = fun.DistanceBetween(self.mousePos, self.startMousePos)
            #if dist > scaleThreshold:
            if self.mousePos[0] < self.startMousePos[0]: # MOVE LEFT
                self.nearBPoint.radius = -dist / 100
            else: # MOVE RIGHT
                self.nearBPoint.radius = dist / 100
            return {'PASS_THROUGH'}
        elif self.tilting:
            if event.type in {'ESC', 'RIGHTMOUSE', 'LEFTMOUSE'}:
                self.tilting = False
                self.nearPoint = -1
            dist = fun.DistanceBetween(self.mousePos, self.startMousePos)
            #if dist > scaleThreshold:
            if self.mousePos[0] < self.startMousePos[0]: # MOVE LEFT
                self.nearBPoint.tilt = -dist / 100
            else: # MOVE RIGHT
                self.nearBPoint.tilt = dist / 100
            return {'PASS_THROUGH'}
        elif not self.dragging and event.shift and not self.extruding:
            self.extruding = True
        elif self.extruding:
            if event.type in {'LEFTMOUSE'} and event.value in {'PRESS'}:
                self.extruding = False
                hit, newCo, normal, index, obj, matrix = fun.RaycastHit_2D_to_3D(context, self.mousePos)
                if not hit:
                    newCo = fun.Convert_2D_screenCoords_to_3D_spaceCoords(context, self.mousePos)
                #newPointCo = penultPoint
                self.spline.bezier_points.add(1)
                #self.spline = bpy.data.curves[context.scene.curve.name].splines[0]
                newLast = self.spline.bezier_points[len(self.spline.bezier_points) - 1]
                newLast.handle_left_type = self.handleType
                newLast.handle_right_type = self.handleType
                newLast.co = newCo
                self.extrudePoint = Vector((0, 0))
                self.extruding = False
            elif event.type in {'ESC', 'RIGHTMOUSE', 'MIDDLEMOUSE'}:
                self.extruding = False
            #return {'PASS_THROUGH'}
        elif  self.nearPoint != -1 and self.active: # self.nearPoint != -1
            if event.ctrl:
                self.dragging = True
                #if not self.extruding and fun.DistanceBetween(self.mousePos, self.extrudePoint) < self.extrudeThreshold:
                #    self.extruding = True
                if event.shift:
                    self.canSnap = True
                    if self.snapping:
                        if self.nearestSnapPoint != None:
                            self.nearBPoint.co = self.nearestSnapPoint
                    else:
                        # CON ESTO NOOO FUNCIONA EL SNAP CON PUNTOS ANTERIORES.... PORQUE DIABLOS? PERO NO HAY AUTO-SNAP-EXIT
                        hit, pos, normal, index, obj, matrix = fun.RaycastHit_2D_to_3D(context, self.mousePos)
                        if hit:
                            self.nearBPoint.co = pos
                else:
                    self.canSnap = False
                    #self.snapping = False
                    hit, pos, normal, index, obj, matrix = fun.RaycastHit_2D_to_3D(context, self.mousePos)
                    if hit:
                        self.nearBPoint.co = pos
                    else:
                        self.nearBPoint.co = fun.Convert_2D_screenCoords_to_3D_spaceCoords(context, self.mousePos)
            elif event.alt:
                self.showHandlers = True
                hit, pos, normal, index, obj, matrix = fun.RaycastHit_2D_to_3D(context, self.mousePos)
                if hit:
                    if fun.DistanceBetween(self.mousePos, self.hL) < fun.DistanceBetween(self.mousePos, self.hR):
                        self.nearBPoint.handle_left = pos
                    else:
                        self.nearBPoint.handle_right = pos
            elif event.type in {'S'}:
                self.scalingPoint = self.nearPoint
                self.scaling = True # Activate scaling (Radius)
                self.startMousePos = Vector((event.mouse_region_x, event.mouse_region_y))
                self.baseRadius = self.nearBPoint.radius
            elif event.type in {'D'}:
                self.tiltingPoint = self.nearPoint
                self.tilting = True # Activate scaling (Radius)
                self.startMousePos = Vector((event.mouse_region_x, event.mouse_region_y))
                self.baseTilt = self.nearBPoint.tilt
            else:
                self.dragging = False
                self.showHandlers = False
        else:
            self.scaling = False
            self.tilting = False
            self.extruding = False
        if SN.curve == None or (event.type in {'ESC', 'RIGHTMOUSE'} and event.value in {'CLICK'} and not self.extruding) or context.mode != 'SCULPT' or context.active_object == None or self.spline == None:
            try:
                context.space_data.draw_handler_remove(self._handle, 'WINDOW')
                del self._handle
            except:
                self.old_context.space_data.draw_handler_remove(self._handle, 'WINDOW')
                del self._handle
                return {'CANCELLED'}
            return {'FINISHED'}
        try:
            context.area.tag_redraw()
        except:

            pass
        return {'PASS_THROUGH'}
    '''
    def cancel(self, context):
        SN.curve = None
        SN.curveShape = None
        SN.isCreated = False
    '''
    def modal_setup(self, context):
        self.old_context = context
        #self.button_1 = fun.CreateButton_Rectangle(Vector((600, 50)), 300, 100, "Remesh", 24)
        #self.button_2 = fun.CreateButton_Circle(Vector((300, 400)), 100, 32, "Hola!", 24)
        #self.button_1 = False
        self.active = False
        self.handleType = 'AUTO'
        self.nearPoint = -1
        self.nearBPoint = None
        self.nearestSnapPoint = None
        self.extrudePoint = Vector((0, 0))
        self.showHandlers = False
        self.scaling = False
        self.tilting = False
        self.dragging = False
        self.snapping = False
        self.extruding = False
        self.hL = Vector((0, 0, 0))
        self.hR = Vector((0, 0, 0))
        self.baseRadius = 1
        self.scaleFactor = 0.1
        self.snapThreshold = 38
        self.extrudeThreshold = 40
        self.canSnap = False
        self.spline = None
        areas = {a.type:a for a in context.screen.areas}
        area = areas.get("VIEW_3D",None)
        self.view = area.spaces.active.region_3d.view_matrix

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
            # Si es tipo wrap se le quita el último trazo el cual se reserva para darle forma al wrapper
            if SN.method == 3: # WRAP
                numStrokes -= 1

        #   GET NOTES POINTS # access with index # location, pressure, strength, uv-rotation... ('foreach_get()') # add/remove point
            # notePoints[numStrokes][]
            noteObjs = []
            note_id = str(random.randint(0,500) + random.randint(0,500))
        #   FOR EACH STROKE
            # Default
            vertices = []
            edges = []
            faces = []
            #face = ()
            oldPoint = None

            meshName = "" + note_id + "_CurveStroke"
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
                numPoints = len(strPoints)
                x = 0
                for point in strPoints:
                    # first stroke and first point
                    if n == 0 and p == 0:
                        vertices.append(point.co)
                        #face = face + (p,)
                        #primVert = p
                        #primPoint = point
                        oldPoint = point
                        p += 1 # Increment for next point
                        x += 1
                    # last stroke and last point
                    elif n == numStrokes-1 and p == numPoints-1:
                        vertices.append(point.co)
                        #face = face + (p)
                        lastVert = p
                        primPoint = point
                        oldPoint = point
                        edges.append((p-1, p))
                        p += 1 # Increment for next point
                        x += 1
                    else:
                        a = npy.array((point.co[0] ,point.co[1], point.co[2]))
                        b = npy.array((oldPoint.co[0], oldPoint.co[1], oldPoint.co[2]))
                        d = npy.linalg.norm(a-b)
                        if d > SN.mergeDistThreshold:
                            vertices.append(point.co)
                            #face = face + (p,)
                            edges.append((p-1, p))
                            p += 1 # Increment for next point
                            x += 1
                            oldPoint = point

            #   UPDATE AND VALIDATE NEW MESH
            #faces.append(face)
            if SN.curve_isCyclic:
                edges.append((p-1, 0))
            mesh.from_pydata(vertices,edges,[]) # [] (empty) #   Fill the mesh with verts, edges, faces
            mesh.validate(verbose=False) # clean_customdata=True
            #mesh.remesh_voxel_size = 0.01

            ob.select_set(state=True)
            context.view_layer.objects.active = ob
            bpy.ops.object.convert(target='CURVE')
            SN.curve = context.active_object

        #   BEZIER CURVA + SIMPLIFY
            bpy.ops.object.mode_set(mode='EDIT')
            try:
                bpy.ops.curve.select_all(action='SELECT')
            except:
                if SN.method == 3:
                    ShowMessageBox("For Wrap mode you have to create the shape (last stroke) you want to use to 'wrap' the path (first strokeS)!", "Please Create a second stroke", 'ERROR')
                    bpy.ops.object.mode_set(mode='OBJECT')
                    bpy.ops.object.select_all(action='DESELECT')
                    obj.select_set(state=True)
                    context.view_layer.objects.active = obj
                    bpy.ops.object.mode_set(mode='SCULPT')
                    return {'FINISHED'}

            bpy.ops.curve.spline_type_set(type='BEZIER') # SPLINE TYPE


            #curveShape = bpy.data.curves[SN.curve.name]
            #spline = curveShape.splines[0]
            if SN.curve_simplify:
                curve = bpy.data.curves[SN.curve.name]
                spline = curve.splines[0]
                numPoints = len(spline.bezier_points)
                #print(numPoints)
                if numPoints > 180:
                    bpy.ops.curve.decimate(ratio=0.1)
                elif numPoints > 105:
                    bpy.ops.curve.decimate(ratio=0.15)
                elif numPoints > 55:
                    bpy.ops.curve.decimate(ratio=0.25)
                elif numPoints > 25:
                    bpy.ops.curve.decimate(ratio=0.4)
                elif numPoints > 12:
                    bpy.ops.curve.decimate(ratio=0.55)
                else:
                    bpy.ops.curve.decimate(ratio=0.75)
                    pass

                #bpy.ops.object.mode_set(mode='OBJECT')
                #bpy.ops.object.mode_set(mode='EDIT') # UPDATE CURVE DATA

                #curve = bpy.data.curves[context.scene.curve.name]
                #self.spline = curve.splines[0]
                #self.points = self.spline.bezier_points

                #for point in curve.splines[0].bezier_points:
                #    point.handle_left_type = 'AUTO'
                #    point.handle_right_type = 'AUTO'

            bpy.ops.curve.handle_type_set(type='AUTOMATIC') # HANDLE TYPE # ALIGNED, AUTOMATIC, VECTOR

            if SN.curve_useCurveMapForSplinePointsRadius:
                #if not SN.curve_simplify:
                #curve = bpy.data.curves[SN.curve.name]
                spline = curve.splines[0]

                numPoints = len(spline.bezier_points)

                #curveNode = CurveData('CurveData')
                #curveMap = curveNode.mapping.curves[0]


                #mapping = curveNode.mapping
                #mapping.initialize()

                #ng = bpy.data.node_groups['NodeGroup']
                #curve = ng.nodes['CurveData'].mapping.curves[0]
                #y = c.evaluate(x)

                node = bpy.data.node_groups['NodeGroup'].nodes['CurveData']
                node.mapping.update()
                curveMap = node.mapping.curves[3]

                '''
                for point in curveMap.points:
                    print(point.location)

                if SN.method == 3:
                    mul = SN.radiusMultiplier
                else:
                    mul = 1
                '''
                n = 0
                for point in spline.bezier_points:
                    x = n/numPoints
                    point.radius = curveMap.evaluate(x)# * mul
                    n += 1

                    #print(x)
                    #print(curveMap.evaluate(x))

            bpy.ops.object.mode_set(mode='OBJECT')
        #

            ob.select_set(state=False)

            SN.curveShape_pivot_mode = 'CENTER'
            SN.curveShape_pivot_index = 0
            SN.curveShape_numNodes = 0

            if SN.method == 3: # 3: WRAP
                stroke = noteFrame.strokes[len(noteStrokes)-1]
                # Default
                vertices = []
                edges = []
                faces = []
                face = ()
                oldPoint = None
                # Create next mesh for next stroke
                meshName = "" + note_id + "_CurveShape"
                mesh = bpy.data.meshes.new(meshName)   # create a new mesh
                ob = bpy.data.objects.new(meshName, mesh)      # create an object with that mesh
                ob.location = Vector((0,0,0)) #by.context.scene.cursor_location   # position object at 3d-cursor
                # Link light object to the active collection of current view layer,
                # so that it'll appear in the current scene.
                context.view_layer.active_layer_collection.collection.objects.link(ob)
                #   FOR EACH POINT IN THE ACTUAL STROKE
                strPoints = stroke.points
                numPoints = len(strPoints)
                p = 0 # RESET FOR NEXT STROKE
                for point in strPoints:
                    # notePoints[numStrokes][p] = point
                    if p == 0:
                        vertices.append(point.co)
                        #face = face + (p,)
                        primVert = p
                        oldPoint = point
                        p += 1 # Increment for next point
                    else:
                        a = npy.array((point.co[0] ,point.co[1], point.co[2]))
                        b = npy.array((oldPoint.co[0], oldPoint.co[1], oldPoint.co[2]))
                        d = npy.linalg.norm(a-b)
                        if d > SN.mergeDistThreshold:
                            vertices.append(point.co)
                            #face = face + (p,)
                            edges.append((p-1, p))
                            p += 1 # Increment for next point
                            oldPoint = point
                #   UPDATE AND VALIDATE NEW MESH
                #faces.append(face)
                edges.append((p-1, 0))
                mesh.from_pydata(vertices,edges,[]) # [] (empty) #   Fill the mesh with verts, edges, faces
                mesh.validate(verbose=True) # clean_customdata=True

                ob.select_set(state=True)
                context.view_layer.objects.active = ob

                bpy.ops.object.convert(target='CURVE')

                bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')

                SN.curveShape = context.active_object

                curve = bpy.data.curves[SN.curve.name]
                curveShape = bpy.data.curves[SN.curveShape.name]
                curve.bevel_object = SN.curveShape

            #   BEZIER CURVA + SIMPLIFY
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.curve.select_all(action='SELECT')
                bpy.ops.curve.spline_type_set(type='BEZIER')

                #curveShape = bpy.data.curves[SN.curve.name]
                #spline = curveShape.splines[0]

                if SN.curve_simplify:
                    curveShape = bpy.data.curves[SN.curveShape.name]
                    spline = curveShape.splines[0]
                    numPoints = len(spline.bezier_points)
                    if numPoints > 180:
                        bpy.ops.curve.decimate(ratio=0.1)
                    elif numPoints > 105:
                        bpy.ops.curve.decimate(ratio=0.15)
                    elif numPoints > 55:
                        bpy.ops.curve.decimate(ratio=0.25)
                    elif numPoints > 25:
                        bpy.ops.curve.decimate(ratio=0.45)
                    elif numPoints > 12:
                        bpy.ops.curve.decimate(ratio=0.80)
                    else:
                        pass

                SN.curveShape_pivot_index = 0
                SN.curveShape_numNodes = len(curveShape.splines[0].bezier_points) - 1 # p - 1 # 0 in count

                bpy.ops.object.mode_set(mode='OBJECT')
            #
            elif SN.method == 5: # PATH
                SetPathWithObject(self, context)
            else:
                curve.bevel_depth = 1

            #bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(state=True)
            context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='SCULPT')

            SN.isCreated = True

            if SN.autoClear:
                bpy.ops.bas.clear_note()

        if SN.curve_postEdit:
            self.modal_setup(context)
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}

        return {'FINISHED'}


# PATH

def SetPathWithObject(self, context):
    SN = context.window_manager.bas_sculptnotes
    bpy.ops.object.select_all(action='DESELECT')
    # Seleccionar la curva y hacer activa
    curvePath = SN.curve
    curvePath.select_set(state=True)
    # y mover el cursor a su origen
    bpy.ops.view3d.snap_cursor_to_selected()
    curvePath.select_set(state=False)
    # Seleccionar el objeto
    objPath = SN.path_object
    objPath.select_set(state=True)
    # aplicar su rot y scale
    context.view_layer.objects.active = objPath
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    # Crear una copia?
    if SN.path_object_makeCopy:
        bpy.ops.object.duplicate_move()
        # Ocultar Objeto Original
        objPath.hide_set(True)
        # Cogemos la copia y Guardar referencia del objeto copia en la scene
        SN.path_object = context.active_object
        objPath = SN.path_object
    # Poner pivote en el centro?
    if SN.path_object_pivotToCenter:
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS')
    # bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    # bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME')
    # Mover objeto al 3d cursor
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    # Crear modificar Array con fit curve -> curvePath && relOffset X
    array = objPath.modifiers.new(name="_Array", type='ARRAY')
    array.fit_type = 'FIT_CURVE'
    array.curve = curvePath
    array.use_constant_offset = True
    array.use_relative_offset = False
    array.constant_offset_displace[0] = 0.1
    array.constant_offset_displace[1] = 0
    array.constant_offset_displace[2] = 0
    # bpy.ops.object.modifier_apply(modifier="_Array")
    # Crear modificador Curve / obj -> curvePath / Axis = Z
    path = objPath.modifiers.new(name="_Path", type='CURVE')
    path.object = curvePath
    path.deform_axis = 'POS_X'
    # bpy.ops.object.modifier_apply(modifier="_Path")

# STRIPES
#Calculate curve length
#curve = bpy.data.objects['BezierCurve']
#curveLength = sum(s.calc_length() for s in curve.evaluated_get(depsgraph).data.splines)

# CALC CURVE LENGTH, to know how much quads are going to be created
# Use thickness of gp for size of quads and for distance threshold when creating curve from stroke
# convert to curve
# extrude by thickness
# convert to mesh

def distance(x1,y1,x2,y2):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist

def draw_callback_px(self, context):

    #bgl.glEnable(bgl.GL_BLEND)
    SN = context.window_manager.bas_sculptnotes
    if self.start:
        value = str(self.solid.thickness)[0:4]
        start = "Thickness :  "
        end = " m"
    else:
        value = str(self.bevel.width)[0:4]
        start = "Bevel Width :  "
        end = " m"

    text = start + value + end

    # ...api_current/bpy.types.Area.html?highlight=bpy.types.area
    header_height = context.area.regions[0].height # 26px
    npanel_width = context.area.regions[1].width
    transorm_panel_width = context.area.regions[3].width

    width = context.area.width - npanel_width - transorm_panel_width
    height = context.area.height + header_height


    # draw text

    font_id = 0  # XXX, need to find out how best to get this.
    #bgl.glColor(*(1.0, 1.0, 1.0, 1))
    blf.size(font_id, 32, 72)
    blf.color(font_id, 1, 1, 1, 1)
    dim_x = blf.dimensions(font_id, text)[0]
    dim_y = blf.dimensions(font_id, text)[1]
    #blf.position(font_id, width/2-dim_x, height/2-dim_y, 0)
    blf.position(font_id, width/4+dim_x, height/6-dim_y, 0)
    blf.draw(font_id, text)

    text = "Use CTRL + MouseWheel"
    blf.size(font_id, 20, 72)
    blf.color(font_id, .8, .7, .4, 1)
    blf.position(font_id, width/4+dim_x, height/6+dim_y, 0)
    blf.draw(font_id, text)

    if self.start and SN.strips_makeBevel:
        text = "LMB -> Confirm and Edit Bevel / RMB -> Confirm and Finish"
    else:
        text = "LMB/RMB -> Confirm and Finish"
    blf.size(font_id, 16, 72)
    blf.color(font_id, .5, .9, .6, 1)
    blf.position(font_id, width/4+dim_x, height/6-dim_y*3, 0)
    blf.draw(font_id, text)
    # restore opengl defaults
    #bgl.glLineWidth(1)
    #bgl.glDisable(bgl.GL_BLEND)
    #bgl.glColor(0.0, 0.0, 0.0, 1.0)

class BAS_OT_Convert_Strips(Operator):
    bl_idname = "bas.sculpt_notes_convert_to_strip"
    bl_label = "Convert Notes to Strips"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        # SETUP
        self.start = True
        self.end = False
        self.sensibility = 30
        self.thickness = 0.01
        self.width = 0.01
        self.lastX = event.mouse_region_x
        self.lastY = event.mouse_region_y
        self.noteData = context.scene.grease_pencil
        if not self.stroke2Mesh(context):
            return {'FINISHED'}
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if self.end or event.type in {'RIGHTMOUSE', 'ESC'}:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            del self._handle
            if self.start:
                bpy.ops.object.modifier_apply(modifier="Solid")
            else:
                bpy.ops.object.modifier_apply(modifier="Solid")
                bpy.ops.object.modifier_apply(modifier="Bevel")
            self.returnToSculpt(context, self.sculptObj)
            return {'FINISHED'}
        SN = context.window_manager.bas_sculptnotes
        #self.cur = (event.mouse_region_x, event.mouse_region_y)
        #diff = (self.cur[0] - self.prev[0], self.cur[1] - self.prev[1])
        if self.start:
            if event.type in {'LEFTMOUSE'} and event.value in {'CLICK'}:
                self.start = False
                self.bevel = self.strip.modifiers.new(name="Bevel", type='BEVEL')
                self.bevel.width = 0
                self.bevel.segments = 0
            else:
                if not hasattr(self, '_handle'):
                    # the arguments we pass the the callback
                    args = (self, context)
                    # Add the region OpenGL drawing callback
                    # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
                    self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
                if event.type in {'WHEELUPMOUSE'} and event.value in {'PRESS'} and event.ctrl:
                        #print("MÁS")
                        self.solid.thickness += self.thickness
                elif event.type in {'WHEELDOWNMOUSE'} and event.value in {'PRESS'} and event.ctrl:
                    #print("MENOS")
                    self.solid.thickness -= self.thickness
                '''
                mX = event.mouse_region_x
                mY = event.mouse_region_y
                if distance(mX, mY, self.lastX, self.lastY) > self.sensibility:
                    if mY > self.lastY: # hacia arriba # CAMBIAR POR CENTRO DE REGION
                        self.solid.thickness += self.thickness
                    elif mY < self.lastY: # hacia abajo # CAMBIAR POR CENTRO DE REGION
                        self.solid.thickness -= self.thickness
                    self.lastX = mX
                    self.lastY = mY
                '''
        elif SN.strips_makeBevel:
            if event.type in {'LEFTMOUSE'} and event.value in {'CLICK'}:
                self.end = True
            else:
                if event.type in {'WHEELUPMOUSE'} and event.value in {'PRESS'} and event.ctrl:
                    if self.bevel.width < 0.03:
                        self.bevel.width += self.width
                        self.bevel.segments += 1
                elif event.type in {'WHEELDOWNMOUSE'} and event.value in {'PRESS'} and event.ctrl:
                    if self.bevel.width > 0:
                        self.bevel.width -= self.width
                        self.bevel.segments -= 1
                '''
                mX = event.mouse_region_x
                mY = event.mouse_region_y
                if distance(mX, mY, self.lastX, self.lastY) > self.sensibility:
                    if mX > self.lastX: # hacia der # CAMBIAR POR CENTRO DE REGION
                        self.bevel.width += self.width
                    elif mX < self.lastX: # hacia izq # CAMBIAR POR CENTRO DE REGION
                        self.bevel.width -= self.width
                    self.lastX = mX
                    self.lastY = mY
                '''
        else:
            self.end = True
        #self.xpos = event.mouse_region_x
        #self.ypos = event.mouse_region_y
        return {'PASS_THROUGH'}

    def stroke2Mesh(self, context):
        self.sculptObj = context.active_object
        noteStrokes = self.noteData.layers.active.active_frame.strokes
        if not noteStrokes:
            return False
        strPoints = noteStrokes[0].points
        numPoints = len(strPoints) - 1
        if numPoints < 5 and not self.poly:
            bpy.ops.bas.clear_note()
            return False
        SN = context.window_manager.bas_sculptnotes
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        note_id = str(random.randint(0,500) + random.randint(0,500))
        meshName = "" + note_id + "_QuadStrip"
        mesh = bpy.data.meshes.new(meshName)   # create a new mesh
        self.strip = bpy.data.objects.new(meshName, mesh)
        self.strip.location = Vector((0,0,0))
        context.view_layer.active_layer_collection.collection.objects.link(self.strip)
        vertices = []
        edges = []
        oldPoint = None
        p = 0
        threshold = SN.mergeDistThreshold
        #maxDist = self.noteData.layers.active.thickness if SN.strips_thicknessForSize == True else threshold
        maxDist = threshold
        for point in strPoints:
            if p == 0:
                vertices.append(point.co)
                p += 1
                oldPoint = point
            else:
                a = npy.array((point.co[0] ,point.co[1], point.co[2]))
                b = npy.array((oldPoint.co[0], oldPoint.co[1], oldPoint.co[2]))
                d = npy.linalg.norm(a-b)
                if d >= maxDist:
                    vertices.append(point.co)
                    edges.append((p-1, p))
                    p += 1
                    oldPoint = point
        #
        mesh.from_pydata(vertices, edges, [])
        mesh.validate(verbose=False)
        mesh.remesh_voxel_size = 0.01

        self.sculptObj.select_set(state=False)
        self.strip.select_set(state=True)
        context.view_layer.objects.active = self.strip

        bpy.ops.object.convert(target='CURVE')
        #bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN')

        #SN.gp = self.strip
        curve = bpy.data.curves[self.strip.name]

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.curve.select_all(action='SELECT')
        bpy.ops.curve.spline_type_set(type='BEZIER')
        bpy.ops.transform.tilt(value=1.570796)

        #bpy.ops.transform.rotate(value=1.570796, orient_axis='X', orient_type='NORMAL') #1.570796

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
        curve.extrude = maxDist / 2
        bpy.ops.object.convert(target='MESH')

        if SN.mirror:
            self.mirror = self.strip.modifiers.new(name="Mirror", type='MIRROR')
            if SN.decimation_symmetry_axis == 'X':
                n = 0
            elif SN.decimation_symmetry_axis == 'Y':
                n = 1
            else:
                n = 2
            self.mirror.use_axis[n]
            self.mirror.use_clip = False
            self.mirror.mirror_object = self.sculptObj

        if SN.strips_makeSolid:
            self.solid = self.strip.modifiers.new(name="Solid", type='SOLIDIFY')
            self.solid.thickness = maxDist #0.03
            self.solid.offset = 1 # add later
            self.solid.thickness_clamp = 0
            self.solid.use_rim = True
            self.solid.use_rim_only = True
        else:
            self.sculptObj.select_set(state=True)
            context.view_layer.objects.active = self.sculptObj
            bpy.ops.object.mode_set(mode='SCULPT')
            if SN.autoClear:
                bpy.ops.bas.clear_note()
            #return {'FINISHED'}
        return True

    def returnToSculpt(self, context, obj):
        SN = context.window_manager.bas_sculptnotes
        '''
        print("END")
        obj.select_set(state=False)
        self.strip.select_set(state=True)
        context.view_layer.objects.active = self.strip

        if SN.remeshIt:
            self.solid.use_rim_only = False
            if SN.mirror:

        bpy.ops.object.modifier_apply(modifier="Solid")
        bpy.ops.object.modifier_apply(modifier="Bevel")

        if SN.remeshIt:
            self.solid.use_rim_only = False
            if SN.mirror:
                self.mirror.use_mirror_merge = False
                bpy.ops.object.modifier_apply(modifier="Mirror")

        for mod in self.strip.modifiers:
            try:
                bpy.ops.object.modifier_apply(modifier=mod.name)
            except:
                pass

        if SN.remeshIt:
            bpy.ops.object.mode_set(mode='SCULPT')
            bpy.ops.object.voxel_remesh()
            print("remesh")
            bpy.ops.object.mode_set(mode='OBJECT')
        '''
        self.strip.select_set(state=False)
        obj.select_set(state=True)
        context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='SCULPT')
        if SN.autoClear:
            bpy.ops.bas.clear_note()

curve_classes = (
    BAS_OT_Convert_Curves,
    BAS_OT_Convert_Strips
)
