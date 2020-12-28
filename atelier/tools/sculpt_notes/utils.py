import bpy
from bpy.types import Operator
from ...utils.others import ShowMessageBox


class BAS_OT_clear_note(Operator):
    bl_idname = "bas.clear_note"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Clear Notes"

    def execute(self, context):
        try:
            note_data = context.scene.grease_pencil
            frame = note_data.layers.active.active_frame
            if len(frame.strokes) < 1:
                ShowMessageBox("No notes to clear", "Can't do this!", 'INFO')
            else:
                frame.clear()
        except:
            ShowMessageBox("No notes to clear", "Can't do this!", 'INFO')
        return {'FINISHED'}

class BAS_OT_undo_note(Operator):
    bl_idname = "bas.undo_note"
    bl_description = "Undo Note"
    bl_label = ""
    bl_options = {'REGISTER', 'UNDO'}

    def error(self, context):
        self.layout.label(text="No strokes to undo !")

    def execute(self, context):
        note_data = context.scene.grease_pencil
        frame = note_data.layers.active.active_frame
        if len(frame.strokes) < 1:
            bpy.context.window_manager.popup_menu(BAS_OT_undo_note.error, title = "Can't do this !", icon = 'INFO')
        else:
            stroke_count = len(frame.strokes)
            last_stroke = frame.strokes[stroke_count-1]
            frame.strokes.remove(last_stroke)
        return {'FINISHED'}

class BAS_OT_sculpt_notes_remove_mesh(Operator):
    bl_idname = "bas.sculpt_notes_remove_mesh"
    bl_label = "Sculpt Notes: Remove Mesh"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):
        SN = context.window_manager.bas_sculptnotes
        try:
            bpy.data.objects.remove(SN.sculptNotes_gp)
        except:
            ShowMessageBox("No recent SculptNote mesh was found", "Can't do this!" 'INFO')
            pass
        SN.sculptNotes_isCreated = False
        return {'FINISHED'}

class BAS_OT_sculpt_notes_remove_curve(Operator):
    bl_idname = "bas.sculpt_notes_remove_curve"
    bl_label = "Sculpt Notes: Remove Curve"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):
        SN = context.window_manager.bas_sculptnotes
        try:
            bpy.data.objects.remove(SN.sculptNotes_curve)
        except:
            ShowMessageBox("No recent SculptNote curve 'path' was found", "Can't do this!" 'INFO')
            pass
        if SN.method == 3: # WRAP
            try:
                bpy.data.objects.remove(SN.sculptNotes_curveShape)
            except:
                ShowMessageBox("No recent SculptNote curve 'shape' was found", "Can't do this!" 'INFO')
        elif SN.method == 5: # PATH
            try:
                bpy.data.objects.remove(SN.sculptNotes_path_object)
            except:
                ShowMessageBox("No recent 'path' object was found", "Can't do this!" 'INFO')
        SN.sculptNotes_isCreated = False
        return {'FINISHED'}

class BAS_OT_sculpt_notes_cancel(Operator):
    bl_idname = "bas.sculpt_notes_cancel"
    bl_label = "Sculpt Notes: Cancel Operation"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):
        SN = context.window_manager.bas_sculptnotes
        SN.sculptNotes_gp = None
        SN.sculptNotes_curve = None
        SN.sculptNotes_curveShape = None
        SN.sculptNotes_isCreated = False
        SN.sculptNotes_path_object = None
        return {'FINISHED'}

def SN_NodeTree():
    if 'SN_NodeGroup' not in bpy.data.node_groups:
        ng = bpy.data.node_groups.new('SN_NodeGroup', 'ShaderNodeTree')
        ng.fake_user = True
    return bpy.data.node_groups['SN_NodeGroup'].nodes

curve_node_mapping = {}
def SN_CurveData(curve_name):
    if curve_name not in curve_node_mapping:
        cn = SN_NodeTree().new('ShaderNodeRGBCurve')
        cn.mapping.initialize()
        curve_node_mapping[curve_name] = cn.name
    return SN_NodeTree()[curve_node_mapping[curve_name]]

class BAS_OT_sculpt_notes_create_curve_map(Operator):
    bl_idname = "bas.sculpt_notes_create_curve_map"
    bl_label = "Sculpt Notes: Create Curve Map"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):
        if 'SN_NodeGroup' not in bpy.data.node_groups:
            nodeGroup = bpy.data.node_groups.new('SN_NodeGroup', 'ShaderNodeTree')
            #nodeGroup.fake_user = True
            curveNode = nodeGroup.nodes.new('ShaderNodeRGBCurve')
            curveNode.name = 'SN_CurveData'
            curveNode.mapping.initialize()
            #print(curveNode.__dir__())
            #print(curveNode.mapping.__dir__())
        context.window_manager.bas_sculptnotes.curve_curveMap_isCreated = True
        context.window_manager.bas_sculptnotes.curve_useCurveMapForSplinePointsRadius = True
        return {'FINISHED'}


utils_classes = (
    BAS_OT_clear_note, BAS_OT_undo_note,
    BAS_OT_sculpt_notes_remove_curve, BAS_OT_sculpt_notes_remove_mesh,
    BAS_OT_sculpt_notes_cancel,
    BAS_OT_sculpt_notes_create_curve_map
)
