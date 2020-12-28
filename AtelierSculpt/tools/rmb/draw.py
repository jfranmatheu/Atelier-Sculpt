import blf
import bgl
import gpu
from gpu_extras.batch import batch_for_shader

vertex_shader = '''
    uniform mat4 ModelViewProjectionMatrix;

    in vec2 pos;
    in vec4 color;
    out vec4 col;

    void main()
    {
    	gl_Position = ModelViewProjectionMatrix * vec4(pos, 0.0, 1.0);
        col = color;
    }
'''

fragment_shader = '''
    in vec4 col;

    void main()
    {
        gl_FragColor = col;
    }
'''

rectpoints = (
    (0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)
)

circlepoints = (
( 0.0 ,  1.0 ),
( -0.19509 ,  0.980785 ),
( -0.382683 ,  0.92388 ),
( -0.55557 ,  0.83147 ),
( -0.707107 ,  0.707107 ),
( -0.83147 ,  0.55557 ),
( -0.92388 ,  0.382683 ),
( -0.980785 ,  0.19509 ),
( -1.0 ,  0.0 ),
( -0.980785 ,  -0.19509 ),
( -0.92388 ,  -0.382683 ),
( -0.83147 ,  -0.55557 ),
( -0.707107 ,  -0.707107 ),
( -0.55557 ,  -0.83147 ),
( -0.382683 ,  -0.92388 ),
( -0.19509 ,  -0.980785 ),
( 0.0 ,  -1.0 ),
( 0.195091 ,  -0.980785 ),
( 0.382684 ,  -0.923879 ),
( 0.555571 ,  -0.831469 ),
( 0.707107 ,  -0.707106 ),
( 0.83147 ,  -0.55557 ),
( 0.92388 ,  -0.382683 ),
( 0.980785 ,  -0.195089 ),
( 1.0 ,  0.0 ),
( 0.980785 ,  0.195091 ),
( 0.923879 ,  0.382684 ),
( 0.831469 ,  0.555571 ),
( 0.707106 ,  0.707108 ),
( 0.555569 ,  0.83147 ),
( 0.382682 ,  0.92388 ),
( 0.195089 ,  0.980786 ),
)

circleindices = (
( 1 ,  0 ,  31 ),
( 1 ,  31 ,  30 ),
( 2 ,  1 ,  30 ),
( 15 ,  13 ,  18 ),
( 30 ,  29 ,  28 ),
( 3 ,  30 ,  28 ),
( 4 ,  3 ,  28 ),
( 27 ,  5 ,  28 ),
( 3 ,  2 ,  30 ),
( 5 ,  27 ,  26 ),
( 6 ,  5 ,  26 ),
( 6 ,  26 ,  25 ),
( 7 ,  6 ,  25 ),
( 7 ,  25 ,  24 ),
( 8 ,  7 ,  24 ),
( 8 ,  24 ,  23 ),
( 9 ,  8 ,  23 ),
( 9 ,  23 ,  22 ),
( 10 ,  9 ,  22 ),
( 10 ,  22 ,  21 ),
( 11 ,  10 ,  21 ),
( 11 ,  21 ,  20 ),
( 12 ,  11 ,  20 ),
( 12 ,  20 ,  19 ),
( 13 ,  12 ,  19 ),
( 13 ,  19 ,  18 ),
( 17 ,  15 ,  18 ),
( 14 ,  13 ,  15 ),
( 15 ,  17 ,  16 ),
( 5 ,  4 ,  28 ),
)

