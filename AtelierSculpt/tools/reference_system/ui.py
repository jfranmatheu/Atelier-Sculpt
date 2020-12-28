# Copyright (C) 2019 Juan Fran Matheu G.
# Contact: jfmatheug@gmail.com 
import bpy
from bpy.types import Panel


references = []
reference_collections = {}
class BAS_PT_Reference_System(Panel):
    bl_label = "Import References"
    bl_category = 'Sculpt'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = ".paint_common"
    bl_options = {'DEFAULT_CLOSED'}
    #bl_ui_units_x = 14
    bl_order = 10

    can_create = False

    def draw_header(self, context):
        self.layout.label(text="", icon='RENDERLAYERS') # FILE_IMAGE  OUTLINER_OB_IMAGE RENDERLAYERS
        self.layout.separator()

    def draw(self, context):
        wm = context.window_manager.bas_references
        scn = context.scene.bas_references

        layout = self.layout
        col = layout.column(align=True)
        
        content = col.box()

        row = content.row()
        row.scale_y = 1.3
        row.prop(wm, "get_references_from", text="Single Image", expand=True)

        if wm.get_references_from == 'SINGLE':
            content.label(text="Image Path", icon='FILE_IMAGE')
            content.prop(wm, "image_path", text="")
            if wm.image_path == "":
                content.alert = True
                content.label(text="Please, select your reference image")
                content.alert = False
                self.can_create = False
            else:
                self.can_create = True

        elif wm.get_references_from == 'FOLDER':
            content.label(text="Folder Directory", icon='FILE_FOLDER')
            content.prop(wm, "previews_dir", text="")
            if wm.previews == "":
                content.alert = True
                content.label(text="Please, select your references folder")
                content.alert = False
                self.can_create = False
            else:
                content.template_icon_view(wm, "previews")
                content.prop(wm, "previews", text="")
                self.can_create = True

        content.separator(factor=.1)
        
        if self.can_create:
            content = col.box()
            content.separator(factor=.1)
            text = content.row(align=True).split(factor=.25)
            text.label(text="Name :")
            text.prop(wm, "name", text="")
            content.prop(wm, "keep_in_actual_mode", text="Keep In Actual Mode", toggle=False)
            #content.prop(wm, "reference_image_opacity", text="Image Opacity")
            #content.prop(wm, "reference_use_transparency", text="Use Transparency", toggle=False)
            content.separator(factor=.1)
            # LABEL SECTION
            section = col.box().column(align=True)
            header = section.box().row()
            arrow_icon = 'TRIA_DOWN' if wm.ui_show_label else 'TRIA_RIGHT'
            #header_text = "       (ON)" if wm.reference_use_label else "     (OFF)"
            header.prop(wm, "use_label", text="", toggle=False)
            header.prop(wm, "ui_show_label", text="Label   ", toggle=True, icon='BOOKMARKS', emboss=False)
            header.label(text="", icon=arrow_icon)
            if wm.ui_show_label:
                label = section.box()
                label.prop(wm, "label_color", text="Label Color")
                label.prop(wm, "label_thickness", text="Label Thickness")
                label.row().prop(wm, "label_align", text="Label Align", expand=True)
                text = label.row(align=True).split(factor=.35)
                text.label(text="Label Text")
                text.prop(wm, "label_text", text="")
                label.prop(wm, "label_text_size", text="Text Size")
                label.prop(wm, "label_text_color", text="Text Color")
                label.row().prop(wm, "label_text_align", text="Text Align", expand=True)
                label.prop(wm, "label_text_padding", text="Global Label Text Padding")
                label.separator(factor=1)
            # OUTLINE SECTION
            #section = content.column(align=True) # This is to split our label and outline properties boxes
            header = section.box().row()
            arrow_icon = 'TRIA_DOWN' if wm.ui_show_outline else 'TRIA_RIGHT'
            #header_text = "    (ON)" if wm.reference_use_outline else "  (OFF)"
            header.prop(wm, "use_outline", text="")
            header.prop(wm, "ui_show_outline", text="Outline", toggle=True, icon='MATPLANE', emboss=False)
            header.label(text="", icon=arrow_icon)
            if wm.ui_show_outline:
                outline = section.box()
                outline.prop(wm, "outline_color", text="Outline Color")
                outline.separator(factor=.5)
            # OTHER PROPERTIES
            #if scn.is_using_references:
            #    other = col.box()
            #    other.prop(wm, "reference_label_text_padding", text="Global Label Text Padding")
            
            # DRAW OPERATOR
            op = col.box()
            op.scale_y = 1.5
            op.operator('bas.reference_maker', text="Draw Reference")

