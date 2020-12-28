import bpy
import bmesh


class BAS_OT_mask_by_cavity(bpy.types.Operator) :
    ''' Mask From Cavity'''
    bl_idname = "bas.mask_by_cavity"
    bl_label = "Mask By Cavity"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.mode == 'SCULPT'

    def execute(self, context):
        mask = context.window_manager.bas_mask
        mask_cavity_angle = mask.cavity_angle # update property from user input
        mask_cavity_strength = mask.cavity_strength # update property from user input

        dynatopoEnabled = False

        if context.active_object.mode == 'SCULPT' :

            if context.sculpt_object.use_dynamic_topology_sculpting :
                dynatopoEnabled = True
                bpy.ops.sculpt.dynamic_topology_toggle()

            BM = bmesh.new() # New bmesh container
            BM.from_mesh(context.active_object.data) # Fill container with our object
            mask = BM.verts.layers.paint_mask.verify() # get active mask layer
            BM.faces.ensure_lookup_table() # Update vertex lookup table

            mask_cavity_angle *= (3.14 * 0.0055556) # Convert angle to radians (approx)
            maskWeight = 1.0 * mask_cavity_strength

            for face in BM.faces :
                for vert in face.verts :
                    vert [mask] = 0.0 # Clear any mask before
                    for loop in vert.link_loops :
                        loopTan =  loop.calc_tangent()
                        angleFace = (face.normal.angle (loopTan, 0.0))
                        angleDiff = (vert.normal.angle( loopTan, 0.0 )) # get the angle between the vert normal to loop edge Tangent
                        if ( angleFace + angleDiff ) <=  (1.57 + mask_cavity_angle) : # if the difference is greater then input
                            vert [mask] = maskWeight # mask it with input weight

            BM.to_mesh(context.active_object.data) # Fill obj data with bmesh data
            BM.free() # Release bmesh
            # mesh.clear_geometry()
            bpy.ops.sculpt.mask_filter(filter_type='SMOOTH', auto_iteration_count=True)
            bpy.ops.sculpt.mask_filter(filter_type='SHARPEN', iterations=3, auto_iteration_count=True)
            
            if dynatopoEnabled :
                bpy.ops.sculpt.dynamic_topology_toggle()

        return {'FINISHED'}
    

classes = (
    BAS_OT_mask_by_cavity,
)