def draw_callback_px(self, context):
    # circle graphic, text, and slider
    brush = context.tool_settings.sculpt.brush
    capabilities = brush.sculpt_capabilities
    unify_settings = context.tool_settings.unified_paint_settings
    strength = unify_settings.strength if self.uni_str else self.brush.strength
    size = unify_settings.size if self.uni_size else self.brush.size
    smooth = brush.auto_smooth_factor if capabilities.has_auto_smooth else None

    vertices = []
    colors = []
    indices = []

    showText = ""
    text = ""
    font_id = 0
    font_id_Size = 0
    do_text = False
    do_textSize = False
    #do_textSmooth = False

    if self.graphic:
        # circle inside brush
        starti = len(vertices)
        for x, y in circlepoints:
            try:
                vertices.append((int(size * x) + self.cur[0], int(size * y) + self.cur[1]))
            except:
                pass
            colors.append((self.brushcolor[0], self.brushcolor[1], self.brushcolor[2], strength * 0.25))
        for i in circleindices:
            indices.append((starti + i[0], starti + i[1], starti + i[2]))

    # STRENGTH
    if self.text != 'NONE' and self.doingstr:
        showText = "Strength: "
        if self.text == 'MEDIUM':
            fontsize = 16
        elif self.text == 'LARGE':
            fontsize = 22
        else:
            fontsize = 12

        blf.size(font_id, fontsize, 72)
        # Fonts with Shadow
        #blf.shadow(font_id, 0, 0.0, 0.0, 0.0, 1.0)
        #blf.enable(font_id, blf.SHADOW)

        #if strength < 0.001:
        #    text = "0"
        #else:
        text = str(strength)[0:4]

        textsize = blf.dimensions(font_id, text)

        xpos = self.start[0] - self.offset[0] - 150
        ypos = self.start[1] + self.offset[1]
        blf.position(font_id, xpos, ypos, 0)

        # rectangle behind text
        starti = len(vertices)
        # rectpoints: (0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)
        for x, y in rectpoints:
            vertices.append((int(textsize[0] * x) + xpos, int(textsize[1] * y) + ypos))
            colors.append((self.backcolor.r, self.backcolor.g, self.backcolor.b, 0)) # 0.5 to 0 so BG is invisible
        indices.extend((
            (starti, starti+1, starti+2), (starti+2, starti, starti+3)
        ))

        do_text = True

    # SIZE
    if self.textSize != 'NONE' and self.doingrad:
        showText = "Size: "
        if self.text == 'MEDIUM':
            fontsize = 16
        elif self.text == 'LARGE':
            fontsize = 22
        else:
            fontsize = 12

        blf.size(font_id_Size, fontsize, 72)
        # Fonts with Shadow
        #blf.shadow(font_id_Size, 0, 0.0, 0.0, 0.0, 1.0)
        #blf.enable(font_id_Size, blf.SHADOW)

        if size < 0.001:
            text = "0"
        else:
            text = str(size)[0:5]
        textsize = blf.dimensions(font_id_Size, text)

        xpos = self.start[0] - self.offset[0] - 100
        ypos = self.start[1] #+ self.offset[1]
        blf.position(font_id_Size, xpos, ypos, 0)

        # rectangle behind text
        starti = len(vertices)
        # rectpoints: (0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)
        for x, y in rectpoints:
            vertices.append((int(textsize[0] * x) + xpos, int(textsize[1] * y) + ypos))
            colors.append((self.backcolor.r, self.backcolor.g, self.backcolor.b, 0)) # 0.5 to 0  (Background Color)
        indices.extend((
            (starti, starti+1, starti+2), (starti+2, starti, starti+3)
        ))

        do_textSize = True
    try:
        shader = gpu.types.GPUShader(vertex_shader, fragment_shader)
        batch = batch_for_shader(shader, 'TRIS', {"pos":vertices, "color":colors}, indices=indices)
    except:
        return

    bgl.glEnable(bgl.GL_BLEND)
    shader.bind()
    batch.draw(shader)
    bgl.glDisable(bgl.GL_BLEND)

    if do_text:
        blf.draw(font_id, showText + text)
        #blf.disable(font_id, blf.SHADOW)

    if do_textSize:
        blf.draw(font_id_Size, showText + text)
        #blf.disable(font_id_Size, blf.SHADOW)
    
