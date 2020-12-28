# Copyright (C) 2019 Juan Fran Matheu G.
# Contact: jfmatheug@gmail.com 
from ...utils.draw2d import Draw_Text, Draw_Image_Texture, Draw_Image, Draw_2D_Rectangle, Draw_2D_Line, Draw_2D_Point
from ...utils.geo2dutils import is_inside_2d_rect, Vector
from bpy.props import StringProperty, BoolProperty, FloatProperty, FloatVectorProperty, IntProperty, EnumProperty
from bpy.types import PropertyGroup
import blf


def Reference_Events(self, context, event):
    # Cursor is inside my reference?
    if self.moving:
        #print("Moving")
        self.ref.position = Vector((self.mousePos[0]-self.ref.size[0]/2, self.mousePos[1]-self.ref.size[1]/2)) - self.offset
        if (event.type not in {'LEFTMOUSE'} and event.value not in {'CLICK_DRAG', 'PRESS'}) or event.type == 'MIDDLEMOUSE':
            context.window_manager.bas_references.moving_reference = False
            self.moving = False
        else:
            return True
    elif is_inside_2d_rect(self.mousePos, *self.ref.position, self.ref.size[0], self.ref.size[1]):
        #print("Hovering")
        if event.type == 'LEFTMOUSE':
            off = self.mousePos - Vector(self.ref.position)
            self.offset = Vector((off[0]-self.ref.size[0]/2, off[1]-self.ref.size[1]/2))
            self.moving = True
            context.window_manager.bas_references.moving_reference = True
            return True
        #elif event.type == 'S':
    return False

def interactive_draw_reference_callback_px(self, context):
    try:
        if self.dragging:
            Draw_Text(100, 50, "Ctrl: Scale from center     |       Shift: Keep aspect ratio", 32, 0)
            if self.using_ctrl:
                #if self.wider:
                height = (self.mousePos[1] - self.midPoint[1]) * 2
                width = height * self.proportion
                #else:
                #width = (self.mousePos[0] - self.midPoint[0]) * 2
                #height = width * self.proportion

                self.center = Vector((self.midPoint[0] - width/2, self.midPoint[1] - height/2))
                Draw_Image_Texture(self.image, self.center, width, height)
            else:
                if self.using_shift:
                    #if self.wider:
                    height = self.mousePos[1] - self.firstPos[1]
                    width = height * self.proportion
                    #else:
                    #width = self.mousePos[0] - self.firstPos[0]
                    #height = width * self.proportion
                else:
                    width = self.mousePos[0] - self.firstPos[0]
                    height = self.mousePos[1] - self.firstPos[1]
                Draw_Image_Texture(self.image, self.firstPos, width, height)

            if not self.using_ctrl:
                # TEXT
                #blf.size(0, self.textSize, 72)
                #textsize = blf.dimensions(0, self.text)
                #if abs(textsize[0]+20) < abs(width) and abs(textsize[1]+20) < abs(height):
                #    alpha = self.textColor[3]
                #elif abs(textsize[0]) > abs(width) or abs(textsize[1]) > abs(height):
                #    alpha = 0
                #else:
                #    alpha = min(clip(abs(width), textsize[0]/abs(width), (20+textsize[0])/abs(width)), clip(abs(height), textsize[1]/abs(height), (20+textsize[1])/abs(height)))
                #textY = self.firstPos[1] + (height - textsize[1]) * .5
                #textX = self.firstPos[0] + (width - textsize[0]) * .5
                #Draw_Text(textX, textY, self.text, self.textSize, 0, self.textColor[0], self.textColor[1], self.textColor[2], alpha)

                Draw_2D_Line(Vector((self.firstPos[0], self.firstPos[1])), Vector((width+self.firstPos[0], self.firstPos[1]))) # bot
                Draw_2D_Line(Vector((self.firstPos[0], self.firstPos[1])), Vector((self.firstPos[0], self.firstPos[1] + height))) # left
                Draw_2D_Line(Vector((self.firstPos[0], self.firstPos[1] + height)), Vector((width+self.firstPos[0], self.firstPos[1] + height))) # top
                Draw_2D_Line(Vector((self.firstPos[0] + width, self.firstPos[1] + height)), Vector((width+self.firstPos[0], self.firstPos[1]))) # right
                Draw_2D_Point(self.firstPos, (.8, .6, .2, 1))
                Draw_2D_Point(self.mousePos, (.8, .6, .2, 1))
            else:
                Draw_2D_Point(self.mousePos, (.8, .6, .2, 1))
                Draw_2D_Point(self.midPoint, (.8, .6, .2, 1))

            self.width = width
            self.height = height
        else:
            Draw_2D_Point(self.mousePos, (.8, .6, .2, 1))
    except:
        return

