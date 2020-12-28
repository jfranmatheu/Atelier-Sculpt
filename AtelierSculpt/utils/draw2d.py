from gpu_extras.batch import batch_for_shader
from gpu.shader import from_builtin
from gpu_extras.presets import draw_circle_2d, draw_texture_2d
from .geo2dutils import is_inside_2d_rect
from enum import Enum
from bpy.types import Image, Space, Area
from bpy.types import (
    SpaceClipEditor, SpaceConsole,
    SpaceDopeSheetEditor, SpaceFileBrowser,
    SpaceGraphEditor, SpaceImageEditor,
    SpaceInfo, SpaceNLA, SpaceNodeEditor,
    SpaceOutliner, SpacePreferences,
    SpaceProperties, SpaceSequenceEditor,
    SpaceTextEditor, SpaceView3D
)
import uuid
import bpy
import bgl
import blf
'''
import mouse
'''
from os.path import isfile
from string import Template
from ..utils.others import override_context


TEXT_DPI_DEFAULT = 72
TEXT_SHADOW_BLUR_LEVELS = [0, 3, 5]


# BUILT-IN SHADERS
shader_2d_image = from_builtin('2D_IMAGE')
shader_2d_color_unif = from_builtin('2D_UNIFORM_COLOR')
shader_2d_color_flat = from_builtin('2D_FLAT_COLOR')
shader_2d_color_smooth = from_builtin('2D_SMOOTH_COLOR')


class Color(Enum):
    Blender_Theme = None
    # BASIC
    Black = (0, 0, 0, 1)
    White = (1, 1, 1, 1)
    Red = (1, 0, 0, 1)
    Green = (0, 1, 0, 1)
    Blue = (0, 0, 1, 1)
    # CYAN DERIVATES
    Cyan = (0, 1, 1, 1)
    Aquamarine = (.498, 1, .831, 1)
    Turquoise = (.251, .878, .816, 1)
    # ORANGE DERIVATES
    Orange = (1, .647, 0, 1)
    Orange_Dark = (1, .549, 0, 1)
    Orange_Red = (1, .27, 0, 1)
    Gold = (1, .843, 0, 1)
    Coral = (1, .498, .314, 1)
    Tomato = (1, .388, .278, 1)


def rectangle_points(x, y, w, h):
    return (
        (x, y),
        (x+w, y),
        (x, y+h),
        (x+w, y+h)
    )


rectangle_indices = (
    (0, 1, 2),
    (2, 1, 3)
)


def Draw_2D_Rectangle(_posX, _posY, _width, _height, _color=[0, 0.5, 0.5, 1.0], _shader=shader_2d_color_unif):
    batch = batch_for_shader(_shader, 'TRIS', {"pos": rectangle_points(
        _posX, _posY, _width, _height)}, indices=rectangle_indices)
    _shader.bind()
    _shader.uniform_float("color", _color)
    bgl.glEnable(bgl.GL_BLEND)
    batch.draw(_shader)
    bgl.glDisable(bgl.GL_BLEND)


def Draw_2D_Lines(coords=[(0, 0, 0), (1, 1, 1)], _color=(1, 1, 0, 1), _shader=shader_2d_color_unif):
    batch = batch_for_shader(_shader, 'LINES', {"pos": coords})
    _shader.bind()
    _shader.uniform_float("color", _color)
    batch.draw(_shader)


def Draw_2D_Line(_p1, _p2, _color=(0, 0, 0, .8), _shader=shader_2d_color_unif):
    coords = [_p1, _p2]
    batch = batch_for_shader(_shader, 'LINES', {"pos": coords})
    _shader.bind()
    _shader.uniform_float("color", _color)
    batch.draw(_shader)

def Draw_2D_Point(_pos, _color = (0, 0, 0, .8), _shader = shader_2d_color_unif):
    coords = [_pos]
    batch = batch_for_shader(_shader, 'POINTS', {"pos": coords})
    _shader.bind()
    _shader.uniform_float("color", _color)
    batch.draw(_shader)

def Draw_2D_Points(coords, color=(1, .55, .15, .85), _shader=shader_2d_color_unif):
    batch = batch_for_shader(_shader, 'POINTS', {"pos": coords})
    _shader.bind()
    _shader.uniform_float("color", color)
    batch.draw(_shader)

