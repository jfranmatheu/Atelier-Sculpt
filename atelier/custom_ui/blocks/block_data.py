from .block_id_draw import UI_BLOCK_DRAW
from .block_id_ppts import UI_BLOCK_PPTS

variable_id_blocks = {'DEF_SEPARATOR_SPACER'}
blocks = []

class UI_Block():
    active_block_index = -1

    def __init__(self, id: str, width: int = 1, x: int = 0):
        self.id = id
        self.name = id.replace('_', ' ').capitalize()
        self.func = UI_Block.get_func(id)
        self.width = width
        self.ui_units_x = width
        self.var_width = id in variable_id_blocks
        self.x = x
        self.abs_x = x
        self.min_max_width = [1, 15]
        self.ppts = UI_Block.get_ppts(id)

        blocks.append(self)

    def __call__(self, ui):
        #return self.func(ui)
        self.ui_units_x = self.func(ui)

    @classmethod
    def pop(cls, i):
        blocks.pop(i)

    @classmethod
    def clear(cls):
        blocks.clear()

    @classmethod
    def get_func(cls, id):
        return eval('UI_BLOCK_DRAW.' + id)

    @classmethod
    def get_ppts(cls, id):
        try:
            ppts = eval('UI_BLOCK_PPTS.' + id)
            #print("PROPS:", ppts)
        except:
            return None
        if not ppts and not isinstance(ppts, dict):
            return None
        return ppts()

    @classmethod
    def get_block(cls, idx):
        if idx > len(blocks):
            return None
        return blocks[idx]

    @classmethod
    def get_active_block(cls):
        if cls.active_block_index == -1:
            return None
        return blocks[cls.active_block_index]

    @classmethod
    def set_active_block(cls, idx):
        cls.active_block_index = idx
