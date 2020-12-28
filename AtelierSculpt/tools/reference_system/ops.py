# Copyright (C) 2019 Juan Fran Matheu G.
# Contact: jfmatheug@gmail.com 
import bpy
from bpy.types import Operator
from .io import Create_Ref_Data
from ...utils.others import ShowMessageBox, Generate_UUID
from .draw import Reference_Events, draw_reference_callback_px, interactive_draw_reference_callback_px, Create_Reference
from .ui import references
import blf
from bpy.props import FloatVectorProperty, BoolProperty, IntProperty, StringProperty
from mathutils import Vector

# OVERLAP N REFERENCE
class BAS_OT_Flip_Reference(Operator):
    bl_idname = "bas.flip_reference"
    bl_label = ""
    bl_description = "Flip Reference"
    index : IntProperty()
    axis : StringProperty()
    def execute(self, context):
        references[self.index].signal = self.axis
        return {'FINISHED'}

# OVERLAP N REFERENCE
class BAS_OT_Overlap_Reference(Operator):
    bl_idname = "bas.overlap_reference"
    bl_label = ""
    bl_description = "Overlap Reference"
    index : IntProperty()
    def execute(self, context):
        r = references[self.index]
        r.in_front = False if r.in_front else True
        return {'FINISHED'}

# OVERLAP N REFERENCE
class BAS_OT_Transparent_Reference(Operator):
    bl_idname = "bas.transparent_reference"
    bl_label = ""
    bl_description = "Overlap Reference"
    index : IntProperty()
    def execute(self, context):
        r = references[self.index]
        r.use_transparency = False if r.use_transparency else True
        return {'FINISHED'}

# HIDE ALL REFERENCES
class BAS_OT_Hide_References(Operator):
    bl_idname = "bas.hide_all_references"
    bl_label = ""
    bl_description = "Hide All References"
    hide : BoolProperty()
    def execute(self, context):
        signal = 'H' if self.hide else ''
        for r in references:
            r.signal = signal
        #bpy.context.window_manager.references_hide_all = self.hide
        return {'FINISHED'}

# HIDE N REFERENCE
class BAS_OT_Hide_Reference(Operator):
    bl_idname = "bas.hide_reference"
    bl_label = ""
    bl_description = "Hide Reference"
    index : IntProperty()
    def execute(self, context):
        r = references[self.index]
        r.signal = 'H' if r.signal == '' else ''
        return {'FINISHED'}

# LOCK ALL REFERENCES
class BAS_OT_Lock_References(Operator):
    bl_idname = "bas.lock_all_references"
    bl_label = ""
    bl_description = "Lock All References"
    state : BoolProperty()
    def execute(self, context):
        for r in references:
            r.is_locked = self.state
        #bpy.context.window_manager.references_lock_all = self.state
        return {'FINISHED'}

# Lock n REFERENCES
class BAS_OT_Lock_Reference(Operator):
    bl_idname = "bas.lock_reference"
    bl_label = ""
    bl_description = "Lock Reference"
    index : IntProperty()
    def execute(self, context):
        r = references[self.index]
        r.is_locked = False if r.is_locked else True
        return {'FINISHED'}


# Remove n REFERENCES
class BAS_OT_Remove_Reference(Operator):
    bl_idname = "bas.remove_reference"
    bl_label = ""
    bl_description = "Remove Reference"
    index : IntProperty()
    permanent : BoolProperty(default=False)

    @classmethod
    def description(cls, context, properties):
        if properties.permanent:
            return "Remove Completelly that image from the project"
        else:
            return "Remove this image from the references but keep it in the project"

    def execute(self, context):
        r = references.pop(self.index)
        #r = references[self.index]
        r.signal = 'R' # remove signal
        r.is_reference = False
        # QUITAR SI CRASHEA
        '''
        if self.permanent:
            for img in bpy.data.images:
                if img.ref.uuid == r.uuid:
                    bpy.data.images.remove(img)
                    break
        '''
        return {'FINISHED'}

