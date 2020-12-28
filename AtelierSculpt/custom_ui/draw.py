from ..utils.draw2d import Draw_2D_Rectangle
from .blocks.block_data import blocks


def edit_custom_ui_callback_px(self, context):
    if self.area != context.area:
        return

    update_interface(context)

    active_index = self.active_slot_index
    y = 2
    height = self.toolheader.height - 6

    if self.moving:
        co = self.new_color
        Draw_2D_Rectangle(
            blocks[active_index].x, y, blocks[active_index].width, height, (co[0], co[1], co[2], 1))

    #Draw_2D_Rectangle(0, 0, self.toolheader.width, self.toolheader.height, (.4, .9, .4, .15))

    if self.active_item:
        self.moving_x = int(
            self.mouse_pos[0] - blocks[self.active_slot_index].width / 2)
        x = self.moving_x if self.moving else blocks[active_index].x
        a = .75 if self.moving else .6
        Draw_2D_Rectangle(
            x, y, blocks[active_index].width, height, (1, 1, 1, a))


def update_interface(context):
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
    invalid_group_indices = invalid_group_block_min_max = invalid_block_indices = []
    #prev_sep_idx = -1
    prev_gr_index = 0
    previous_was_spacer = False

    index_that_are_separator_spacer = []

    for i, block in enumerate(blocks):
        w = block.ui_units_x
        if w == -1:
            print("INVALID BLOCK:", block.id)
            block.width = -1
            invalid_block_indices.append(block)
            #if group_width == 0:
            #group_width -= sep
            previous_was_spacer = False
            pass
        elif w == 0:
            invalid_group_block_min_max.append([prev_gr_index, i])
            if group_width == 0:
                invalid_group_indices.append(len(groups))
                # invalid_group_block_max.append(i)
            #prev_sep_idx = i
            prev_gr_index = i
            #group_width -= sep
            # print(group_width)
            #print([item.id for item in group])
            groups.append([group, group_width])
            total_width += group_width
            num_seps += 1
            group = group.copy()
            group.clear()
            group_width = 0
            index_that_are_separator_spacer.append(i)
            previous_was_spacer = True
            # group.append(block)
        else:
            w *= bl_ui_unit
            group_width += w + sep
            block.width = w
            group.append(block)
            previous_was_spacer = False

    groups.append([group, group_width])
    total_width += group_width
    # group.clear()
    reg_width = context.region.width

    off_x = context.region.view2d.region_to_view(0, 0)[0]

    #print(reg_width - total_width)
    # bef_width + bl_ui_unit + scale + sep >= aft_start_x:
    so_tiny = reg_width - (total_width + bl_ui_unit * 1.5) < sep + 1

    if off_x != 0:
        print("SCROLLING!")
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
                x += block.width  # w
    elif so_tiny:
        print("SO TINY!")
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
        num_groups = len(groups) - 1  # -1 only for index separator way
        width_count = 0

        # reversed(list(enumerate()))
        for g_index, ss_index in enumerate(index_that_are_separator_spacer):
            bef_width = groups[g_index][1]
            width_count += bef_width
            print("GINDEX:", g_index, " SSINDEX:", ss_index, " NUM_GROUPS:",
                  num_groups, " NUM_SEPS:", num_seps, " TOTAL_WIDTH:", total_width)
            #print("Group Width:", groups[g_index][1])
            # THERE'S NOT AFTER GROUP
            if g_index > num_groups or num_seps == 1:
                print("NO AFTER GROUP! or num seps == 1")
                blocks[ss_index].width = reg_width - total_width - sep * 3.25
                break
            else:
                if num_seps == 2:
                    aft_width = groups[g_index + 1][1]
                    print("num seps == 2")
                    # GROUPS 1-2
                    if g_index == 0:
                        print("== 0 Group Index")
                        # Group too close to previous one
                        # NOTE: have to add aft_mid_width of the group as it's in the middle
                        #       also one sep just to take into account the separation between groups.
                        if bef_width + aft_width / 2.0 + sep > reg_width / 2.0:
                            print("No before's spacing")
                            blocks[ss_index].width = sep * 1.2
                        else:
                            aft_mid_x = reg_width / num_seps  # Take mid #
                            # Offset mid to get start point using width
                            aft_start_x = aft_mid_x - aft_width / 2.0
                            # Diff start with prev group width and standard unit and scale
                            blocks[ss_index].width = aft_start_x - \
                                bef_width - bl_ui_unit - scale
                    # GROUPS 2-3
                    elif g_index == 1:
                        print("== 1 Group Index")
                        sep_start_x = width_count
                        sep_final_x = reg_width - aft_width
                        blocks[ss_index].width = sep_final_x - \
                            sep_start_x - bl_ui_unit * 1.5 + x0 * 1.1  # 1.1
                else:
                    # print(g_index)
                    print("num seps > 2")
                    next_group_width = groups[g_index + 1][1]
                    if g_index == 0:
                        print("FIRST ONE")
                        aft_mid_x = reg_width / num_seps  # Take mid of next group
                        # Offset mid to get start point using width
                        aft_start_x = aft_mid_x - next_group_width / 2.0
                        sep_width = aft_start_x - bef_width - bl_ui_unit - sep * .33
                    elif (g_index + 1) == num_groups:
                        print("LAST ONE")
                        # END POINT - START POINT
                        sep_width = (reg_width - next_group_width) - \
                            width_count - bl_ui_unit - sep * 1.2
                    else:
                        print("IN THE MIDDLE")
                        aft_mid_x = (reg_width / num_seps) * \
                            (g_index + 1)  # Take mid #
                        # Offset mid to get start point using width
                        aft_start_x = aft_mid_x - next_group_width / 2.0
                        # Diff start with prev group width and standard unit and scale
                        sep_width = aft_start_x - width_count - bl_ui_unit - sep * 1.4

                    sep_width = sep if sep_width < sep + 1 else sep_width
                    blocks[ss_index].width = sep_width
                    # print(sep_width)

                width_count += blocks[ss_index].width
                total_width += blocks[ss_index].width

        # OLD METHOD. But...
        '''
        for gindex in range(0, len(groups)):
            if groups[gindex][1] != 0:
                for i in range(invalid_group_block_min_max[gindex][0], invalid_group_block_min_max[gindex][1]):
                    if blocks[i].width != -1:
                        x += sep
                        blocks[i].abs_x = blocks[i].x = x
                        x += blocks[i].width # w
        '''

        for i, block in enumerate(blocks):
            #if num_seps != 0 and block in invalid_block_indices:  # verify if it has separator and group is 0...
            #    x -= sep + 1
            if block.width == -1:
                pass # x -= 1
            #elif block.ui_units_x == -1:
            #    if num_seps != 0:
            #        x -= sep + 1
            else:
                x += sep
                block.abs_x = block.x = x
                x += block.width  # w

        # When having 2 separators together and in the block between them
        # is -1 in width (not been drawn), there was a separator counting up,
        # and that was causing issues in edit mode.
        # INSTEAD. We need to iter the groups and each group block.
        #          then, asign abs_x, x to blocks[idx], avoid groups with 0 width.
        '''
        block_idx = 0
        for gr_index, gr in enumerate(groups):
            if (gr_index + 1) <= num_seps:
                #gr[0].append(blocks[len(gr[0]) + 1])
                max_index = len(gr[0]) + 1
            else:
                max_index = len(gr[0])
            if gr_index in invalid_group_indices:
                #max_index = invalid_group_block_max[gr_index]
                x += blocks[invalid_group_block_max[gr_index]].width
            else:
                if gr[1] != 0:
                    print(max_index)
                    for idx in range(block_idx, block_idx + max_index):
                        if blocks[idx].width != -1:
                            x += sep
                            blocks[idx].abs_x = blocks[idx].x = x
                            x += blocks[idx].width
                        print(x, blocks[idx].width)
                else:
                    print("Group with width", gr[1], gr[0])
            block_idx += max_index
        '''
