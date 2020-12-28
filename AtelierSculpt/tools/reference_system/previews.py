# Copyright (C) 2019 Juan Fran Matheu G.
# Contact: jfmatheug@gmail.com 
import os
import bpy
from .ui import reference_collections
from bpy.utils import previews


def register_previews():
    p_pcoll = previews.new()
    p_pcoll.bas_reference_previews_dir = ""
    p_pcoll.bas_reference_previews = ()
    reference_collections["previews"] = p_pcoll
    
def unregister_previews():
    previews.remove(reference_collections["previews"])

def enum_previews_from_directory_items(self, context):
    """EnumProperty callback"""
    if context is None:
        return []

    #scn = context.scene.bas_references
    wm = context.window_manager.bas_references
    
    if wm.previews_dir == "":
        return []
    enum_items = []
    directory = wm.previews_dir

    # Get the preview collection (defined in register func).
    pcoll = reference_collections["previews"]

    if directory == pcoll.bas_reference_previews_dir:
        return pcoll.bas_reference_previews

    print("Scanning directory: %s" % directory)

    if directory and os.path.exists(directory):
        # Scan the directory for png files
        image_paths = []
        for fn in os.listdir(directory):
            if fn.lower().endswith(".png") or fn.lower().endswith(".jpg"):
                image_paths.append(fn)

        for i, name in enumerate(image_paths):
            # generates a thumbnail preview for a file.
            filepath = os.path.join(directory, name)
            icon = pcoll.get(name)
            if not icon:
                thumb = pcoll.load(name, filepath, 'IMAGE')
            else:
                thumb = pcoll[name]
            enum_items.append((name, name, "", thumb.icon_id, i))

    pcoll.bas_reference_previews = enum_items
    pcoll.bas_reference_previews_dir = directory
    return pcoll.bas_reference_previews

# We can store multiple preview collections here,
# however in this example we only store "main"
#preview_collections = {}