def Draw_Text(_x, _y, _text, _size, _font_id=0, _r=1, _g=1, _b=1, _a=1):
    blf.color(_font_id, _r, _g, _b, _a)
    blf.position(_font_id, _x, _y, 0)  # -6/-6 para "o" #
    blf.size(_font_id, _size, 72)
    blf.draw(_font_id, _text)


def Draw_2D_Circle(_center, _radius, _segments=32, _color=(0, 0, 0, .8)):
    draw_circle_2d(_center, _color, _radius, _segments)


register_menu_template = """
import bpy

class ${name}(bpy.types.Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "$label"

    def draw(self, context):
        layout = self.layout
        layout.operator('render.render')

bpy.utils.register_class(${name})
"""

unregister_menu_template = """from bpy.utils import unregister_class
from bpy.types import ${name}
unregister_class(${name})
"""

register_pie_menu_template = """
import bpy

class ${name}(bpy.types.Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "$label"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator_enum("mesh.select_mode", "type")

bpy.utils.register_class(${name})
"""

unregister_pie_menu_template = """from bpy.utils import unregister_class
from bpy.types import ${name}
unregister_class(${name})
"""

register_panel_template = """
import bpy

class ${name}(bpy.types.Panel):
    # label is displayed at the center of the pie menu.
    bl_label = "$label"

    def draw(self, context):
        layout = self.layout
        layout.operator_enum("mesh.select_mode", "type")

bpy.utils.register_class(${name})
"""

unregister_panel_template = """from bpy.utils import unregister_class
from bpy.types import ${name}
unregister_class(${name})
"""


class MenuTypes(Enum):
    Default = ("VIEW3D_MT_", register_menu_template, unregister_menu_template)
    Pie = ("VIEW3D_MT_PIE_", register_pie_menu_template, unregister_pie_menu_template)
    Panel = ("VIEW3D_PT_POPOVER_", register_panel_template, unregister_panel_template)


class Menu():
    def __init__(self, item, menu_type=MenuTypes.Default):
        self.item = item
        self.menu_type = menu_type
        self.name = self.menu_type.value[0] + self.item.name.lower() + "_context_menu"
        code = Template(self.menu_type.value[1]).substitute(name=self.name, label=self.item.name)
        print(code)
        exec(code)

    def __call__(self, area_type, region_type):
        print("MENU::call")
        if self.menu_type == MenuTypes.Pie:
            print("PIE")
            bpy.ops.wm.call_menu_pie(override_context(area_type, region_type), name=self.name)
        elif self.menu_type == MenuTypes.Default:
            print("DEFAULT")
            bpy.ops.wm.call_menu(override_context(area_type, region_type), name=self.name)
            #clase = eval("bpy.types."+self.name)
            #bpy.context.window_manager.popup_menu(clase.draw, title="Greeting", icon='INFO')

    def __del__(self):
        try:
            exec(Template(menu_type.value[2]).substitute(classname=self.name))
        except ImportError as e:
            print("Menu class couldn't be found.", e)
        except NameError as e:
            print("Menu class name in not valid.", e)


class Label():
    def __init__(self, text, pos=[0, 0], size=14, color=Color.Black):
        self.text = text
        self.x, self.y = pos
        self.size = size
        self.color = list(color.value) if isinstance(color, Color) else list(color)
        self.context_menu = None

    def get_rgba(self):
        co = self.color
        return co[0], co[1], co[2], co[3]

    def get_text_dimensions(self):
        blf.size(0, self.size, TEXT_DPI_DEFAULT)
        return blf.dimensions(0, self.text)

    def set_alpha(self, alpha_value=1):
        self.color[3] = alpha_value

    def set_text(self, text):
        self.text = text

    def draw(self):
        Draw_Text(self.x, self.y, self.text, self.size, 0, *self.get_rgba())

    def draw_off(self, off_x, off_y):
        Draw_Text(self.x + off_x, self.y + off_y, self.text, self.size, 0, *self.get_rgba())

    def serialize(self):
        return {
            'text': self.text,
            'pos': tuple(self.x, self.y),
            'size': self.size,
            'color': tuple(self.color)
        }


