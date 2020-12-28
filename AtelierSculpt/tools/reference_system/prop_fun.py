# Copyright (C) 2019 Juan Fran Matheu G.
# Contact: jfmatheug@gmail.com 
import bpy

def update_references_hide_all(self, context):
    if self.hide_all:
        bpy.ops.bas.hide_all_references(hide=True)
    else:
        bpy.ops.bas.hide_all_references(hide=False)
    return None

def update_references_lock_all(self, context):
    if self.lock_all:
        bpy.ops.bas.lock_all_references(state=True)
    else:
        bpy.ops.bas.lock_all_references(state=False)
    return None
