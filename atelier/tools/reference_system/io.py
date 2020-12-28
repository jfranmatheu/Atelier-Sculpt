# Copyright (C) 2019 Juan Fran Matheu G.
# Contact: jfmatheug@gmail.com 
from os import path, sep
data_dir = path.join(path.dirname(__file__), "data")
references_path = path.join(data_dir, "references")

import bpy

def Create_Ref_Data():
    try:
        name = bpy.path.basename(bpy.context.blend_data.filepath).split(".blend")[0]
        path_to_refs = references_path + sep + name + ".json"
        bpy.context.scene.bas_references.data_base = path_to_refs
        f = open(path_to_refs, "w") # write, create if it doesn't exist
        return True
    except:
        return False

def Save_Ref_Data(_buttonData):
    # TODO Button data must be serialized before
    refs_data = bpy.context.scene.bas_references.data_base
    with open(refs_data) as data_file:
        data_loaded = json.load(data_file)
    with open(refs_data, 'w+', encoding='utf-8') as json_file: # Después de salir del bloque del "with" el archivo es cerrado automáticamente
        if data_loaded != {}:
            json.dump(MergeDictionaries(data_loaded, _buttonData), json_file, ensure_ascii=False, indent=4)
        else:
            json.dump(_buttonData, json_file, ensure_ascii=False, indent=4)
    # TODO algunos matices que ajustar acorde a las settings