class Alignment(Enum):
    Left = 0,
    Center = 1,
    Right = 2,
    Bottom = 3,
    Top = 4,
    Bottom_Left = 5,
    Bottom_Right = 6,
    Top_Left = 7,
    Top_Right = 8,


class Icon():
    def __init__(self, image, pos, size):
        self.image = image
        self.x, self.y = pos
        self.pos = pos
        self.width, self.width = size
        self._activate_image()
        self.name = self.image.name if self.image else ""
        self.path = self.image.filepath if self.image else ""
        self.context_menu = None

    def load_image_from_path(self, image_path):
        if not isfile(image_path):
            return None
        self.image = bpy.data.images.load(image_path, check_existing=False)
        self.name = self.image.name
        self.path = image_path
        self._activate_image()

    def load_image_from_data(self, image_name):
        self.image = bpy.data.images.get(image_name, None)
        if not self.image:
            return None
        self.name = image_name
        self.path = self.image.filepath
        self._activate_image()

    def _activate_image(self):
        if self.image and isinstance(self.image, Image):
            self.image.gl_load()

    def draw(self):
        self.image.gl_touch()
        draw_texture_2d(self.image.bindcode, self.pos, self.width, self.height)

    def serialize(self):
        return {
            'name': self.name,
            'path': self.path,
            'pos': tuple(self.x, self.y),
            'size': tuple(self.width, self.height)
        }

    def __del__(self):
        if self.image:
            self.image.gl_free()
            self.image.buffers_free()


class ToggleGroup():
    def __init__(self):
        self.buttons = []
        self.id = str(uuid.uuid4())

    def set_active(self, target, state):
        target.is_active = state

    def deactivate_buttons(self):
        for b in self.buttons:
            self.set_active(False)

    def toggle(self, target):
        self.deactivate_buttons()
        self.set_active(target, True)

    def add_button(self, button):
        if isinstance(button, Button):
            self.buttons.append(button)
            button.toggle_group = self

    def add_buttons(self, buttons):
        if isinstance(buttons, list):
            for b in buttons:
                self.add_button(b)

    def remove_button(self, button):
        if isinstance(button, int):
            self.buttons.pop(button)
        elif isinstance(button, Button):
            self.buttons.remove(button)


class Button():
    buttons = []

    def __init__(self, pos, size, color, on_hover_color, fun, label=None, icon=None):
        self.id = uuid.uuid4().__str__()
        self.name = "Button_" + str(len(Button.buttons))
        self.x, self.y = pos
        self.width, self.height = size
        self.color = list(color.value) if isinstance(color, Color) else list(color)
        self.color_on_hover = list(on_hover_color.value) if isinstance(on_hover_color, Color) else list(on_hover_color)
        self.on_click = fun
        self.on_click_args = {}
        self.is_active = False
        self.on_hover = False
        self.label = label
        self.icon = icon
        self.context_menu = Menu(self)
        self.toggle_group = None
        #self._parent = None

        Button.buttons.append(self)

    def set_label(self, label):
        if isinstance(label, Label):
            return None
        self.label = label

    def set_icon(self, icon):
        if isinstance(icon, Icon):
            return None
        self.icon = icon

    def set_context_menu(self, context_menu):
        if isinstance(context_menu, Menu):
            return None
        self.context_menu = context_menu

    # def _set_parent(self, parent):
    #    if isinstance(parent, Canvas):
    #        self._parent = parent

    def add_label(self, text='Text', size=14, alignment=Alignment.Center, color=(0, 0, 0, 1)):
        if self.label or not isinstance(alignment, Alignment):
            return None
        self.label = Label(text, [0, 0], size, color)
        width, height = self.label.get_text_dimensions()
        if alignment == Alignment.Center:
            self.label.x = int(width / 2.0) - 2
            self.label.y = int(self.height / 2.0 - height / 2.0)
        return self.label

    def add_icon(self, image, pos, size):
        if self.icon:
            return None
        self.icon = Icon(image, pos, size)

    def add_icon_from_data(self, image_name, pos, size):
        add_icon(None, pos, size)
        self.icon.load_image_from_data(image_name)

    def add_icon_from_path(self, image_path, pos, size):
        add_icon(None, pos, size)
        self.icon.load_image_from_path(image_path)

    def set_alpha(self, alpha_value=1):
        self.color[3] = self.color_on_hover[3] = alpha_value
        return self

    def move(self, pos):
        self.x = int(pos[0] - self.width / 2.0)
        self.y = int(pos[1] - self.height / 2.0)

    def draw(self):
        Draw_2D_Rectangle(
            self.x, self.y,
            self.width, self.height,
            self.color if not self.is_active and not self.on_hover else self.color_on_hover
        )
        if self.icon:
            self.image.draw_off(self.x, self.y)
        if self.label:
            self.label.draw_off(self.x, self.y)

    def __call__(self):
        #print("Button::call", self)
        try:
            self.on_click()
        except Exception as e:
            print(e)
        finally:
            if self.toggle_group:
                self.toggle_group.toggle(self.index_toggle_group)

    def evaluate(self):
        Button.deactivate_buttons()
        self.set_active(True)
        eval(self.on_click)()

    def serialize(self):
        return {
            'id': self.id,
            'toggle_group_index': self.toggle_group.id if self.toggle_group else None,
            'pos': tuple(self.x, self.y),
            'size': tuple(self.width, self.height),
            'color': tuple(self.color),
            'color_on_hover': tuple(self.color_on_hover),
            'on_click': self.on_click,  # TODO: ops, looks for a string representation of this code maybe?
            'label': self.label.serialize(),
            'icon': self.icon.serialize()
        }


