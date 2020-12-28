import bpy


def update_sculptNotes_curveShape(self, context):
    try:
        if self.curveShape != None:
            self.curveShape_numNodes = len(bpy.data.curves[self.curveShape.name].splines[0].bezier_points) - 1  # se da por hecho de que la curveShape sólo tiene una spline y es bezier
            self.curveShape_pivot_index = 0 # se resetea el index como precaución
            if self.curveShape_numNodes == 0: # si fuese 0 probar con puntos normales en vez de bezier por si el tipo de spline es diferente
                self.curveShape_numNodes = len(bpy.data.curves[self.curveShape.name].splines[0].points) - 1 # 0 in count
    except:
        pass
    return

def update_sculptNotes_solid_thickness(self, context):
    try:
        obj = self.gp
        if obj == None:
            return
        else:
           obj.modifiers["Solid"].thickness = self.thickness
    except:
        return
'''
def update_sculptNotes_curve_radius(self, context):
    try:
        curve = bpy.data.curves[scn.sculptNotes_curve.name]
        curveShape = bpy.data.curves[scn.sculptNotes_curveShape.name]
        curve.bevel_object = curveShape
        curveObj = context.scene.sculptNotes_curveShape
        if curveObj == None:
            curveShapeObj = context.scn.sculptNotes_gp
            if curveShapeObj == None:
                return
            else:
                curveShape.bevel_depth = self.sculptNotes_radius
        else:
            r = self.sculptNotes_radius
            curveObj.scale = (r, r, r)
    except:
        return
'''
def update_sculptNotes_ngon(self, context):
    if self.ngon:
        self.reproject = False
    return

def update_sculptNotes_reproject(self, context):
    if self.reproject:
        self.ngon = False
    return

def update_sculptNotes_method(self, context):
    #   FILTER OF OPTIONS
    if self.method_type == 'SOLID':
        self.canJoinStrokes = True
        self.canMergeStrokes = True
        self.canReproject = True
        self.canNgon = True
        self.canMirror = True
        self.canSmooth = True
        self.canRemesh = True
        self.method = 1
    elif self.method_type == 'FLAT':
        self.canJoinStrokes = True
        self.canMergeStrokes = True
        self.canReproject = False
        self.canNgon = True
        self.canMirror = False
        self.canSmooth = False
        self.canRemesh = False
        self.method = 2
    elif self.method_type == 'WRAP':
        self.canJoinStrokes = False
        self.canMergeStrokes = False
        self.canReproject = False
        self.canNgon = False
        self.canMirror = True
        self.canSmooth = False
        self.canRemesh = True
        self.method = 3
    elif self.method_type == 'CURVE':
        self.canJoinStrokes = False
        self.canMergeStrokes = False
        self.canReproject = False
        self.canNgon = False
        self.canMirror = True
        self.canSmooth = False
        self.canRemesh = True
        self.method = 4
    elif self.method_type == 'PATH':
        self.canJoinStrokes = False
        self.canMergeStrokes = False
        self.canReproject = False
        self.canNgon = False
        self.canMirror = True
        self.canSmooth = False
        self.canRemesh = True
        self.method = 5
    elif self.method_type == 'STRIPS':
        self.canJoinStrokes = False
        self.canMergeStrokes = False
        self.canReproject = False
        self.canNgon = False
        self.canMirror = False
        self.canSmooth = False
        self.canRemesh = False
        self.method = 6
    else:
        self.canJoinStrokes = False
        self.canMergeStrokes = False
        self.canReproject = False
        self.canNgon = False
        self.canMirror = True
        self.canSmooth = False
        self.canRemesh = True
        self.method = 0
    return

def update_sculptNotes_curve_curveMap(self, context):
    if self.curve_useCurveMapForSplinePointsRadius:
        self.showCurveMapEditor = True
        if not self.curve_curveMap_isCreated:
            bpy.ops.bas.sculpt_notes_create_curve_map()
    else:
        self.showCurveMapEditor = False
    return