# INTERACTIVE DRAWING IMAGE REFERENCE MAKER
# FLOATING IMAGE REFERENCE SYSTEM
class BAS_OT_Reference_Maker(Operator):
    bl_idname = "bas.reference_maker"
    bl_label = ""
    bl_description = "Reference Maker"

    @classmethod
    def description(cls, context, properties):
        return "Drag over the viewport to draw your reference"

    def modal(self, context, event):
        self.mousePos = Vector((event.mouse_region_x, event.mouse_region_y))
        if event.type in {'ESC'} or self.finished:
            self.finish(context)
            return {'FINISHED'}
        elif self.dragging:
            if event.type in {'LEFTMOUSE'} and event.value in {'RELEASE', 'CLICK'}:
                self.lastPos = self.mousePos
                self.create_button(context)
                return {'FINISHED'}
            if event.shift:
                self.using_shift = True
                self.using_ctrl = False
            elif event.ctrl:
                if not self.using_ctrl:
                    self.midPoint = (self.mousePos + self.firstPos) / 2
                self.using_ctrl = True
                self.using_shift = False
            else:
                self.midPoint = Vector((0, 0))
                self.using_shift = False
                self.using_ctrl = False
        else:
            if event.type in {'LEFTMOUSE'} and event.value in {'PRESS'}:
                self.firstPos = self.mousePos
                self.dragging = True
                return {'RUNNING_MODAL'}
        context.area.tag_redraw()
        return {'RUNNING_MODAL'}

    def execute(self, context):
        scn = context.scene.bas_references
        wm = context.window_manager.bas_references
        # LOAD IMAGE
        if wm.get_references_from == 'SINGLE':
            if wm.image_path == None or wm.image_path == "":
                ShowMessageBox("Image path is empty", "Can't load any image", 'ERROR')
                return {'FINISHED'}
        else:
            if wm.previews_dir == "" or wm.previews == None:
                ShowMessageBox("Directory is empty or image in null", "Can't load any image", 'ERROR')
                return {'FINISHED'}
        try:
            # TODO check existing to true and make a previous pass to determine if image can be imported, return error msg if not
            if wm.get_references_from == 'SINGLE':
                self.image = bpy.data.images.load(wm.image_path, check_existing=False)
            else:
                self.image = bpy.data.images.load(wm.previews_dir + wm.previews, check_existing=False)
        except:
            ShowMessageBox("Image path or image is not valid", "Can't load any image", 'ERROR')
            return {'FINISHED'}
        wm.image = self.image # this is for passing image data to real draw method
        size = self.image.size
        self.proportion = size[0] / size[1]
        self.wider = False if self.proportion > 1 else True
        
        # TEMP TOOL
        self.mode = context.mode
        self.oldTool = context.workspace.tools.from_space_view3d_mode(self.mode, create=False).idname
        bpy.ops.wm.tool_set_by_id(name="builtin.annotate")

        # VARS
        self.mousePos = Vector((0, 0))
        self.firstPos = Vector((0, 0))
        self.lastPos = Vector((0, 0))
        self.midPoint = Vector((0, 0))
        self.finished = False
        self.dragging = False
        self.width = 0
        self.height = 0
        self.using_shift = False
        self.using_ctrl = False

        # SAFE TEXT
        if wm.label_text_size > wm.label_thickness:
            wm.label_text_size = wm.label_thickness - 2

        # HANDLERS
        context.window_manager.modal_handler_add(self)
        if not hasattr(self, '_handle'):
            args = (self, context)
            self._handle = bpy.types.SpaceView3D.draw_handler_add(interactive_draw_reference_callback_px, args, 'WINDOW', 'POST_PIXEL')
        return {'RUNNING_MODAL'}

    def create_button(self, context):
        #wm = context.window_manager
        if self.using_ctrl:
            coords = self.center
        elif self.lastPos[1] < self.firstPos[1] and self.lastPos[0] < self.firstPos[0]:
            coords = Vector((self.firstPos[0] - abs(self.width), self.firstPos[1] - abs(self.height)))
        elif self.lastPos[1] < self.firstPos[1]:
            coords = Vector((self.firstPos[0], self.firstPos[1] - abs(self.height)))
        elif self.lastPos[0] < self.firstPos[0]:
            coords = Vector((self.firstPos[0] - abs(self.width), self.firstPos[1]))
        else:
            coords = Vector((self.firstPos[0], self.firstPos[1]))
        bpy.ops.bas.create_reference(size=(self.width, self.height), position=coords)
        self.finish(context)

    def finish(self, context):
        if self.finished == False:
            bpy.ops.wm.tool_set_by_id(name=self.oldTool)
            try:
                self.finished = True
                if self._handle:
                    bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
                    del self._handle
            except:
                pass
        return {'FINISHED'}

