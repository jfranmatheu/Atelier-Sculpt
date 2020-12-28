


def draw_callback_px(self, context):
    #bgl.glEnable(bgl.GL_BLEND)

    if self.start:
        value = str(self.solid.thickness)[0:4]
        start = "Thickness :  "
        end = " m"
    else:
        value = str(self.bevel.width)[0:4]
        start = "Bevel Width :  "
        end = " m"

    text = start + value + end

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

    if self.start and context.scene.sculptNotes_strips_makeBevel:
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
