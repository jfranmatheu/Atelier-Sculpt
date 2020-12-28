import bpy
from bpy.types import Operator
from bpy.props import BoolProperty, EnumProperty, FloatProperty

from ...utils.others import ShowMessageBox


class BAS_OT_voxel_remesh_reproject(Operator):
    """Remesh by using OpenVDB Voxel Remesher"""
    bl_idname = "bas.voxel_remesh_reproject"
    bl_label = "Voxel Remesh with Reprojection"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):
        wm = context.window_manager
        obj = context.active_object
        remesh = wm.bas_remesh
        try:
            if context.sculpt_object.use_dynamic_topology_sculpting:
                bpy.ops.sculpt.dynamic_topology_toggle()
                use_dyntopo = True
            else:
                use_dyntopo = False
        except:
            use_dyntopo = False
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
        obj_copy = context.active_object
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(state=True)
        context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.object.voxel_remesh()
        bpy.ops.object.mode_set(mode='OBJECT')

        if remesh.voxel_reprojection == 'DOUBLE':
            sw = obj.modifiers.new(name="SW1", type='SHRINKWRAP')
            sw.wrap_method = 'TARGET_PROJECT' # PROJECT # NEAREST_VERTEX # TARGET_PROJECT # NEAREST_SURFACEPOINT
            sw.wrap_mode = 'ABOVE_SURFACE' # ABOVE_SURFACE # ON_SURFACE
            sw.target = obj_copy
            sw.use_positive_direction = True
            sw.use_negative_direction = True
            sw.cull_face = 'FRONT'
            bpy.ops.object.modifier_apply(modifier="SW1")
            sw = obj.modifiers.new(name="SW2", type='SHRINKWRAP')
            sw.wrap_method = 'TARGET_PROJECT' # PROJECT # NEAREST_VERTEX # TARGET_PROJECT # NEAREST_SURFACEPOINT
            sw.wrap_mode = 'ABOVE_SURFACE' # ABOVE_SURFACE # ON_SURFACE
            sw.target = obj_copy
            sw.use_positive_direction = True
            sw.use_negative_direction = True
            sw.cull_face = 'BACK'
            bpy.ops.object.modifier_apply(modifier="SW2")
        else:
            sw = obj.modifiers.new(name="SW", type='SHRINKWRAP')
            sw.wrap_method = 'NEAREST_SURFACEPOINT' # PROJECT # NEAREST_VERTEX # TARGET_PROJECT # NEAREST_SURFACEPOINT
            sw.wrap_mode = 'ABOVE_SURFACE' # ABOVE_SURFACE # ON_SURFACE
            sw.target = obj_copy
            bpy.ops.object.modifier_apply(modifier="SW")

        bpy.data.objects.remove(obj_copy)

        bpy.ops.object.mode_set(mode='SCULPT')

        if use_dyntopo:
            bpy.ops.sculpt.dynamic_topology_toggle()

        return {'FINISHED'}

class BAS_OT_voxel_remesh_join(Operator):
    """Remesh by using OpenVDB Voxel Remesher"""
    bl_idname = "bas.voxel_remesh_join"
    bl_label = "Voxel Remesh Join Objects"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return context.active_object

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT') # Cambiamos a Object
        #activeObj = context.active_object
        #activeObj.select_set(state=True) # AÑADIMOS EL OBJETO INICIAL A LA SELECCION
        context.window_manager.bas_remesh.voxel_join_object.select_set(state=True)
        bpy.ops.object.join() # JOIN PARA AMBOS OBJ
        bpy.ops.object.mode_set(mode='SCULPT') # Cambiamos a Object
        bpy.ops.object.voxel_remesh()
        context.window_manager.bas_remesh.voxel_join_object = None
        return {'FINISHED'}

class BAS_OT_voxel_remesh(Operator):
    """Remesh by using OpenVDB Voxel Remesher"""
    bl_idname = "bas.voxel_remesh"
    bl_label = "Voxel Remesh (Dyntopo Support)"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'SCULPT'

    def execute(self, context):
        if context.sculpt_object.use_dynamic_topology_sculpting:
            bpy.ops.sculpt.dynamic_topology_toggle()
            bpy.ops.object.voxel_remesh()
            bpy.ops.sculpt.dynamic_topology_toggle()
        else:
            bpy.ops.object.voxel_remesh()

        return {'FINISHED'}

