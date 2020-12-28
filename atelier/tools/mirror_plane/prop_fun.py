import bpy


def update_mirror(self, context):
    if self.show:
        bpy.ops.bas.mirror_plane('INVOKE_DEFAULT')
    return

def update_mirror_plane_color(self, context):
    try:
        self.mirror_object.color =  self.color
    except:
        pass
    return
