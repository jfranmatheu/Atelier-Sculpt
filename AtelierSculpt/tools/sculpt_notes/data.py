from bpy.types import PropertyGroup
from bpy.props import *
from . prop_fun import *


class SculptNotesPG(PropertyGroup):
    # SCULPT NOTES
    curve_postEdit : BoolProperty(default=False, name="Post-Edition of curves in Sculpt Mode", description="You'll be able to edit result curve in Sculpt Mode. Ctrl to Move. Shift for extrude. S for Scale. D for Rotate. Ctrl+Shift for snap. Alt to show handles.")
    live : BoolProperty(default=False, name="Live sculpting", description="Live sculpting. ONLY with annotations")
    autoClear : BoolProperty(default=True, name="Auto-Clear after convert", description="Clear all made notes automatically after converting them")
    use : EnumProperty (
        items=(
            ('NOTES', "Annotations", "Use annotations to sculpt"),
            ('GP', "Grease Pencil", "Use GP to sculpt")
        ),
        default='NOTES', name="Annotations or Grease Pencil?", description="",
        #update=update_sculptNotes_use
    )
    notes_symmetry_x : BoolProperty(default=False, name="Use X Symmetry for annotations?")
    thickness : FloatProperty(name="Thickness", min=0.001, max=1, default=.1, subtype='DISTANCE', description="Change thickness of sculpted notes", update=update_sculptNotes_solid_thickness) 
    #sculptNotes_radius : FloatProperty(name="Radius", max=10, min=0.001, default=.05, subtype='DISTANCE', description="Change Radious for the path of sculpted notes", update=update_sculptNotes_curve_radius)
    gp : PointerProperty(type=bpy.types.Object, name="Pointer to GP Object")
    curve : PointerProperty(type=bpy.types.Object, name="Pointer to GP Curve")
    path_object : PointerProperty(type=bpy.types.Object, name="Object To Follow The Path", update=update_sculptNotes_path_object)
    path_object_makeCopy : BoolProperty(default=True, name="Make a Copy", description="Make a copy from the original object. Do it if you're aware of loosing that object")
    path_object_pivotToCenter : BoolProperty(default=False, name="Obj pivot to its center", description="Force pivot to be in the center of the object")
    curve_curveMap_isCreated : BoolProperty(default=False, name="CurveMap is created?")
    mergeDistThreshold : FloatProperty(name="Distance Threshold", default=.06, min=0.0001, max=0.5, subtype='DISTANCE', description="Minimum distance between vertices. This will reduce greatly the ammount of vertices / nodes")
    isCreated : BoolProperty(default=False, name="A note is created?")
    applyModifiersDirectly : BoolProperty(default=True, name="Apply modifiers directly")
    joinStrokes : BoolProperty(default=True, name="Join strokes", description="Join meshes extracted from different strokes or keep them separated in different objects")
    mergeStrokes : BoolProperty(default=False, name="Merge strokes into One?")
    ngon : BoolProperty(default=False, name="N-gons?", description="Use n-gon to fill the face of the mesh?", update=update_sculptNotes_ngon)
    reproject : BoolProperty(default=False, name="Re-project?", description="You may get better results, specially for curved surfaces, a little slower", update=update_sculptNotes_reproject)
    smooth : BoolProperty(default=False, name="Post-Smooth")
    smoothPasses : IntProperty(min=1, max=10, default=2, name="Smooth Passes", description="Number of iterations for smooth")
    remeshIt : BoolProperty(default=True, name="Post-Remesh")
    mirror : BoolProperty(default=False, name="Post-Mirror")
    strips_thicknessForSize : BoolProperty(default=False, name="Use Notes Thickness For Quad Size", description="Instead of the distance threshold")
    strips_makeSolid : BoolProperty(default=True, name="Make Solid")
    strips_makeBevel : BoolProperty(default=True, name="Make Bevel")
    curveShape : PointerProperty(type=bpy.types.Object, name="Curve Shape for Wrapper", update=update_sculptNotes_curveShape)
    curve_isCyclic : BoolProperty(default=False, name="Is Cyclic?", description="Make a cyclic curve")
    curve_simplify : BoolProperty(default=True, name="Simplify?", description="Simplify curve to make it with less points")
    curve_useCurveMapForSplinePointsRadius : BoolProperty(default=False, name="Use CurveMap for Radius", description="Use Curve Map to 'map' the radius of the stroke over it's length", update=update_sculptNotes_curve_curveMap)
    #sculptNotes_radiusMultiplier : FloatProperty(name="Radius Multiplier", max=5, min=0.1, default=1, subtype='FACTOR', description="Factor to multiply radius made with curve map", update=update_sculptNotes_curve_radius)
    method_type : EnumProperty (
        items=(
            ('SOLID', "Solid", "Make a solid block from the draw"),
            ('WRAP', "Wrap", "The firsts strokes are for the path, the last stroke in for the shape to wrap the path!"),
            ('FLAT', "Flat", "Just flat mesh. Take care is n-gon!"),
            ('CURVE', "Curve", "Make a curve with a stroke or various strokes! Use the bevel curve you want and tweak it in Post-Edition without exiting Sculpt-Mode!"),
            ('STRIPS', "Strips", "Make perfect quad strips with size based on the threshold or the thickness of the annotation tool!"),
            ('PATH', "Path", "Draw shapes and save them as curves to use them later! Make your own shape library!")
        ),
        default='SOLID', name="Which mode do you want to use?", description="",
        update=update_sculptNotes_method
    )
    curveShape_pivot_mode : EnumProperty (
        items=(
            ('CENTER', "Center", "Pivot at the center of the curve"),
            ('FISRT', "Start", "Pivot at the start point of the curve"),
            ('LAST', "End", "Pivot at the end point of the curve"),
            ('AVERAGE', "Average", "Curve at average point between start and end points"),
            ('NODE', "Per Node", "Pivot at specific curve point")
        ),
        default='CENTER', name="Pivot location", description="Where to align the pivot of the curve?",
        update=update_sculptNotes_curveShape_pivot_mode
    )
    canJoinStrokes : BoolProperty(default=True)
    canMergeStrokes : BoolProperty(default=True)
    canReproject : BoolProperty(default=True)
    canNgon : BoolProperty(default=True)
    canMirror : BoolProperty(default=True)
    canSmooth : BoolProperty(default=True)
    canRemesh : BoolProperty(default=True)
    method : IntProperty(default=1)
    #points : bpy.props.FloatVectorProperty(size=5, default=[0,0,0,0,0])

    showCurveMapEditor : BoolProperty(default=False, name="Show Curve Map Editor")
    curveShape_numNodes : IntProperty(min=1, name="Nodes of the Shape", description="Number of Nodes of the Curve Shape")
    curveShape_pivot_index : IntProperty(min=-1, name="Pivot Index", description="Index of the node used as pivot point", update=update_sculptNotes_curveShape_pivot_index)
