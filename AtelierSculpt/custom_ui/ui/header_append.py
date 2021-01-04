def temporal_tool_header_buttons(self, context):
    if context.mode == 'SCULPT':
        self.layout.menu('BAS_MT_toolheader_ctx_ui_presets', text="Presets")
        self.layout.menu("BAS_MT_custom_ui_items", text="", icon='ADD')
        self.layout.operator('bas.edit_custom_ui', text="", icon='GREASEPENCIL')