# FLOATING IMAGE REFERENCE SYSTEM
class BAS_OT_Create_Reference(Operator):
    bl_idname = "bas.create_reference"
    bl_label = ""
    bl_description = "Create Reference"

    size : FloatVectorProperty(default=(0,0), size=2, min=64, max=2048)
    position : FloatVectorProperty(default=(0,0), size=2, min=0)

    def modal(self, context, event):
        if self.area != context.area: # just for safe
            print("hey")
            print(self.area)
            print(context.area)
            print("ERROR: Reference will be removed...")
            self.remove()
            return {'FINISHED'}
        self.refresh(context) # refresh

        # SIGNAL CHANGE !
        if self.prev_signal != self.ref.signal:
            # REMOVING SIGNAL
            if self.ref.signal == 'R':
                self.remove() # force remove ref
                return {'FINISHED'}
            elif self.ref.signal == 'X':
                self.flipX = False if self.flipX else True # invert flip x state
                self.flipY = False if self.flipX else self.flipY # deactivate flip in other axist to not interf
                self.ref.signal = self.prev_signal # Reset Signal to prev state
            elif self.ref.signal == 'Y':
                self.flipY = False if self.flipY else True
                self.flipX = False if self.flipY else self.flipX
                self.ref.signal = self.prev_signal # Reset Signal to prev state
            else:
                self.prev_signal = self.ref.signal # update prev Signal
        # HIDDING SIGNAL?
        elif self.ref.signal != 'H':
            # Image is locked or global lock state is active ?
            # Some image is being moved but is not this one  ?
            if (self.ref.is_locked or context.window_manager.bas_references.lock_all) or (context.window_manager.bas_references.moving_reference and not self.moving):
                pass
            # IS THE RIGHT MODE ?
            elif self.ref.mode == 'ALL' or context.mode == self.ref.mode:
                self.mousePos = Vector((event.mouse_region_x, event.mouse_region_y))
                if Reference_Events(self, context, event):
                    return {'RUNNING_MODAL'}
                #print("EXCEPTION: Reference will be removed...")
                #self.remove()
                #return {'FINISHED'}
        return {'PASS_THROUGH'}

    def refresh(self, context):
        if context.area:
            context.area.tag_redraw()

    def remove(self):
        if self.cancelled == False:
            self.cancelled = True
            try:
                if hasattr(self, '_handle'):
                    bpy.types.SpaceView3D.draw_handler_remove(self._handle, "WINDOW")
                    del self._handle
            except:
                pass
            scn = bpy.context.scene.bas_references
            scn.num_of_references -= 1
            if scn.num_of_references < 1:
                scn.is_using_references = False
                scn.num_of_references = 0

    def execute(self, context):
        wm = context.window_manager.bas_references
        if not wm.image:
            print("WARN: No reference image data was found!")
            return {'FINISHED'}
        scn = context.scene.bas_references
        self.cancelled = False # cancelled condition to block over-iter
        self.moving = False
        self.flipX = False
        self.flipY = False
        self.image = bpy.data.images[wm.image.name] # load image data
        wm.image = None # free" pointer
        # This way we can know if this project has references to load
        if not scn.is_using_references:
            scn.is_using_references = True
        scn.num_of_references += 1
        self.image.use_fake_user = True # We ensure to keep image in project
        ref = self.image.ref # Access to custom reference data in our image
        ref.is_reference = True # Now this image is set as a reference
        ref.uuid = Generate_UUID() # Generate a unic ID for this image reference
        # If this is true, we are going to block this reference to be drawing only in the actual mode
        if wm.keep_in_actual_mode:
            ref.mode = context.mode
        else:
            ref.mode = 'ALL'
        ref.size = self.size # this is passed by the interactive drawing method
        ref.position = self.position # this is passed by the interactive drawing method
        ref.name = wm.name
        ref.use_label = wm.use_label
        ref.label_text = wm.label_text
        ref.label_text_size = wm.label_text_size
        ref.label_text_align = wm.label_text_align
        ref.label_text_color = wm.label_text_color
        ref.label_color = wm.label_color
        ref.label_thickness = wm.label_thickness
        ref.label_align_to = wm.label_align
        #ref.opacity = wm.reference_image_opacity
        ref.use_outline = wm.use_outline
        ref.outline_color = wm.outline_color
        ref.is_locked = False # By default is always false
        ref.signal = '' # by default is always '' empty == visible
        ref.in_front = True
        ref.use_transparency = False #wm.reference_use_transparency

        self.prev_signal = ''
        self.ref = ref # we'll use self.image for image and bindcode atributes, self.ref for reference properties
        # Add it to our list of references
        references.append(self.ref)

        # ADD A MODAL HANDLER
        context.window_manager.modal_handler_add(self)
        # ADD A DRAWING HANDLER
        if not hasattr(self, '_handle'):
            args = (self, context)
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_reference_callback_px, args, 'WINDOW', 'POST_PIXEL')
        self.area = context.area
        return {'RUNNING_MODAL'}