class Space(Enum):
    VIEW_3D = bpy.types.SpaceView3D
    IMAGE_EDITOR = bpy.types.SpaceImageEditor
    NODE_EDITOR = bpy.types.SpaceNodeEditor
    SEQUENCE_EDITOR = bpy.types.SpaceSequenceEditor
    CLIP_EDITOR = bpy.types.SpaceClipEditor
    DOPESHEET_EDITOR = bpy.types.SpaceDopeSheetEditor
    GRAPH_EDITOR = bpy.types.SpaceGraphEditor
    NLA_EDITOR = bpy.types.SpaceNLA
    TEXT_EDITOR = bpy.types.SpaceTextEditor
    CONSOLE = bpy.types.SpaceConsole
    INFO = bpy.types.SpaceInfo
    OUTLINER = bpy.types.SpaceOutliner
    PROPERTIES = bpy.types.SpaceProperties
    FILE_BROWSER = bpy.types.SpaceFileBrowser
    PREFERENCES = bpy.types.SpacePreferences


class Region(Enum):
    WINDOW = 'WINDOW'
    HEADER = 'HEADER'
    TOOL_HEADER = 'TOOL_HEADER'
    UI = 'UI'
    TOOLS = 'TOOLS'
    TOOL_PROPS = 'TOOL_PROPS'
    FOOTER = 'FOOTER'
    CHANNELS = 'CHANNELS'
    TEMPORARY = 'TEMPORARY'
    PREVIEW = 'PREVIEW'
    HUD = 'HUD'
    NAVIGATION_BAR = 'NAVIGATION_BAR'
    EXECUTE = 'EXECUTE'