class BAS_PT_Reference_Manager(Panel):
    bl_label = "References"
    bl_category = 'Sculpt'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = ".paint_common"
    bl_options = {'DEFAULT_CLOSED'}
    #bl_ui_units_x = 14
    bl_order = 11

    def draw_header(self, context):
        wm = context.window_manager.bas_references
        row = self.layout.row(align=True)
        hide_icon = 'HIDE_ON' if wm.hide_all else 'HIDE_OFF'
        row.prop(wm, "hide_all", text="", icon=hide_icon, toggle=True)
        lock_icon = 'DECORATE_LOCKED' if wm.lock_all else 'DECORATE_UNLOCKED'
        row.prop(wm, "lock_all", text="", icon=lock_icon, toggle=True)
        row.separator()
        row.label(text="", icon='RENDERLAYERS') # FILE_IMAGE  OUTLINER_OB_IMAGE
        

    def draw(self, context):
        wm = context.window_manager.bas_references
        scn = context.scene.bas_references

        # AVOID TO DRAW IF NOT REFERENCES ARE AVAILABLE
        if scn.is_using_references:
            layout = self.layout
            col = layout.column(align=True)
            
            content = col.box().column(align=True)
            header = content.box()
            header.label(text="Image References", icon='RENDER_RESULT')
            refs = content.box()
            n = 0
            m = 0
            for ref in references:
                if ref.mode == 'ALL' or ref.mode == context.mode:
                    row = refs.row(align=True)
                # HIDE
                    hide = row.row(align=True)
                    hide.enabled = not wm.hide_all
                    isHidden = True if ref.signal == 'H' else False
                    hide_icon = 'HIDE_ON' if isHidden else 'HIDE_OFF'
                    hide.operator("bas.hide_reference", text="", icon=hide_icon, depress=isHidden).index = n
                # LOCK
                    look = row.row(align=True)
                    look.enabled = not wm.lock_all
                    lock_icon = 'DECORATE_LOCKED' if ref.is_locked else 'DECORATE_UNLOCKED'
                    look.operator("bas.lock_reference", text="", icon=lock_icon, depress=ref.is_locked).index = n
                # OVERLAP dui
                    #overlap = row.row()
                    #overlap.enabled = not wm.references_lock_all
                    row.operator("bas.overlap_reference", text="", icon='OVERLAY', depress=ref.in_front).index = n
                # TRANSPARENCY
                    row.operator("bas.transparent_reference", text="", icon='NODE_TEXTURE', depress=ref.use_transparency).index = n
                # NAME
                    row.label(text=ref.name)
                # OPTIONS
                    #options_n = n
                    #options = row.popover("DUI_PT_Reference_Options", text="", icon='THREE_DOTS')
                # FLIP X
                    flip = row.operator("bas.flip_reference", text="", icon='EVENT_X')
                    flip.index = n
                    flip.axis = 'X'
                # FLIP Y
                    flip = row.operator("bas.flip_reference", text="", icon='EVENT_Y')
                    flip.index = n
                    flip.axis = 'Y'
                # REMOVE
                    remove = row.operator("bas.remove_reference", text="", icon='TRASH')
                    remove.index = n
                    remove.permanent = False
                    #perma_remove = row.operator("bas.remove_reference", text="", icon='LIBRARY_DATA_BROKEN')
                    #perma_remove.index = n
                    #perma_remove.permanent = True
                    m += 1
                n += 1
            if n == 0:
                refs.alert = True
                refs.label(text="There are no references yet", icon='INFO')
            elif m == 0:
                refs.alert = True
                refs.label(text="No references in this mode", icon='INFO')
        else:
            self.layout.alert = True
            self.layout.label(text="There are no references yet", icon='INFO')


classes = (
    BAS_PT_Reference_System,
    BAS_PT_Reference_Manager
)
