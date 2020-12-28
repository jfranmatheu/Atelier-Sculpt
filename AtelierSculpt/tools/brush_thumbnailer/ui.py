from bpy.types import Panel


class BrushThumbnailerOptions(Panel):
    bl_idname = "BAS_PT_brush_thumbnailer_options"
    bl_label = "Brush Thumbnailer"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "NONE"
    bl_category = 'Sculpt'
    bl_description = "Render Custom Brush Icon Options"

    #   BRUSH OPTIONS
    def draw(self, context):
        col = self.layout
        props = context.window_manager.bas_brush_thumbnailer
        block = col.box().column(align=True)
        block.label(text="Custom Brush Icon")
        block.separator()
        row = block.row()
        row.scale_y = 1.5
        row.prop(props, 'mode', expand=True, text="Manual")

        if props.mode == 'AUTO':
            settings = block.box().column(align=True)
            settings.label(text="Settings :", icon='SETTINGS')

            row = settings.split(align=True, factor=0.1)
            row.prop(props, 'override_size', text="", toggle=False) # Override
            ppt = row.row()
            ppt.enabled = props.override_size
            ppt.prop(props, 'brush_size', text="Brush Size", slider=True)

            row = settings.split(align=True, factor=0.1)
            row.prop(props, 'override_strength', text="", toggle=False) # Override
            ppt = row.row()
            ppt.enabled = props.override_strength
            ppt.prop(props, 'brush_strength', text="Brush Strength", slider=True)

            settings.prop(props, 'inverted', text="Invert Brush Direction")

            settings.prop(props, 'use_text', text="Use Text")
            row = settings.split(align=True, factor=0.1)
            row.label(text='') # Dummy
            col = row.column(align=True)
            col.enabled = props.use_text
            col.prop(props, 'text', text="")
            row = col.split(align=True, factor=0.4)
            row.prop(props, 'text_color', text="")
            row.prop(props, 'text_size', text="Size", slider=True)

            _col = settings
        else:
            _col = block.box().column(align=True)

        # 4TH ROW
        _col.separator()
        _col.label(text="Background Color :", icon='IMAGE_BACKGROUND')
        row = _col.split(align=True, factor=0.1)
        row.label(text='') # Dummy
        col = row.column(align=True)
        col.prop(props, 'use_alpha', text="Use Alpha")
        ppt = col.row()
        ppt.enabled = not props.use_alpha
        ppt.prop(props, 'bg_color', text="")

        _col.separator()
        _col.label(text="Mesh Color :", icon='SHADING_RENDERED')
        row = _col.split(align=True, factor=0.1)
        row.label(text='') # Dummy
        col = row.column(align=True)
        col.prop(props, 'use_tint', text="Use Tint")
        ppt = col.row()
        ppt.enabled = props.use_tint
        ppt.prop(props, 'tint', text="")

        #row = _col.row(align=True)
        #row.scale_y = 1.2
        #row.prop(props, "focal_length", text="Focal Length", slider=True)

        block.separator()
        row = block.row()
        row.scale_y = 1.5
        row.operator("bas.brush_render_icon", text="Render Custom Brush Icon", icon='RESTRICT_RENDER_OFF')