class BAS_OT_dyntopo_remesh(Operator):
    """Remesh by using Dyntopo Flood Fill"""
    bl_idname = "bas.dyntopo_remesh"
    bl_label = "Dyntopo Remesh"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    resolution : FloatProperty(name="Resolution", subtype='FACTOR', default=100, min=1, max=300, precision=2, description="Mesh resolution. Higher value for a high mesh resolution")
    force_symmetry : BoolProperty(name="Force Symmetry", description="", default=False)
    symmetry_axis : EnumProperty(items=(('POSITIVE_X', "X", ""), ('POSITIVE_Y', "Y", ""), ('POSITIVE_Z', "Z", "")), default='POSITIVE_X', name="Axis", description="Axis where apply symmetry")
    only_masked : BoolProperty(name="Remesh masked", default=False)

    @classmethod
    def poll(cls, context):
        return context.active_object

    def execute(self, context):
        if context.sculpt_object.use_dynamic_topology_sculpting:
            if self.only_masked:
                bpy.ops.paint.mask_flood_fill(mode='INVERT')
            tool_settings = context.tool_settings
            sculpt = tool_settings.sculpt
            detail_method = sculpt.detail_type_method
            sculpt.detail_type_method = 'CONSTANT'
            resolution = sculpt.constant_detail_resolution
            sculpt.constant_detail_resolution = self.resolution
            #bpy.ops.sculpt.set_detail_size()
            bpy.ops.sculpt.detail_flood_fill()
            if self.force_symmetry:
                #symmetry_dir = sculpt.symmetrize_direction
                sculpt.symmetrize_direction = self.symmetry_axis
                bpy.ops.sculpt.symmetrize()
            sculpt.constant_detail_resolution = resolution
            #sculpt.symmetrize_direction = symmetry_dir
            sculpt.detail_type_method = detail_method
        else:
            # Shows a message box with an error message when dyntopo is disabled
            ShowMessageBox("This remesher only works if Dyntopo is enabled", "Can't apply remesher", 'ERROR')
            self.report({'ERROR'}, "Dyntopo should be enabled")
        return {'FINISHED'}

class BAS_OT_decimate_remesh(Operator):
    """Remesh by using Decimate Modifier"""
    bl_idname = "bas.decimate_remesh"
    bl_label = "Decimation Remesh"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    type : EnumProperty(
        items=(('COLLAPSE', "Collapse", ""), ('UNSUBDIVIDE', "Un-Subdivide", ""), ('PLANAR', "Planar", "")),
        default='COLLAPSE', description="Decimation Type to apply"
    )
    ratio : FloatProperty(name="% of Triangles", subtype='PERCENTAGE', default=100, min=0.0001, max=100, precision=2, description="Percentage of triangles. Less value = less triangles")
    triangulate : BoolProperty(name="Triangulate", description="", default=False)
    symmetry : BoolProperty(name="Symmetry", description="", default=False)
    symmetry_axis : EnumProperty(
        items=(('X', "X", ""), ('Y', "Y", ""), ('Z', "Z", "")),
        default='X', description="Axis where apply symmetry", name="Axis"
    )

    @classmethod
    def poll(cls, context):
        return context.active_object

    def execute(self, context):
        obj = context.active_object
        decimation = obj.modifiers.new(name="Remesh", type='DECIMATE')
        decimation.ratio = self.ratio / 100 # % to factor range(0, 1)
        decimation.use_collapse_triangulate = self.triangulate
        decimation.use_symmetry = self.symmetry
        decimation.symmetry_axis = self.symmetry_axis
        bpy.ops.object.modifier_apply(modifier="Remesh")
        return {'FINISHED'}


classes = (
    BAS_OT_voxel_remesh,
    BAS_OT_voxel_remesh_reproject,
    BAS_OT_voxel_remesh_join,
    BAS_OT_dyntopo_remesh,
    BAS_OT_decimate_remesh
)
