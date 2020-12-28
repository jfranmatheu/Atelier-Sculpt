def register(reg):
    from .ops import classes
    from .ui import BAS_PT_Mask_By_Cavity
    reg(BAS_PT_Mask_By_Cavity)

    for cls in classes:
        reg(cls)

def unregister(unreg):
    from .ui import BAS_PT_Mask_By_Cavity
    unreg(BAS_PT_Mask_By_Cavity)

    from .ops import classes
    for cls in reversed(classes):
        unreg(cls)
