def register_keymap():
    from bpy import context
    cfg = context.window_manager.keyconfigs.addon
    if not cfg.keymaps.__contains__('Sculpt'):
        cfg.keymaps.new('Sculpt', space_type='EMPTY', region_type='WINDOW')
    kmi = cfg.keymaps['Sculpt'].keymap_items
    kmi.new('sculpt.brush_rmb', 'RIGHTMOUSE', 'PRESS')
    kmi.new('sculpt.brush_rmb_alt', 'RIGHTMOUSE', 'PRESS', alt=True)
    
def unregister_keymap():
    from bpy import context
    cfg = context.window_manager.keyconfigs.addon
    if cfg.keymaps.__contains__('Sculpt'):
        for kmi in cfg.keymaps['Sculpt'].keymap_items:
            if kmi.idname == 'sculpt.brush_rmb' or (kmi.idname == 'sculpt.brush_rmb_alt'):
                if kmi.value == 'PRESS' and kmi.type == 'RIGHTMOUSE':
                    cfg.keymaps['Sculpt'].keymap_items.remove(kmi)
                    break