'''
class Canvas():
    def __init__(self, space_type=Space.VIEW_3D, region_type=Region.WINDOW, win_x=0, win_y=0):
        print("CANVAS::Init")
        self.buttons = []
        self.labels = []
        self.images = []
        self.custom = []
        self.space = space_type.value
        self.region_type = region_type.value
        self.area_type = str(space_type).split('.')[1]
        self.draw_type = 'POST_PIXEL'
        self._handler = None
        self.item_on_hover = None
        self.win_x = win_x
        self.win_y = win_y
        self.has_modal = False
        self.mouse_pos = [-1, -1]
        self.dragging = False

    def use_for_custom_operator(self):
        CanvasOperator.canvas = self
        return self

    def start(self, args=()):
        if not self.space:
            return None
        if not isinstance(args, tuple):
            return None
        if self._handler:
            return None
        print("CANVAS::Start")
        if not args:
            args = (bpy.context,)
        self._handler = self.space.draw_handler_add(self.draw, args, self.region_type, self.draw_type)
        if not self.has_modal:
            mouse.on_click(self.event, args=())
            mouse.on_right_click(self.context_menu, args=())
            #mouse.on_middle_click(self.drag_item, args=())
            mouse.on_button(self.drag_item, args=(), buttons=('middle'), types=('down'))
        return self

    def stop(self):
        if not self._handler:
            return None
        print("CANVAS::Stop")
        self.space.draw_handler_remove(self._handler, self.region_type)
        #del self._handler

    def new_button(self, pos, size, color, on_hover_color, fun, label=None, icon=None):
        return self.add_button(Button(pos, size, color, on_hover_color, fun, label, icon))

    def add_button(self, button):
        if isinstance(button, Button):
            self.buttons.append(button)
            # button._set_parent(self)
        return button

    def new_image(self, image, pos, size):
        return self.add_image(Icon(image, pos, size))

    def add_image(self, image):
        if isinstance(button, Image):
            self.images.append(image)
        return image

    def new_label(self, text, pos, size, color):
        return self.add_label(Label(text, pos, size, color))

    def add_label(self, label):
        if isinstance(button, Label):
            self.labels.append(label)
        return label

    def check_on_hover(self, item, mouse):
        return is_inside_2d_rect(mouse, item.x, item.y, item.width, item.height)

    # Limite drawing canvas to the target area you specify.
    # Use area type or context to specify the area target. None to use all them.

    def lock_to_area(self, area_target):
        # Area.
        if isinstance(area_target, Area) and area_target.type == self.area_type:
            self.area = area_target
        # Context.
        elif hasattr(area_target, "area"):
            if area_target.area.type == self.area_type:
                self.area = area_target.area
        # None.
        elif area_target is None and hasattr(self, "area"):
            del self.area
        return self

    def event(self):
        if not self.item_on_hover:
            print("CANVAS::Nothing to click")
            return False
        #bpy.ops.fake.click_op(override_context(self.area_type, self.region_type), 'INVOKE_DEFAULT')
        print("CANVAS::ON CLICK!")
        self.item_on_hover()
        return True

    def context_menu(self):
        if not self.item_on_hover:
            return False
        if not self.item_on_hover.context_menu:
            return False
        print("CANVAS::Context Menu")
        self.item_on_hover.context_menu(self.area_type, self.region_type)
        return True

    def drag_item(self):
        if not self.item_on_hover:
            return False
        print("CANVAS::Drag")
        self.dragging = True
        while mouse.is_pressed(button=mouse.MIDDLE):
            self.drag()
        self.dragging = False
        return True

    def drag(self):
        self.item_on_hover.move(self.mouse_pos)

    def draw(self, context):
        if hasattr(self, "area"):
            if self.area != context.area:
                return
        if not self.has_modal:
            # self.event()
            # NOTE: We are supposing all screens are 16:9_1080p.
            # Get mouse position.
            mouse_pos = list(mouse.get_position())
            # Invert Y axis.
            mouse_pos[1] -= 1080  # if using event from modal this should be skipped.
            # Apply editor/space window offset.
            mouse_pos[0] -= self.win_x
            mouse_pos[1] += self.win_y  # if using event from modal this should be -=.
            # Detects if it's a second monitor.
            if mouse_pos[0] > 1920:
                mouse_pos[0] -= 1920  # TODO: multiply per int(mouse_pos[0] / 1920) if > 2 screens.
            mouse_pos[0] = abs(mouse_pos[0])
            mouse_pos[1] = abs(mouse_pos[1])
            #print(mouse_pos[0], mouse_pos[1])
            self.mouse_pos = mouse_pos
        print(self.mouse_pos)
        for i in self.images:
            i.draw()
        if not self.dragging:
            self.item_on_hover = None
        for b in self.buttons:
            if self.check_on_hover(b, self.mouse_pos):
                #print("ON HOVER!")
                b.on_hover = True
                self.item_on_hover = b
            else:
                b.on_hover = False
            b.draw()
        for t in self.labels:
            t.draw()
        for c in self.custom:
            c.draw()

    @staticmethod
    def serialize_list(list):
        serialized_items = []
        for item in self.list:
            serialized_items.append(item.serialize())
        return serialized_items

    def serialize(self):
        return {
            # 'id' : self.id,
            'space_type': self.space_type,
            'space': self.space,
            'region_type': self.region_type,
            'draw_type': self.draw_type,
            'buttons': Canvas.serialize_list(self.buttons),
            'images': Canvas.serialize_list(self.images),
            'labels': Canvas.serialize_list(self.labels)
        }

    def __del__(self):
        self.stop()


class CanvasModal(Canvas):
    class Modal(bpy.types.Operator):
        bl_idname = "canvas.modal"
        bl_label = ""

        canvas = None
        stop = False

        def execute(self, context):
            print("EXECUTE")
            self.dragging = False
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}

        def modal(self, context, event):
            # print("MODAL")
            self.canvas.mouse_pos = [event.mouse_region_x, event.mouse_region_y]
            if self.dragging:
                print("MODAL::Dragging...")
                if event.type == 'MIDDLEMOUSE' and event.value == 'RELEASE':
                    self.dragging = False
                    return {'PASS_THROUGH'}
                self.canvas.drag_item()
            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                if self.canvas.event():
                    print("LEFT!")
                    return {'RUNNING_MODAL'}
            elif event.type == 'RIGHTMOUSE' and event.value == 'PRESS':
                if self.canvas.context_menu():
                    print("RIGHT!")
                    return {'RUNNING_MODAL'}
            elif event.type == 'MIDDLEMOUSE' and event.value == 'PRESS':
                if self.canvas.item_on_hover:
                    print("MIDDLE!")
                    self.dragging = True
                    return {'RUNNING_MODAL'}
            elif event.type == 'ESC':
                print("ESC!")
                self.canvas.stop()
                return {'FINISHED'}
            return {'PASS_THROUGH'}

    def __init__(self, space_type=Space.VIEW_3D, region_type=Region.WINDOW):
        self.buttons = []
        self.labels = []
        self.images = []
        self.custom = []
        self.space = space_type.value
        self.region_type = region_type.value
        self.area_type = str(space_type).split('.')[1]
        self.draw_type = 'POST_PIXEL'
        self._handler = None
        self.item_on_hover = None
        self.has_modal = True
        self.mouse_pos = [-1, -1]
        self.dragging = False

        self.Modal.canvas = self
        bpy.utils.register_class(CanvasModal.Modal)
        self._modal = bpy.ops.canvas.modal

    def start(self, args=()):
        super().start(args)
        self._modal()

    def stop(self):
        super().stop()
        self.Modal.stop = True
        self.Modal.canvas = None
        del self

    def drag_item(self):
        print("CANVAS::Drag Item...")
        self.item_on_hover.move(self.mouse_pos)

    def __del__(self):
        super().__del__()
        del self._modal
        bpy.utils.unregister_class(CanvasModal.Modal)


canvas_operator_property_group = """
from bpy.types import PropertyGroup, WindowManager as wm
from bpy.utils import register_class
from bpy.props import PointerProperty
class PG_${name}(PropertyGroup):
    modal = []
    canvas = []
register_class(PG_${name})
wm.${name} = PointerProperty(type=PG_${name})
"""


class CanvasOperator(Canvas, bpy.types.Operator):
    bl_idname = "canvas.operator"
    bl_label = ""

    canvas = Canvas()

    # def __init__(self, space_type=Space.VIEW_3D, region_type=Region.WINDOW, win_x=0, win_y=0):
    #    super().__init__(space_type, region_type, 0, 0)

    def execute(self, context):
        print("EXECUTE")
        #self.index = len(pgs)
        #code = Template(canvas_operator_property_group).substitute(name="CanvasOperator_"+str(self.index))
        # exec(code)
        # self.pgs.append()
        if CanvasOperator.canvas is None:
            print("No canvas on operator")
            return {'FINISHED'}

        self.canvas = CanvasOperator.canvas  # self.__init__()
        CanvasOperator.canvas = None
        self.canvas.has_modal = True
        self.canvas.start()

        self.dragging = False
        self.area = context.area
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        # print("MODAL")
        if not self.canvas:
            return {'FINISHED'}
        if self.area != context.area:
            self.canvas.stop()
            return {'FINISHED'}
        self.area.tag_redraw()
        self.canvas.mouse_pos = [event.mouse_region_x, event.mouse_region_y]
        if self.dragging:
            print("MODAL::Dragging...")
            if event.type == 'MIDDLEMOUSE' and event.value == 'RELEASE':
                self.dragging = False
                return {'RUNNING_MODAL'}
            self.canvas.drag()
            return {'PASS_THROUGH'}
        elif event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            if self.canvas.event():
                print("LEFT!")
                return {'RUNNING_MODAL'}
        elif event.type == 'RIGHTMOUSE' and event.value == 'PRESS':
            if self.canvas.context_menu():
                print("RIGHT!")
                return {'RUNNING_MODAL'}
        elif event.type == 'MIDDLEMOUSE' and event.value == 'PRESS':
            if self.canvas.item_on_hover:
                print("MIDDLE!")
                self.dragging = True
                return {'RUNNING_MODAL'}
        elif event.type == 'ESC':
            print("ESC!")
            self.canvas.stop()
            return {'FINISHED'}
        return self.loop(context, event)

    def loop(self, context, event):
        return {'PASS_THROUGH'}
'''

