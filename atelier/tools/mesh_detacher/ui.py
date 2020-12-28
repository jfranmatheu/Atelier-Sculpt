from bpy.types import Panel


def draw_mesh_detacher(layout, context):
    props = context.window_manager.bas_detacher
    row = layout.row(align=True)
    row.ui_units_x = 6.3
    _props = row.operator("bas.mask_detacher", text="Mesh Detacher", icon='LIBRARY_DATA_BROKEN') # OUTLINER_OB_META
    _props.detachInDifferentObjects = props.detach_multi_objects
    _props.separateLooseParts = props.separate_loose_parts
    _props.sculptMaskedMesh = props.go_sculpt_masked_mesh
    _props.closeDetachedMeshes = props.close_detached_meshes
    _props.closeOnlyMasked = props.close_only_masked
    _props.doRemesh = props.do_remesh
    row.popover(panel="BAS_PT_Mesh_Detacher_Options", text="")

class BAS_PT_Mesh_Detacher_Options(Panel):
    bl_label = "Mesh Detacher Options"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "NONE"
    bl_category = 'Sculpt'
    bl_description = "Mesh Detacher Options"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        props = context.window_manager.bas_detacher
        layout = self.layout
        row = layout.row()
        row.prop(props, 'detach_multi_objects')
        _layout = layout.column()
        _layout.enabled = props.detach_multi_objects
        row = _layout.row()
        row.prop(props, 'separate_loose_parts')
        row = _layout.row()
        row.enabled = not props.separate_loose_parts
        row.prop(props, 'go_sculpt_masked_mesh')
        row = _layout.row()
        if props.separate_loose_parts:
            row.enabled = False
        else:
            row.enabled = True
        row.prop(props, 'close_detached_meshes')
        row = _layout.row()
        if not props.close_detached_meshes or props.separate_loose_parts:
            row.enabled = False
        else:
            row.enabled = True
        row.prop(props, 'do_remesh')
        row.prop(props, 'close_only_masked')
