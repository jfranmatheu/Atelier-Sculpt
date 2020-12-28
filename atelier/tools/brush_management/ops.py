import bpy


class BAS_OT_brush_fav_remove(bpy.types.Operator):
    bl_idname = "bas.brush_fav_remove"
    bl_label = "Remove Fav Brush"
    bl_description = "Remove Active Brush from Favourites."
    
    nBrush: bpy.props.StringProperty()
    
    def execute(self, context):
        from .ui import favBrushes
        brush = bpy.data.brushes.get(self.nBrush, None)
        if brush:
            favBrushes.remove(brush)
        return {'FINISHED'}


class BAS_OT_brush_fav_add(bpy.types.Operator):
    bl_idname = "bas.brush_fav_add"
    bl_label = "Add Fav Brush"
    bl_description = "Add Active Brush to Favourites."
    
    nBrush: bpy.props.StringProperty()
    
    def execute(self, context):
        brush = bpy.data.brushes.get(self.nBrush, None)
        if not brush:
            return {'FINISHED'}
        from .ui import favBrushes
        if brush in favBrushes:
            return {'FINISHED'}
        favBrushes.append(brush)
        return {'FINISHED'}

class BAS_OT_change_brush(bpy.types.Operator):
    bl_idname = "bas.change_brush"
    bl_label = ""
    bl_description = "Change actual brush to selected one."
    
    nBrush: bpy.props.StringProperty()

    def execute(self, context):
        brush = bpy.data.brushes.get(self.nBrush, None)
        if not brush:
            return {'FINISHED'}
        context.tool_settings.sculpt.brush = brush
        return {'FINISHED'}

classes = (
    BAS_OT_brush_fav_add, BAS_OT_brush_fav_remove,
    BAS_OT_change_brush
)


'''
class NSMUI_OT_toolHeader_brushRemove(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_brush_remove"
    bl_label = ""
    bl_description = "Remove Active Brush plus Unlink"
    def execute(self, context):
        brush = bpy.context.tool_settings.sculpt.brush
        st = brush.sculpt_tool
        try:
            if brush in favBrushes:
                favBrushes.remove(bpy.data.brushes[brush.name])
        except:
            pass
        try:
            
            bpy.data.brushes.remove(brush, do_unlink=True)
            # Seleccionar automaticamente una brocha del mismo tipo
            for b in bpy.data.brushes:
                if b.sculpt_tool == st and b.use_paint_sculpt:
                    bpy.context.tool_settings.sculpt.brush = b
                    return {'FINISHED'}
            # Sino hay ninguna del mismo tipo entonces se cogerá la primera en buscar
            for b in bpy.data.brushes:
                if b.use_paint_sculpt:
                    bpy.context.tool_settings.sculpt.brush = b
                    return {'FINISHED'}
        except:
            pass
        
        return {'FINISHED'}
'''
