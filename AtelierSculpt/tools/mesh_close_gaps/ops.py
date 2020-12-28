import bpy
from bpy.types import Operator
from bpy.props import EnumProperty, IntProperty, BoolProperty


class BAS_OT_Close_Gaps(Operator):
    """Destroy those gaps from that broken mesh!"""
    bl_idname = "bas.close_gaps"
    bl_label = "Close Gaps"

    use : EnumProperty (
        items=(
            ('TRIS', "Tris", ""),
            ('QUADS', "Quads", "")
        ),
        default='TRIS',
        name="Use tris or quads",
        description="Close gap with tris or quads"
    )

    smooth_passes : IntProperty (
        default = 3,
        max = 10,
        min = 0,
        name = "Smooth Passes",
        description = "Number of smooth passes that will be applied after closing the gap"
    )

    keep_dyntopo : BoolProperty (
        default = True,
        name="Keep Dyntopo",
        description="Only works if you are using dyntopo"
    )

    def execute(self, context):
        usingDyntopo = bpy.context.sculpt_object.use_dynamic_topology_sculpting
        try:
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE', action='TOGGLE')
            bpy.ops.mesh.select_non_manifold()
            if self.use == 'TRIS':
                bpy.ops.mesh.fill()
            elif self.use == 'QUADS':
                try:
                    bpy.ops.mesh.fill_grid()
                except:
                    ShowMessageBox("The mesh is not compatible with 'Quads' mode or there's no gaps to close. Will try to close with tris.", "Can't close gaps with quads", 'ERROR')
                    bpy.ops.mesh.fill()
                    #bpy.ops.mesh.fill_holes(sides=100)
            n = 0
            while n < self.smooth_passes:
                bpy.ops.mesh.vertices_smooth()
                n+=1
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='SCULPT')

            if self.keep_dyntopo and usingDyntopo:
                bpy.ops.sculpt.dynamic_topology_toggle()
        except:
            bpy.ops.object.mode_set(mode='SCULPT')
            if self.keep_dyntopo and usingDyntopo:
                bpy.ops.sculpt.dynamic_topology_toggle()
        return {'FINISHED'}


classes = (
    BAS_OT_Close_Gaps,
)
