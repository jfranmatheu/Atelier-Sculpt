from ...utils.draw2d import (
    Draw_2D_Lines, Draw_2D_Points, Draw_2D_Line,
    Draw_Text, Draw_2D_Circle, Draw_2D_Rectangle, Color
)
from ...utils.draw3d import Draw_3D_Lines, Draw_3D_Points
from ...utils.space_conversion import convert_3d_spaceCoords_to_2d_screenCoords
from ...utils.geo2dutils import distance_between, is_inside_2d_rect

orange = list(Color.Orange.value)
white = list(Color.White.value)
blue = list(Color.Turquoise.value)


spacing = 10
tool_height = 25
height = 125
width = 160
header_height = 30


def draw_stroke_callback(self, context):
    if self.area != context.area:
        return

    can_draw = context.window_manager.bas_nondestructive.show_overlays
    from .ops import tool_text, StrokeTool as Tool

    if self.op_mode == 'BRISTLE':
        # Filter 1.
        if not self.cursor_origin:
            return

        # Origin Graphic.
        Draw_Text(self.cursor_origin[0]-6, self.cursor_origin[1]-14, "*", 28, 0, 1, .1, .1, 1)
        if self.cursor_active:
            Draw_2D_Circle(self.cursor_origin, 10, 16, (1, 1, 0, 1))

        # Filter 2.
        if not self.cursor_points:
            return

        # Draw cursor points.
        for i, point in enumerate(self.cursor_points):
            Draw_Text(point[0]-6, point[1]-8, "•", 24, 0, 1, .1, .1, .5)
            Draw_2D_Circle(point, self.cursor_points_size[i], 8, (1, 1, 0, 1))
        return

    if self.op_mode == 'CURVE':
        if self.bez_screen_point:
            if can_draw:
                Draw_2D_Lines(self.bez_screen_point, (.7, .1, .2, .4))
            for p in self.bez_screen_point:
                Draw_Text(p[0]-4, p[1]-4, "•", 14, 0, 1, .5, .2, 1)
        if self.bezier_points:  # self.bez_space_point:
            # SEARCH FOR ACTIVE POINT
            minDist = 2000
            idx = 0
            #prev = None
            # for p in self.bez_space_point:
            # OBTENEMOS LAS COORDENADAS EN PANTALLA
            #    v = convert_3d_spaceCoords_to_2d_screenCoords(context, p)
            #    if v:
            for p in self.bezier_points:
                #self.bez_screen_point[idx] = v
                dist = distance_between(p, self.mouse_pos)  # v
                if (dist < minDist):
                    minDist = dist
                    self.active_point = p
                    self.active_point_index = idx
                # DRAW POINT
                if idx == 1:
                    Draw_Text(p[0]-6, p[1]-8, "•", 24, 0, 1, .1, .1, 1)
                    Draw_Text(p[0]-6, p[1]-14, "*", 28, 0, 1, .1, .1, 1)
                    Draw_Text(p[0], p[1] + 10, str(int(self.bez_length)) + " / " + str(self.bez_point_count), 15, 0)
                else:
                    Draw_Text(p[0]-6, p[1]-8, "•", 24, 0, 0, .4, 1, 1)
                    Draw_Text(p[0]-6, p[1]-14, "*", 28, 0, .1, .4, 1, 1)  # .6, .8, 1, 1) # v
                # if can_draw:
                    # DIBUJAMOS CADA LINEA
                #    if prev:
                #        Draw_2D_Line(prev, p, (.7, .1, .2, .4))
                #    prev = p
                idx += 1
            if minDist > self.dist_threshold:
                self.active_point = None
            # DRAW ACTIVE POINT
            elif self.active_point:
                Draw_Text(self.active_point[0]-6, self.active_point[1]-14, "*", 28, 0, 1, .1, .1, 1)
                Draw_2D_Circle(self.active_point, 10, 16, (1, 1, 0, 1))
            if self.props.curve_mode_follow_cursor:
                if distance_between(self.curve_drag_point, self.mouse_pos) < minDist:
                    self.active_point = None
                    self.curve_drag_point_active = True
                else:
                    self.curve_drag_point_active = False
                Draw_Text(self.curve_drag_point[0]-6, self.curve_drag_point[1]-14, "♦", 28, 0, 1, .1, .1, 1)
        return

    n = 0
    minDist = 2000
    prev = [0, 0, 0]
    near_2d_point = [0, 0]
    if self.space_points:
        self.snapping = False
        for point in self.space_points:
            # OBTENEMOS LAS COORDENADAS EN PANTALLA
            v = convert_3d_spaceCoords_to_2d_screenCoords(context, point)
            if v != None:
                self.strokes[n].mouse = self.screen_points[n] = v
                dist = distance_between(v, self.mouse_pos)  # ya es abs !
                if (dist < minDist):
                    if self.active_point != point:  # Comprobar si no es el punto ya activo
                        if abs(dist) < self.dist_threshold:  # Si está dentro del rango
                            # self.near_point = point # guardar referencia coordenadas
                            near_2d_point = v
                            self.active_point = point
                            self.active_point_index = n
                    minDist = dist
                if can_draw:
                    # DIBUJAMOS CADA LINEA
                    # if n != 0:
                    #    Draw_2D_Line(prev, v, (.7, .1, .2, .5))

                    # DIBUJAMOS CADA PUNTO
                    Draw_Text(v[0]-6, v[1]-8, "•", 24, 0, .6, .8, 1, .8)
                prev = v
                n += 1

        if minDist > self.dist_threshold:
            self.active_point = None

        if can_draw:
            # Start / End.
            Draw_Text(self.screen_points[0][0]-6, self.screen_points[0][1]-14, "*", 28, 0, 1, .7, .2, 1)
            Draw_Text(self.screen_points[-1][0]-6, self.screen_points[-1][1]-14, "*", 28, 0, 1, .7, .2, 1)

            if self.active_point:
                # DIBUJAMOS PUNTO ACTIVO
                if self.using_tool:
                    Draw_Text(near_2d_point[0]-9, near_2d_point[1]-13, "•", 36, 0, 1, .6, .8, .8)
                    Draw_2D_Circle(near_2d_point, 10, 16, (1, 1, 0, .8))

                    # if self.active_tool == Tool.Rope:
                    #    p = self.screen_points[self.active_point_index]
                    #    Draw_2D_Circle(self.mouse_pos, 24, 16, (1, 1, 1, 1))
                    #    Draw_2D_Line(self.mouse_pos, p, (1, 0, 0, 1))
                    #    Draw_Text(p[0]-9, p[1]-13, "•", 36, 0, 1, .1, .1, 1)
                else:
                    active_point_2d = convert_3d_spaceCoords_to_2d_screenCoords(context, self.active_point)
                    Draw_Text(active_point_2d[0]-9, active_point_2d[1]-13, "•", 36, 0, 1, .6, .8, .8)
                    Draw_2D_Circle(active_point_2d, 10, 16, (1, 1, 0, .8))

                if self.active_tool == Tool.Rope:
                    p = self.screen_points[self.active_point_index]
                    Draw_Text(p[0]-9, p[1]-13, "•", 36, 0, 1, .1, .1, 1)
            if self.active_tool == Tool.Erase:
                self.update_points_in_area(context)
                for i in self.points_in_area:
                    p = self.screen_points[i]
                    Draw_Text(p[0]-9, p[1]-13, "•", 36, 0, 1, .1, .1, .9)
            elif self.active_tool in {Tool.Magnet, Tool.Liquify}:
                self.update_points_in_area(context)
                self.update_points_in_area_distances(context)
                rad2 = self.ups.size / 2 if self.ups.use_unified_size else self.brush.size / 2
                if self.active_tool == Tool.Magnet:
                    for idk, i in enumerate(self.points_in_area):
                        p = self.screen_points[i]
                        d = self.points_in_area_distances[idk]
                        co = (1 if d > rad2 else d / rad2, 1 if d < rad2 else 1 - abs((d - rad2) / rad2), 0, 1)
                        # print(co)
                        Draw_Text(p[0]-9, p[1]-13, "•", 36, 0, *co)
                else:
                    for idk, i in enumerate(self.points_in_area):
                        p = self.screen_points[i]
                        d = self.points_in_area_distances[idk]
                        co = (1 if d < rad2 else 1 - abs((d - rad2) / rad2), 1 if d > rad2 else d / rad2, 0, 1)
                        # print(co)
                        Draw_Text(p[0]-9, p[1]-13, "•", 36, 0, *co)

    # DRAW HELP TEXTS
    num_tools = Tool.ALL.value
    header_y = self.y + tool_height * num_tools
    half_spacing = spacing / 2
    height = tool_height * num_tools + spacing * 2 + header_height

    Draw_2D_Rectangle(self.x, self.y - spacing, width, height, (0, 0, 0, .5))
    if is_inside_2d_rect(self.mouse_pos, self.x, self.y - spacing, width, height):
        if context.tool_settings.sculpt.show_brush:
            context.tool_settings.sculpt.show_brush = False
        mouse_y = self.mouse_pos[1]
        tool_y = 0
        for i, tool in enumerate(reversed(tool_text)):
            if mouse_y < self.y + tool_height * (i + 1) - half_spacing:
                tool_y = self.y + tool_height * i - half_spacing
                self.hover_tool = tool[1]
                break
        if tool_y != 0:
            Draw_2D_Rectangle(self.x, tool_y, width, tool_height, blue)
        else:
            self.hover_tool = Tool.NONE
    else:
        self.hover_tool = None
        if not context.tool_settings.sculpt.show_brush:
            context.tool_settings.sculpt.show_brush = True
    Draw_2D_Line([self.x, header_y], [self.x + width, header_y], (1, 1, 1, .5))
    Draw_Text(self.x + spacing, header_y + header_height / 2.5, "Tools", 18, 0)

    tx = self.x + spacing
    for tool in tool_text:
        Draw_Text(
            tx, self.y + tool_height * (num_tools - tool[1].value),  # position
            str(tool[1].value) + " :  " + tool[0], 18, 0,  # text and size
            *orange if self.active_tool == tool[1] else white  # color
        )


'''
    if self.screen_points:
        Draw_2D_Lines(self.screen_points)
        Draw_2D_Lines(self.screen_points[:-1])
        Draw_2D_Points(self.screen_points)
        if self.active_point:
            Draw_2D_Points([self.active_point], (1, 0, 0, 1))

    if self.space_points:
        Draw_3D_Lines(self.space_points)
        Draw_3D_Points(self.space_points)
        if self.active_point_3d:
            Draw_3D_Points([self.active_point_3d], (1, 0, 0, 1))
'''
