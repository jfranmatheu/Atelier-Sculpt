from enum import Enum

class CursorIcon(Enum):
    DEFAULT       =      'DEFAULT'
    NONE          =         'NONE'
    WAIT          =         'WAIT'
    CROSSHAIR     =    'CROSSHAIR'
    MOVE_X        =       'MOVE_X'
    MOVE_Y        =       'MOVE_Y'
    KNIFE         =        'KNIFE'
    TEXT          =         'TEXT'
    PAINT_BRUSH   =  'PAINT_BRUSH'
    PAINT_CROSS   =  'PAINT_CROSS'
    HAND          =         'HAND'
    SCROLL_X      =     'SCROLL_X'
    SCROLL_Y      =     'SCROLL_Y'
    EYEDROPPER    =   'EYEDROPPER'
    DOT           =          'DOT'
    ERASER        =       'ERASER'

class Cursor:
    @staticmethod
    def set_icon(context, cursor = CursorIcon.DEFAULT):
        context.window.cursor_modal_set(cursor.value)
        #for wm in bpy.data.window_managers:
        #    for win in wm.windows:
        #        win.cursor_modal_set(cursor)

    @staticmethod
    def wrap(context, x, y):
        context.window.cursor_warp(x, y)