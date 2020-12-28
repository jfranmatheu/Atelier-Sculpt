import bpy
from bpy.types import Operator
from bpy.props import BoolProperty, IntProperty, StringProperty


class BAS_OT_brush_remove(Operator):
    bl_idname = "bas.brush_remove"
    bl_label = ""
    bl_description = "Remove and Unlink Active Brush"
    def execute(self, context):
        brush = context.tool_settings.sculpt.brush
        st = brush.sculpt_tool

        # TODO: ENSURE TO REMOVE FROM FAV BRUSHES !
        #if brush in favBrushes:
        #    favBrushes.remove(bpy.data.brushes[brush.name])

        bpy.data.brushes.remove(brush, do_unlink=True)
        brush = None

        # Seleccionar automaticamente una brocha del mismo tipo
        for b in bpy.data.brushes:
            if b.sculpt_tool == st and b.use_paint_sculpt:
                context.tool_settings.sculpt.brush = b
                return {'FINISHED'}

        if not context.tool_settings.sculpt.brush:
            # Sino hay ninguna del mismo tipo entonces se cogerá la primera en buscar
            for b in bpy.data.brushes:
                if b.use_paint_sculpt:
                    context.tool_settings.sculpt.brush = b
                    return {'FINISHED'}
        return {'FINISHED'}

classes = [
    BAS_OT_brush_remove
]