# OPTIMAL FLOATING IMAGE REFERENCE SYSTEM
class BAS_OT_Create_Opti_Reference(Operator):
    bl_idname = "bas.create_opti_reference"
    bl_label = ""
    bl_description = "Create Reference"

    def execute(self, context):
        scn = context.scene.bas_references
        wm = context.window_manager.bas_references
        # CHECK IF IT'S FIRST REFERENCE
        if not scn.is_using_references:
            # CREATE REFERENCE DATABASE FOR THIS PROJECT
            if Create_Ref_Data(): # If succeed, continue
                scn.is_using_references = True # Save into project file so next time you start ur project it will notice it
                scn.num_of_references += 1 # Increment in 1 the number of references created
            else:
                ShowMessageBox("A database problem has ocurred! Please report it!", "Ops! There is a problem!", 'ERROR')
                return {'FINISHED'}
        # Get Image path and import image
        self.image = bpy.data.images.load(wm.image_path, check_existing=True)
        # Save Internally?
        if scn.save_references_mode == 'INTERNAL':
            self.image.use_fake_user = True # Force to keep in project so it's not deleted when closing
        else: # EXTERNAL SAVE
            self.image.use_fake_user = False # No need to save in project
            # Save it in reference folder
        # Fills reference object data and save 'reference' to that inst    
        self.reference = Create_Reference()
        
        # TODO


classes = (
    BAS_OT_Create_Opti_Reference,
    BAS_OT_Create_Reference,
    BAS_OT_Flip_Reference,
    BAS_OT_Hide_Reference,
    BAS_OT_Hide_References,
    BAS_OT_Lock_Reference,
    BAS_OT_Lock_References,
    BAS_OT_Overlap_Reference,
    BAS_OT_Reference_Maker,
    BAS_OT_Remove_Reference,
    BAS_OT_Transparent_Reference
)
