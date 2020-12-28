from bpy.types import Operator
from bpy.props import FloatProperty


class BAS_OT_voxel_size_increment(Operator):
    bl_idname = "bas.voxel_size_increment"
    bl_label = "Increment Voxel Size"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    value : FloatProperty(default=0.1, min=-.5, max=.5, name="Voxel Size Increment")

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'

    def execute(self, context):
        context.active_object.data.remesh_voxel_size += self.value
        return {'FINISHED'}


class BAS_OT_voxel_size_change(Operator):
    bl_idname = "bas.voxel_size_change"
    bl_label = "Change Voxel Size"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    value : FloatProperty(default=0.1, min=.00001, max=1, name="Voxel Size Value")

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == 'MESH'

    def execute(self, context):
        context.active_object.data.remesh_voxel_size = self.value
        return {'FINISHED'}


utils_classes = [
    BAS_OT_voxel_size_increment,
    BAS_OT_voxel_size_change
]
