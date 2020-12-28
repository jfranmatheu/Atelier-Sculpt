import bpy
from . presets import *
from math import radians
from ...utils.easing import *
from ...utils.others import blender_version
from ...utils.space_conversion import convert_3d_spaceCoords_to_2d_screenCoords
extended = blender_version()[1] >= 2.90


class BAS_OT_brush_render_icon(bpy.types.Operator):
    bl_idname = "bas.brush_render_icon"
    bl_label = "Render Custom Brush Icon"
    bl_description = "Create a Custom Icon for the Actual Brush based on the Viewport"

    @classmethod
    def poll(cls, context):
        return context.sculpt_object

    def sculpt_base_mesh(self, context, props):
        lista = []
        n = len(sphere_standard_05)
        size = props.brush_size
        start = True
        for i, p in enumerate(sphere_standard_05):
            m = convert_3d_spaceCoords_to_2d_screenCoords(context, p)
            d = {
                'name' : str(i),
                'is_start' : start,
                'location' : p,
                'mouse' : m,
                'mouse_event' : m,
                'pen_flip' : False,
                'pressure' : max(0.08, min(QuadEaseInOut().ease(i/n), 1)),
                'size' : size,
                'time' : 0.1 * i,
                'x_tilt' : 0.0,
                'y_tilt' : 0.0
            }
            if extended:
                d2 = {
                    'mouse_event' : m,
                    'x_tilt' : 0.0,
                    'y_tilt' : 0.0
                }
                d.update(d2)
            start = False
            lista.append(d)
        bpy.ops.sculpt.brush_stroke(stroke=lista, mode='NORMAL' if not props.inverted else 'INVERT', ignore_background_click=False)

    def execute(self, context):
        scene = context.scene
        props = context.window_manager.bas_brush_thumbnailer
        original_obj = target_obj = context.active_object
        #scene.cursor.location = (0, 0, 0)
        #scene.cursor.rotation_euler = (0, 0, 0)

        if props.mode == 'AUTO':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.view3d.snap_cursor_to_center()

            if props.use_text and props.text != '':
                text_obj = bpy.ops.object.text_add()
                text_obj = context.active_object
                # text_obj.location = [0, -2, 0]
                text_obj.data.body = ''
            else:
                text_obj = None

            base_mesh = bpy.ops.mesh.primitive_ico_sphere_add (
                subdivisions=7, radius=1.0, calc_uvs=False, enter_editmode=False,
                align='WORLD', location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0)
            )
            target_obj = context.active_object
            bpy.ops.object.shade_smooth()
            if text_obj:
                text_obj.select_set(True)
            bpy.ops.view3d.localview()
            bpy.ops.view3d.view_axis(type='FRONT', align_active=True)
            bpy.ops.object.mode_set(mode='SCULPT')
            tool_settings = context.tool_settings
            sculpt = tool_settings.sculpt
            ups = tool_settings.unified_paint_settings
            if props.override_size:
                if ups.use_unified_size:
                    size = ups.size
                    ups.size = props.brush_size
                else:
                    size = sculpt.brush.size
                    sculpt.brush.size = props.brush_size
            if props.override_strength:
                if ups.use_unified_strength:
                    strength = ups.strength
                    ups.strength = props.brush_strength
                else:
                    strength = sculpt.brush.strength
                    sculpt.brush.strength = props.brush_strength
            x = sculpt.use_symmetry_x
            y = sculpt.use_symmetry_y
            z = sculpt.use_symmetry_z
            sculpt.use_symmetry_x = False
            sculpt.use_symmetry_y = False
            sculpt.use_symmetry_z = False
            self.sculpt_base_mesh(context, props)
            if props.override_size:
                if ups.use_unified_size:
                    ups.size = size
                else:
                    sculpt.brush.size = size
            if props.override_strength:
                if ups.use_unified_strength:
                    ups.strength = strength
                else:
                    sculpt.brush.strength = strength
            sculpt.use_symmetry_x = x
            sculpt.use_symmetry_y = y
            sculpt.use_symmetry_z = z
            context.active_object.data.use_auto_smooth = True
            if text_obj:
                text_obj.show_in_front = True
                text_obj.color = props.text_color
                text_obj.data.size = props.text_size
                text_obj.data.body = props.text
                text_obj.data.offset_x = -1
                text_obj.data.offset_y = -1
                text_obj.rotation_euler[0] = radians(90)
                text_obj.data.space_character = 1.1
                # 0.5  -> 0.01
                # 0.2  -> x
                text_obj.data.offset = 0.01 * props.text_size / 0.5
                text_obj.data.fill_mode = 'FRONT'
                # text_obj.data.bevel_depth = 0.02
                # text_obj.data.render_resolution_u = 12

                #bpy.ops.view3d.zoom(delta=2)
                #bpy.ops.view3d.zoom(delta=2)
                #bpy.ops.view3d.zoom(delta=2)
                #bpy.ops.view3d.zoom(delta=1)

            # Link active object to the new collection
            # C.scene.collection.objects.link(base_mesh)

            # And finally select it and make it active.
            # base_mesh.select_set(True)
            # view_layer.objects.active = base_mesh
            target_obj.data.remesh_voxel_size *= 1
        else:
            original_obj.data.remesh_voxel_size *= 1
            text_obj = None

        space = context.space_data
        brush = context.tool_settings.sculpt.brush # Get active brush
        brush.use_custom_icon = True # Mark to use custom icon

        # BACKUP DATA
        overlays_state = context.space_data.overlay.show_overlays
        gizmo_state = context.space_data.show_gizmo
        resX = scene.render.resolution_x
        resY = scene.render.resolution_y
        displayMode = context.preferences.view.render_display_type
        oldpath = scene.render.filepath
        lens = context.space_data.lens

        withAlpha = props.use_alpha
        withTint = props.use_tint
        light = space.shading.light
        bgColor = space.shading.background_color
        shadingBgType = space.shading.background_type
        film = scene.render.film_transparent
        color_type = space.shading.color_type
        obj_color = target_obj.color
        show_cavity = space.shading.show_cavity

        # PRIMEROS PREPARATIVOS :)
        context.preferences.view.render_display_type = 'NONE'
        context.space_data.overlay.show_overlays = False
        context.space_data.show_gizmo = False
        scene.render.resolution_x = 128
        scene.render.resolution_y = 128
        context.space_data.lens = 100 # props.focal_length
        space.shading.light = 'MATCAP'
        space.shading.show_cavity = True
        if withAlpha:
            scene.render.film_transparent = True
        else:
            scene.render.film_transparent = False
            space.shading.background_type = 'VIEWPORT'
            space.shading.background_color = props.bg_color
        if withTint or text_obj:
            space.shading.color_type = 'VERTEX'  # 'SINGLE'
            # space.shading.single_color = props.tint
            target_obj.color = props.tint

        from os.path import join
        # temp_dir = bpy.app.tempdir # TEMPORAL FOLDER OF THE ACTUAL BLENDER PROJECT
        from ... import root
        icons_dir = join(root, "user_data", 'sculpt_brush_icons')
        filename = brush.name + "_icon.png"
        filepath = join(icons_dir, filename)

        # RENDER SETTINGS
        scene.render.image_settings.file_format = 'PNG'
        scene.render.filepath = filepath
        bpy.ops.render.opengl(write_still=True) # RENDER + SAVE (In filepath as PNG)

        render_image = bpy.data.images["Render Result"] # GET RENDERED IMAGE
        render_image.name = '.' + filename # CHANGE RENDERED IMAGE' NAME TO GENERATE FILENAME
        bpy.ops.image.pack() # PACK IMAGE TO .BLEND FILE

        # ASIGN ICON (RENDER) TO BRUSH
        bpy.data.brushes[brush.name].icon_filepath = filepath

        # RESTORE DATA
        scene.render.resolution_x = resX
        scene.render.resolution_y = resY
        context.space_data.overlay.show_overlays = overlays_state
        context.space_data.show_gizmo = gizmo_state
        context.preferences.view.render_display_type = displayMode
        scene.render.filepath = oldpath
        context.space_data.lens = lens
        scene.render.film_transparent = film
        space.shading.show_cavity = show_cavity
        space.shading.light = light

        if withAlpha == False:
            space.shading.background_color = bgColor
            space.shading.background_type = shadingBgType
        if withTint or text_obj:
            space.shading.color_type = color_type
            # space.shading.single_color = (1, 1, 1)
            target_obj.color = obj_color
        try:
            bpy.data.images.remove(bpy.data.images[filename + ".001"])
        except:
            pass

        # PREPARE NEW RENDER IMAGE SLOT FOR ANOTHER ICON
        bpy.ops.image.new(name="Render Result")

        if props.mode == 'AUTO':
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.view3d.localview()
            bpy.data.objects.remove(context.active_object)

            if props.use_text and props.text != '' and text_obj:
                bpy.data.objects.remove(text_obj)

            original_obj.select_set(True)
            context.view_layer.objects.active = original_obj
            bpy.ops.object.mode_set(mode='SCULPT')

        context.area.tag_redraw()
        return {'FINISHED'}
    

classes = (
    BAS_OT_brush_render_icon,
)
