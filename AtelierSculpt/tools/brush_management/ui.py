from bpy.types import Panel
from bl_ui.properties_paint_common import UnifiedPaintPanel
from ...icons import Icon
import bpy


# BRUSHES MAIN PANEL
class BAS_PT_Brushes(Panel, UnifiedPaintPanel):
    bl_label = "Brushes"
    bl_category = 'Sculpt'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = ".paint_common"
    # bl_options = {'DEFAULT_CLOSED'}
    bl_order = -1

    def draw(self, context):
        if(context.mode == "SCULPT"):
            props = context.scene.bas_brush_management

            try:
                sculpt = context.tool_settings.sculpt
                settings = self.paint_settings(context)
                
                brush = settings.brush
            except:
                pass

            layout = self.layout
            split = layout.split(align=True)

            split.prop(props, 'toggle_brush_preview', icon='IMAGE_PLANE', text="", toggle=True)
            split.prop(props, 'toggle_brush_favourites', icon='SOLO_ON', text="", toggle=True)
            split.prop(props, 'toggle_brush_pertype', icon='IMGDISPLAY', text="", toggle=True)
            split.prop(props, 'toggle_brush_recents', icon='RECOVER_LAST', text="", toggle=True)

            if props.toggle_brush_preview:
                layout.use_property_decorate = False  # No animation.
                settings = self.paint_settings(context)
                try:
                    brush = settings.brush
                
                    row = layout.row()
                    row.column().template_ID_preview(settings, "brush", cols=4, rows=7, hide_buttons=True)

                    if props.show_brush_options:
                        col = row.column(align=True)
                        col.scale_y = 1.5
                        col.scale_x = 1.3
                        col.operator("brush.add", text="", icon_value=Icon.BRUSH_ADD()) # DUPLICATE BRUSH
                        col.operator("brush.reset", text="", icon_value=Icon.BRUSH_RESET()) # RESET BRUSH
                        col.operator("bas.brush_remove", text="", icon_value=Icon.BRUSH_REMOVE()) # DELETE BRUSH
                        col.operator("bas.brush_render_icon", text="", icon='RESTRICT_RENDER_OFF') # RENDER CUSTOM ICON
                except:
                    pass

        
            count = 0
            if props.toggle_brush_favourites == True: count = count + 1
            if props.toggle_brush_pertype == True: count = count + 1
            if props.toggle_brush_recents == True: count = count + 1

            layout = self.layout
            
            if count > 1:
                if props.toggle_brush_favourites:
                    row_box = layout.row(align=True)
                    box = row_box.box()
                    box.scale_y = 0.6
                    box.scale_x = 0.6
                    row = box.column().row()

                    if props.show_brush_favourites:
                        row.prop(props, "show_brush_favourites", icon="DOWNARROW_HLT", text="Favourites", emboss=False)
                        BAS_PT_Brushes_Favs.draw(self, context)
                    else:
                        row.prop(props, "show_brush_favourites", icon="RIGHTARROW", text="Favourites", emboss=False)
                        
                    row_box.prop(props, 'show_only_icons', text="", icon='FILE_IMAGE')

                if props.toggle_brush_pertype:
                    box = layout.box()
                    box.scale_y = 0.6
                    box.scale_x = 0.6
                    row = box.column().row()

                    if props.show_brush_pertype:
                        row.prop(props, "show_brush_pertype", icon="DOWNARROW_HLT", text="Per Type", emboss=False)
                        BAS_PT_Brushes_ByType.draw(self, context)
                    else:
                        row.prop(props, "show_brush_pertype", icon="RIGHTARROW", text="Per Type", emboss=False)

                if props.toggle_brush_recents:
                    row_box = layout.row(align=True)
                    box = row_box.box()
                    box.scale_y = 0.6
                    box.scale_x = 0.6
                    row = box.column().row()

                    if props.show_brush_recents:
                        row.prop(props, "show_brush_recents", icon="DOWNARROW_HLT", text="Recent Brushes", emboss=False)
                        BAS_PT_Brushes_Recent.draw(self, context)
                    else:
                        row.prop(props, "show_brush_recents", icon="RIGHTARROW", text="Recent Brushes", emboss=False)

                    row_box.prop(props, "recent_brushes_stay_in_place", text="", icon='LOCKED' if props.recent_brushes_stay_in_place else 'UNLOCKED')
            
            elif props.toggle_brush_favourites:
                layout.separator()
                BAS_PT_Brushes_Favs.draw(self, context)

            elif props.toggle_brush_pertype:
                layout.separator()
                BAS_PT_Brushes_ByType.draw(self, context)

            elif props.toggle_brush_recents:
                layout.separator()
                BAS_PT_Brushes_Recent.draw(self, context)


# RECENT BRUSHES
recentBrushes = []
class BAS_PT_Brushes_Recent(Panel):
    bl_label = "Recent Brushes"
    bl_context = 'NONE'
    
    bl_category = 'Sculpt'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        if(context.mode == "SCULPT"):
            try:
                props = context.scene.bas_brush_management
                activeBrush = context.tool_settings.sculpt.brush
                # RECENT BRUSHES
                length = len(recentBrushes)
                n = 6
                if length == 0: # or recentBrushes == [] # EMPTY LIST
                    recentBrushes.append(activeBrush)
                elif length < n+1:
                    if activeBrush in recentBrushes:
                        if not props.recent_brushes_stay_in_place:
                            recentBrushes.remove(activeBrush)
                            recentBrushes.append(activeBrush)
                    elif length == n:
                        recentBrushes.pop(0)
                        recentBrushes.append(activeBrush)
                    else:
                        recentBrushes.append(activeBrush)
            except:
                pass
            # print (length)
            # print(recentBrushes)
            col = self.layout.column() # define una fila
            for b in reversed(recentBrushes):
                # col.label(text=b, icon_value=bpy.data.brushes[b].preview.icon_id) # SOLO PREVIEW
                col.operator('bas.change_brush', text=b.name, icon_value=bpy.data.brushes[b.name].preview.icon_id).nBrush = b.name