def draw_reference_callback_px(self, context):
    try:
        if context.area != self.area:
            return
        if self.ref.signal != 'H' and context.window_manager.bas_references.hide_all == False:
            # IS THE RIGHT MODE ?
            if self.ref.mode == 'ALL' or context.mode == self.ref.mode:
                coords = self.ref.position
                width = self.ref.size[0]
                height = self.ref.size[1]
                # DRAW IMAGE
                Draw_Image(self.image, coords, width, height, self.ref.use_transparency, self.flipX, self.flipY)
                #Draw_Texture(self.image, self.ref.position, width, height)
                # DRAW OUTLINE
                if self.ref.use_outline:
                    lineColor = self.ref.outline_color
                    #Draw_2D_Line_GL((coords[0], coords[1]), (width+coords[0], coords[1]), 2, lineColor)
                    #Draw_2D_Line_GL((coords[0], coords[1]), (coords[0], coords[1] + height), 2, lineColor)
                    #Draw_2D_Line_GL((coords[0], coords[1] + height), (width+coords[0], coords[1] + height), 2, lineColor)
                    #Draw_2D_Line_GL((coords[0] + width, coords[1] + height), (width+coords[0], coords[1]), 2, lineColor)
                    Draw_2D_Line(Vector((coords[0], coords[1])), Vector((width+coords[0], coords[1])), lineColor) # bot
                    Draw_2D_Line(Vector((coords[0], coords[1])), Vector((coords[0], coords[1] + height)), lineColor) # left
                    Draw_2D_Line(Vector((coords[0], coords[1] + height)), Vector((width+coords[0], coords[1] + height)), lineColor) # top
                    Draw_2D_Line(Vector((coords[0] + width, coords[1] + height)), Vector((width+coords[0], coords[1])), lineColor) # right
                # DRAW LABEL
                if self.ref.use_label:
                    if self.ref.label_align_to == 'TOP':
                        x = self.ref.position[0]
                        y = self.ref.position[1] + height
                    else:
                        x = self.ref.position[0]
                        y = self.ref.position[1] - self.ref.label_thickness

                    # DRAW LABEL TEXT
                    tColor = self.ref.label_text_color
                    blf.size(0, self.ref.label_text_size, 72)
                    textsize = blf.dimensions(0, self.ref.label_text)
                    textY = y + (self.ref.label_thickness - textsize[1]) * .5
                    #textY = y + self.ref.label_text_size/2
                    if self.ref.label_text_align == 'LEFT':
                        textX = coords[0] + context.window_manager.bas_references.label_text_padding
                    elif self.ref.label_text_align == 'CENTER':
                        textX = coords[0] + (width - textsize[0]) * .5
                    elif self.ref.label_text_align == 'RIGHT':
                        textX = coords[0] + width - textsize[0] - context.window_manager.bas_references.label_text_padding
                    
                    Draw_2D_Rectangle(x, y, width, self.ref.label_thickness, self.ref.label_color)
                    
                    Draw_Text(textX, textY, str(self.ref.label_text), self.ref.label_text_size, 0, 
                        self.ref.label_text_color[0], self.ref.label_text_color[1], self.ref.label_text_color[2], self.ref.label_text_color[3])
    except:
        pass
              
    

# CONSTRUCTOR DE REFERENCIAS
class Create_Reference:
    image_path : StringProperty(name="Image Path", subtype='FILE_PATH')
    label_text : StringProperty(name="Label Text")

    def __init__(self):
        wm = bpy.context.window_manager.bas_references
        self.image_path = wm.image_path
        self.label_text = wm.label_text
        # saved external or internal
        # text
        # use label
        # label size
        # label position
        # etc

    #def __repr__(self):
    #    return "Create_Reference[%s, %i[], %i[], %i[]]" % (self.stage_Name, self.relative_Values, self.constant_Values, self.brush_Values)
