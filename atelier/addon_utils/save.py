import bpy
from os.path import basename, join, dirname
from bpy.types import Operator
from ..import __package__ as main_package

class FILE_OT_incremental_save(Operator):
    bl_idname = "file.incremental_save"
    bl_label = "Incremental Save"
    bl_description = "Save new version of the actual project"
    bl_options = {"REGISTER", "UNDO"}
    def execute(self, context):
        nota = context.preferences.addons[main_package].preferences.file_incremental_notation
        filepath = bpy.data.filepath
        if filepath.count(nota):
            strnum = filepath.rpartition(nota)[-1].rpartition(".blend")[0]
            intnum = int(strnum)
            modnum = strnum.replace(str(intnum), str(intnum+1))
            output = filepath.replace(strnum, modnum)
            base = basename(filepath)
            bpy.ops.wm.save_as_mainfile(filepath=join(dirname(filepath),("%s"+nota+"%s.blend") % (base.rpartition(nota)[0],str(modnum))))
        else:
            output = filepath.rpartition(".blend")[0]+nota+"01"
            bpy.ops.wm.save_as_mainfile(filepath=output+".blend")

        return {'FINISHED'}
