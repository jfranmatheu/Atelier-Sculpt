import bpy
import gpu
from gpu.types import GPUShader
from gpu_extras.batch import batch_for_shader
from gpu.shader import from_builtin


vertex_shader_3d_dotted_line = '''
    uniform mat4 u_ViewProjectionMatrix;

    in vec3 position;

    void main()
    {
        gl_Position = u_ViewProjectionMatrix * vec4(position, 1.0f);
    }
'''

fragment_shader_3d_dotted_line = '''
    uniform float u_Scale;

    void main()
    {
        if (sin(u_Scale) > 0.5) discard;
        gl_FragColor = vec4(1.0);
    }
'''

shader_3d_dotted_line = GPUShader(vertex_shader_3d_dotted_line, fragment_shader_3d_dotted_line)
shader_3d_uniform_color = from_builtin('3D_UNIFORM_COLOR')


def Draw_3D_DottedLine(context, _shader = shader_3d_dotted_line):
    batch = batch_for_shader(
        _shader, 'LINE_STRIP',
        {"position": coords, "arcLength": arc_lengths},
    )
    _shader.bind()
    _shader.uniform_float("u_ViewProjectionMatrix", context.region_data.perspective_matrix)
    _shader.uniform_float("u_Scale", 10)
    batch.draw(_shader)


def Draw_3D_Lines(coords=[(0,0,0), (1, 1, 1)], _shader = shader_3d_uniform_color):
    batch = batch_for_shader(_shader, 'LINES', {"pos": coords})
    _shader.bind()
    _shader.uniform_float("color", (1, 1, 0, 1))
    batch.draw(_shader)

def Draw_3D_Points(coords, color = (1, .55, .15, .85), _shader = shader_3d_uniform_color):
    batch = batch_for_shader(_shader, 'POINTS', {"pos": coords})
    _shader.bind()
    _shader.uniform_float("color", color)
    batch.draw(_shader)