# FAV BRUSHES
favBrushes = []
class BAS_PT_Brushes_Favs(Panel):
    bl_context = 'NONE'
    bl_label = "Favorite Brushes"
    # bl_options = {'DEFAULT_CLOSED'}
    
    bl_category = 'Sculpt'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
        
    def draw(self, context):
            props = context.scene.bas_brush_management
            try:
                activeBrush = context.tool_settings.sculpt.brush

                row = self.layout.row(align=True)
                brushName = activeBrush.name
                row.operator('bas.brush_fav_add', text="ADD", icon='ADD').nBrush = brushName
                row.operator('bas.brush_fav_remove', text="REMOVE", icon='REMOVE').nBrush = brushName
                row = self.layout.row()
                # print (length)
                # print(recentBrushes)
            except:
                pass
            
            # RECENT BRUSHES
            length = len(favBrushes)
            
            for region in context.area.regions:
                if region.type == "UI":
                    width = region.width
                    break
            #print(width)
            
            k = 0   
            i = 1
            if props.show_only_icons:
                #if length != 0:
                
                col = self.layout.grid_flow()
                
                if width > 420:
                    i = 10
                    colY = 1.6
                    colX = 1.6
                elif width > 350:
                    i = 8
                    colY = 1.8
                    colX = 1.8
                elif width > 280:
                    i = 6
                    colY = 2
                    colX = 2
                elif width > 230:
                    i = 5
                    colY = 2
                    colX = 2
                else:
                    i = 4
                    colY = 1.8
                    colX = 1.8

                col.scale_x = colX
                col.scale_y = colY

                for b in favBrushes:
                    try:
                        if b.name == brushName:
                            act = True
                        else:
                            act = False
                    except:
                        act = False
                    #row.template_icon(icon_value=bpy.data.brushes[b].preview.icon_id, scale=5)
                    # col.label(text=b, icon_value=bpy.data.brushes[b].preview.icon_id) # SOLO PREVIEW
                    k = k + 1
                    if k == 1:
                        col = col.row()
                    #col.label(text=b, icon_value=bpy.data.brushes[b].preview.icon_id) # SOLO PREVIEW
                    col.operator('bas.change_brush', depress=act, text="", icon_value=bpy.data.brushes[b.name].preview.icon_id).nBrush = b.name
                    if k == i:
                        col = self.layout.column()
                        col.scale_x = colX
                        col.scale_y = colY
                        k = 0
            else:
                if width > 280: 
                    i = 2 
                if width > 420: 
                    i = 3
                if length != 0:
                    #col = row.column() # define una fila
                    #col.separator()
                    col = self.layout.grid_flow()
                    col.scale_y = 1.1
                    col.scale_x = 1.1

                for b in favBrushes:
                    try:
                        if b.name == brushName:
                            act = True
                        else:
                            act = False
                    except:
                        act = False
                    #row.template_icon(icon_value=bpy.data.brushes[b].preview.icon_id, scale=5)
                    # col.label(text=b, icon_value=bpy.data.brushes[b].preview.icon_id) # SOLO PREVIEW
                    if i == 1:
                        col.operator('bas.change_brush', depress=act, text=b.name, icon_value=bpy.data.brushes[b.name].preview.icon_id).nBrush = b.name
                    else:
                        k = k + 1
                        if k == 1:
                            col = col.row()
                        col.operator('bas.change_brush', depress=act, text=b.name, icon_value=bpy.data.brushes[b.name].preview.icon_id).nBrush = b.name
                        if k == i:
                            col = self.layout.column()
                            col.scale_y = 1.1
                            col.scale_x = 1.1
                            k = 0


class BAS_PT_Brushes_ByType(Panel):
    bl_context = 'NONE'
    bl_label = "Related Brushes"
    # bl_options = {'DEFAULT_CLOSED'}
    
    bl_category = 'Sculpt'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        try:   
            brush = context.tool_settings.sculpt.brush
            #sculpt = context.tool_settings.sculpt
            i = 1
            for region in context.area.regions:
                if region.type == "UI":
                    width = region.width
                    break
            #print(width)
            if width > 280: 
                i = 2 
                if width > 420: 
                    i = 3
            col = self.layout.column() # define una fila
            # BRUSH LIST
            k = 0
            for b in bpy.data.brushes:
                if (b.sculpt_tool == brush.sculpt_tool) and b.use_paint_sculpt:
                    icon = bpy.data.brushes[b.name].preview
                    if b.name == brush.name:
                        act = True
                    else:
                        act = False
                    #icon.icon_size = (2,2)
                    if i == 1:
                        col.scale_y = 1.1
                        col.scale_x = 1.1
                        col.operator('bas.change_brush', depress=act, text=b.name, icon_value=icon.icon_id).nBrush = b.name
                    else:
                        k = k + 1
                        if k == 1:
                            col = col.row()
                        col.operator('bas.change_brush', depress=act, text=b.name, icon_value=icon.icon_id).nBrush = b.name
                        if k == i:
                            col = self.layout.column()
                            k = 0
        except:
            pass


classes = (
    BAS_PT_Brushes,
    BAS_PT_Brushes_ByType,
    BAS_PT_Brushes_Favs,
    BAS_PT_Brushes_Recent
)