def update_sculptNotes_curveShape_pivot_mode(self, context):
    obj = context.active_object
    bpy.ops.object.mode_set(mode='OBJECT')
    curveShape = self.curveShape
    if curveShape == None:
        curveShape = bpy.data.curves[self.curve.name].bevel_object
        if curveShape == None:
            try:
                bpy.ops.object.mode_set(mode='SCULPT')
            except:
                pass
            return
        else:
            if self.curveShape_numNodes <= 1:
                numPoints = len(bpy.data.curves[curveShape.name].splines[0].bezier_points)
                if numPoints == 0:
                    numPoints = len(bpy.data.curves[curveShape.name].splines[0].points)
                self.curveShape_numNodes = numPoints - 1
            pass
    curveShape.select_set(state=True)
    obj.select_set(state=False)
    context.view_layer.objects.active = curveShape
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    #bpy.ops.object.transform_apply(location=True, rotation=True, scale=True) # TEST
    #bpy.ops.view3d.snap_selected_to_grid()
    if self.curveShape_pivot_mode == 'CENTER':
        pass
    else:
        # ref. a cursor y pos.
        cursor = context.scene.cursor
        prevLoc = cursor.location
        # ref. a curveShape y sus puntos
        spline = bpy.data.curves[curveShape.name].splines[0]
        if spline.type == 'BEZIER':
            points = spline.bezier_points
        else:
            points = spline.points
        # dependiendo del modo posicionar el cursor
        if self.curveShape_pivot_mode == 'FIRST':
            cursor.location = points[0].co
        elif self.curveShape_pivot_mode == 'LAST':
            cursor.location = points[self.curveShape_numNodes].co
        elif self.curveShape_pivot_mode == 'NODE':
            p = points[self.curveShape_pivot_index].co
            cursor.location = (p[0],p[1],p[2])
            #cursor.location = points[self.curveShape_pivot_index].co
        elif self.curveShape_pivot_mode == 'AVERAGE':
            cursor.location = (points[self.curveShape_numNodes].co - points[0].co) / 2
        #aplicar el pivote al cursor
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        # volver cursor a su estado anterior
        cursor.location = prevLoc
    curveShape.select_set(state=False)
    obj.select_set(state=True)
    context.view_layer.objects.active = obj
    try:
        bpy.ops.object.mode_set(mode='SCULPT')
    except:
        pass
    return

def update_sculptNotes_curveShape_pivot_index(self, context):
    obj = context.active_object
    bpy.ops.object.mode_set(mode='OBJECT')
    curveShape = self.curveShape

    if curveShape == None:
        curveShape = bpy.data.curves[self.curve.name].bevel_object
        if curveShape == None:
            try:
                bpy.ops.object.mode_set(mode='SCULPT')
            except:
                pass
            return
        else:
            if self.curveShape_numNodes <= 1:
                numPoints = len(bpy.data.curves[curveShape.name].splines[0].bezier_points)
                if numPoints == 0:
                    numPoints = len(bpy.data.curves[curveShape.name].splines[0].points)
                self.curveShape_numNodes = numPoints - 1
            pass
    curveShape.select_set(state=True)
    obj.select_set(state=False)
    context.view_layer.objects.active = curveShape   
    
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    #bpy.ops.object.transform_apply(location=True, rotation=True, scale=True) # TEST
    #bpy.ops.view3d.snap_selected_to_grid()

    # ref. a cursor y pos.
    cursor = context.scene.cursor
    prevLoc = cursor.location
    # ref. a curveShape y sus puntos
    spline = bpy.data.curves[curveShape.name].splines[0]
    if spline.type == 'BEZIER':
        points = spline.bezier_points
    else:
        points = spline.points

    if self.curveShape_pivot_index > self.curveShape_numNodes:
        self.curveShape_pivot_index = 0
    elif self.curveShape_pivot_index < 0:
        self.curveShape_pivot_index = self.curveShape_numNodes
    p = points[self.curveShape_pivot_index].co
    cursor.location = (p[0],p[1],p[2])
    
    # aplicar el pivote al cursor
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    # volver cursor a su estado anterior
    cursor.location = prevLoc
    
    curveShape.select_set(state=False)
    obj.select_set(state=True)
    context.view_layer.objects.active = obj
    try:
        bpy.ops.object.mode_set(mode='SCULPT')
    except:
        pass
    return

def update_sculptNotes_path_object(self, context):
    if self.isCreated:
        if self.sculptNotes_path_object == None:
            self.isCreated = False
    return
