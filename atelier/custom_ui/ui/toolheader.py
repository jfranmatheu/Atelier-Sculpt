from bl_ui.properties_paint_common import UnifiedPaintPanel
#from .icons import preview_collections
from bl_ui.space_view3d import VIEW3D_HT_tool_header as ToolHeader
from ..blocks.block_data import blocks
from ... import __package__ as main_package

widths = []


class BAS_HT_toolHeader(ToolHeader):  # , UnifiedPaintPanel):
    bl_idname = "BAS_HT_ToolHeader"
    bl_label = "Toolheader"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOL_HEADER"
    #bl_context = ".paint_common"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        if (context.mode != "SCULPT"):
            super().draw(context)
            return
        # Not a brush but a tool.
        elif not UnifiedPaintPanel.paint_settings(context):
            super().draw(context)
            return

        # self.layout.template_header() # to change region

        # VARIABLES
        toolsettings = context.tool_settings
        self.sculpt = toolsettings.sculpt
        self.brush = brush = self.sculpt.brush

        wm = context.window_manager
        scn = context.scene

        # Not a brush but a tool.
        if brush is None:
            return

        self.capabilities = self.brush.sculpt_capabilities
        self.ups = toolsettings.unified_paint_settings
        self.context = context

        self.prefs = context.preferences.addons[main_package].preferences
        self.sep = 5 * context.preferences.view.ui_scale

        self.props = scn.bas_custom_ui
        #blocks = self.props.blocks
        #width = self.props.width
        #pos_x = self.props.pos_x
        #slots = self.props.ui_blocks.block_slots

        layout = self.layout

        for block in blocks:
            block(self)

        '''
        scale = context.preferences.view.ui_scale
        bl_ui_unit = 20 * scale
        sep = 5 * scale
        x = 3 * scale
        w = 0
        x0 = x + sep

        num_seps = 0

        groups = []
        group = []
        group_width = 0
        total_width = 0

        index_that_are_separator_spacer = []

        for i, block in enumerate(blocks):
            w = block(self)
            if w == -1:
                block.width = w
            elif w == 0:
                #group_width -= sep
                #print(group_width)
                #print([item.id for item in group])
                groups.append([group, group_width])
                total_width += group_width
                num_seps += 1
                group.clear()
                group_width = 0
                index_that_are_separator_spacer.append(i)
                #group.append(block)
            else:
                w *= bl_ui_unit
                group.append(block)
                group_width += w + sep
                block.width = w

        groups.append([group, group_width])
        total_width += group_width
        group.clear()
        reg_width = context.region.width

        off_x = context.region.view2d.region_to_view(0, 0)[0]

        #print(reg_width - total_width)
        so_tiny = reg_width - (total_width + bl_ui_unit * 1.5) < sep + 1 # bef_width + bl_ui_unit + scale + sep >= aft_start_x:

        if off_x != 0:
            #print("SCROLLING!")
            # To optimize (not process all the thing) we know if scrolling is ON, this is gone...
            sep_ext = sep * 1.2
            for ss_index in index_that_are_separator_spacer:
                blocks[ss_index].width = sep_ext

            off_x *= 2
            view2d = context.region.view2d
            for i, block in enumerate(blocks):
                if block.width != -1:
                    x += sep
                    #block.width = w = block(self) * bl_ui_unit
                    block.abs_x = x
                    block.x = view2d.region_to_view(x, 0)[0] - off_x
                    #print("Item: %i - X: %i - Real X: %i" % (i, x, block.x))
                    x += block.width # w
        elif so_tiny:
            #print("SO TINY!")
            # THIS FIX SOME BUG(s) WHEN VALUES ARE TINY OR BECOME NEGATIVE
            sep_ext = sep * 1.2
            for ss_index in index_that_are_separator_spacer:
                blocks[ss_index].width = sep_ext
            for block in blocks:
                if block.width != -1:
                    x += sep
                    block.x = block.abs_x = x
                    x += block.width
        else:
            num_groups = len(groups) - 1 # -1 only for index separator way
            width_count = 0

            for g_index, ss_index in enumerate(index_that_are_separator_spacer):
                bef_width = groups[g_index][1]
                width_count += bef_width
                #print("GINDEX:", g_index, " SSINDEX:", ss_index, " NUM_GROUPS:", num_groups, " NUM_SEPS:", num_seps, " TOTAL_WIDTH:", total_width)
                # THERE'S NOT AFTER GROUP
                if g_index  > num_groups or num_seps == 1:
                    #print("NO AFTER GROUP!")
                    blocks[ss_index].width = reg_width - total_width - sep
                    break
                else:
                    if num_seps == 2:
                        aft_width = groups[g_index + 1][1]
                        #print("num seps == 2")
                        # GROUPS 1-2
                        if g_index == 0:
                            #print("== 0 Group Index")
                            aft_mid_x = reg_width / num_seps # Take mid #
                            aft_start_x = aft_mid_x - aft_width / 2 # Offset mid to get start point using width
                            blocks[ss_index].width = aft_start_x - bef_width - bl_ui_unit - scale # Diff start with prev group width and standard unit and scale
                        # GROUPS 2-3
                        elif g_index == 1:
                            #print("== 1 Group Index")
                            sep_start_x = width_count
                            sep_final_x = reg_width - aft_width
                            blocks[ss_index].width = sep_final_x - sep_start_x - bl_ui_unit * 1.5 + x0 * 1.1
                    else:
                        #print(g_index)
                        next_group_width = groups[g_index + 1][1]
                        if g_index == 0:
                            #print("FIRST ONE")
                            aft_mid_x = reg_width / num_seps # Take mid of next group
                            aft_start_x = aft_mid_x - next_group_width / 2 # Offset mid to get start point using width
                            sep_width = aft_start_x - bef_width - bl_ui_unit - sep * .33
                        elif (g_index + 1) == num_groups:
                            #print("LAST ONE")
                            sep_width = (reg_width - next_group_width) - width_count - bl_ui_unit - sep * 1.2 # END POINT - START POINT
                        else:
                            #print("IN THE MIDDLE")
                            aft_mid_x = (reg_width / num_seps) * (g_index + 1)  # Take mid #
                            aft_start_x = aft_mid_x - next_group_width / 2 # Offset mid to get start point using width
                            sep_width = aft_start_x - width_count - bl_ui_unit - sep * 1.4 # Diff start with prev group width and standard unit and scale

                        sep_width = sep if sep_width < sep + 1 else sep_width
                        blocks[ss_index].width = sep_width
                        #print(sep_width)

                    width_count += blocks[ss_index].width
                    total_width += blocks[ss_index].width

            for i, block in enumerate(blocks):
                if block.width != -1:
                    x += sep
                    block.abs_x = block.x = x
                    x += block.width # w
        '''

        # layout.separator_spacer()

        #layout.popover('BAS_PT_custom_ui_uilist', text="Slots")

        #layout.menu("BAS_MT_custom_ui_items", text="", icon='ADD')
        #layout.operator('bas.edit_custom_ui', text="", icon='GREASEPENCIL')