def Draw_Texture(_bincode, _pos, _width, _height):
    draw_texture_2d(_bincode, _pos, _width, _height)

def Draw_Image_Texture(_image, _pos, _width, _height):
    try:
        if _image.gl_load():
            raise Exception()
    except:
        pass
    draw_texture_2d(_image.bindcode, _pos, _width, _height)

shader_img = shader_2d_image
def Draw_Image(image, _pos, _width, _height, _use_transparency = False, _flipX = False, _flipY = False):
    off_x, off_y =  _pos
    if image.gl_load():
        raise Exception()
     # bottom left, top left, top right, bottom right
    if _flipX:
        vertices = (
            (off_x + _width,    _height + off_y),
            (off_x + _width,    off_y),
            (off_x,             off_y),
            (off_x,             _height + off_y)
        )
    elif _flipY:
        vertices = (
            (off_x,             off_y),
            (off_x,             _height + off_y),
            (off_x + _width,    _height + off_y),
            (off_x + _width,    off_y)
        )
    else:
        vertices = (
            (off_x,             _height + off_y),
            (off_x,             off_y),
            (off_x + _width,    off_y),
            (off_x + _width,    _height + off_y) 
        )
    batch_img = batch_for_shader(shader_img, 'TRI_FAN', { "pos" : vertices, "texCoord": ((0, 1), (0, 0), (1, 0), (1, 1)) },)
    #if _image is not None:
    try:
        if _use_transparency:
            bgl.glEnable(bgl.GL_BLEND)
            # TRANSPARENCIA
            bgl.glBlendFunc(bgl.GL_SRC_COLOR, bgl.GL_ONE)
            #bgl.glBlendFunc(bgl.GL_SRC_COLOR, bgl.GL_ONE_MINUS_SRC1_ALPHA) # GL_DST_ALPHA # GL_ONE_MINUS_CONSTANT_ALPHA # GL_SRC_ALPHA # GL_ONE
            # AUMENTA CONTRASTE Y SATURACION
            #bgl.glBlendFunc(bgl.GL_ONE_MINUS_CONSTANT_ALPHA, bgl.GL_SRC_COLOR)
            # bgl.glBlendFunc(bgl.GL_ONE, bgl.GL_SRC_COLOR)
            # bgl.glBlendFunc(bgl.GL_SRC_COLOR, bgl.GL_CONSTANT_ALPHA)
        if image.ref.in_front:
            bgl.glDisable(bgl.GL_DEPTH_TEST) # DELANTE
        else:
            bgl.glEnable(bgl.GL_DEPTH_TEST) # DETRÁS
        bgl.glActiveTexture(bgl.GL_TEXTURE0)
        bgl.glBindTexture(bgl.GL_TEXTURE_2D, image.bindcode)
        #bgl.glColor4ub(0,0,0, 120)
        #bgl.glTexEnvf(bgl.GL_TEXTURE_2D, bgl.GL_SOURCE0_ALPHA, bgl.GL_TEXTURE0)
        #bgl.glBlendFunc(bgl.GL_SRC_ALPHA, bgl.GL_ONE_MINUS_SRC_ALPHA)
        shader_img.bind()
        shader_img.uniform_int("image", 0)
        batch_img.draw(shader_img)
        bgl.glDisable(bgl.GL_BLEND)
        bgl.glDisable(bgl.GL_DEPTH_TEST)
        return True
    except:
        return False
