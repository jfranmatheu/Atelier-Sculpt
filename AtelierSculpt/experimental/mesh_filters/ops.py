import bpy

def get_context():
    for window in bpy.context.window_manager.windows:
        screen = window.screen

        for area in screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        return {'window': window, 'screen': screen, 'area': area, 'region': region}
                break

AXIS = ('X', 'Y', 'Z')

def set_meshfilter(_type, _strength, _axis):
    #def_axis = set(AXIS[i] for i, axis in enumerate(_axis) if axis)
    bpy.ops.sculpt.mesh_filter (
        #get_context(),
        #'INVOKE_DEFAULT',
        type=_type,
        strength=_strength,
        deform_axis={'X', 'Y', 'Z'},
        use_face_sets=False,
        surface_smooth_shape_preservation=0.5,
        surface_smooth_current_vertex=0.5,
        sharpen_smooth_ratio=0.35
    )

def set_meshfilter_smooth(self, value):
    if value != 0:
        set_meshfilter('SMOOTH', value, self.axis)
        self.smooth = 0
    return None

def set_meshfilter_scale(self, value):
    if value != 0:
        set_meshfilter('SCALE', value, self.axis)
        self.scale = 0
    return None