def draw_callback_px_2(self, context):
    # circle graphic, text, and slider
    brush = context.tool_settings.sculpt.brush
    capabilities = brush.sculpt_capabilities
    unify_settings = context.tool_settings.unified_paint_settings
    size = unify_settings.size if self.uni_size else self.brush.size
    smooth = brush.auto_smooth_factor if capabilities.has_auto_smooth else None

    vertices = []
    colors = []
    indices = []

    smoothText = "Smooth: "
    text = ""
    font_id = 0
    do_textSmooth = False

    if self.graphic:
        # circle inside brush
        starti = len(vertices)
        for x, y in circlepoints:
            vertices.append((int(size * x) + self.cur[0], int(size * y) + self.cur[1]))
            colors.append((self.brushcolor[0], self.brushcolor[1], self.brushcolor[2], smooth * 0.25))
        for i in circleindices:
            indices.append((starti + i[0], starti + i[1], starti + i[2]))

    # SMOOTH
    if self.textSmooth != 'NONE' and self.doingsmooth:
        if self.textSmooth == 'MEDIUM':
            fontsize = 16
        elif self.textSmooth == 'LARGE':
            fontsize = 22
        else:
            fontsize = 12

        blf.size(font_id, fontsize, 72)
        # Font shadow
        #blf.shadow(font_id, 0, 0.0, 0.0, 0.0, 1.0)
        #blf.enable(font_id, blf.SHADOW)

        if smooth < 0.001:
            text = "0"
        else:
            text = str(smooth)[0:4] # 5 to 4
        textsize = blf.dimensions(font_id, text)

        xpos = self.start[0] - self.offset[0] - 150
        ypos = self.start[1] #+ self.offset[1]
        blf.position(font_id, xpos, ypos, 0)

        # rectangle behind text
        starti = len(vertices)
        # rectpoints: (0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)
        for x, y in rectpoints:
            vertices.append((int(textsize[0] * x) - xpos, int(textsize[1] * y) + ypos))
            colors.append((self.backcolor.r, self.backcolor.g, self.backcolor.b, 0))  #0.5 to 0
        indices.extend((
            (starti, starti+1, starti+2), (starti+2, starti, starti+3)
        ))

        do_textSmooth = True

    # SMOOTH
    if self.slider != 'NONE' and self.doingsmooth:
        xpos = self.start[0] + self.offset[0] - self.sliderwidth + (44 if self.textSmooth == 'MEDIUM' else 64 if self.textSmooth == 'LARGE' else 24)
        #ypos = self.start[1] + self.offset[1] - self.sliderheight # + (1 if self.slider != 'SMALL' else 0)
        ypos = self.start[1] - self.sliderheight

        sliderscale = smooth

        # slider back rect
        starti = len(vertices)
        # rectpoints: (0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)
        for x, y in rectpoints:
            vertices.append((int(self.sliderwidth * x) + xpos, int(self.sliderheight * y) + ypos - 1))
            colors.append((self.backcolor.r, self.backcolor.g, self.backcolor.b, 0)) #0.5 to 0
        indices.extend((
            (starti, starti+1, starti+2), (starti+2, starti, starti+3)
        ))

        # slider front rect
        starti = len(vertices)
        # rectpoints: (0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)
        for x, y in rectpoints:
            vertices.append((int(self.sliderwidth * x * sliderscale) + xpos - 100, int(self.sliderheight * y * 0.75) + ypos))
            colors.append((self.frontcolor.r, self.frontcolor.g, self.frontcolor.b, 0.8))
        indices.extend((
            (starti, starti+1, starti+2), (starti+2, starti, starti+3)
        ))

    shader = gpu.types.GPUShader(vertex_shader, fragment_shader)
    batch = batch_for_shader(shader, 'TRIS', {"pos":vertices, "color":colors}, indices=indices)

    bgl.glEnable(bgl.GL_BLEND)
    shader.bind()
    batch.draw(shader)
    bgl.glDisable(bgl.GL_BLEND)

    if do_textSmooth:
        #blf.draw(font_id, smoothText)
        blf.draw(font_id, smoothText + text)
        #blf.disable(font_id, blf.SHADOW)
