from bpy import context as C
from bpy.props import FloatVectorProperty
from bpy.types import Panel
from ...icons import Icon
from ... import __package__ as main_package

# ----------------------------------------------------------------- #
#   DYNTOPO SETUP                                                   #
# ----------------------------------------------------------------- #

# Values for Detail Size depending of the METHOD used
# LEFT (LOW) - CENTER (MID) - RIGHT (HIGH)
# RELATIVE & MANUAL --> a menor valor, mayor detalle. Valor en px.
relative_Low =  [14, 12, 10]
relative_Mid =  [ 8,  6,  4]
relative_High = [ 3,  2,  1]
# CONSTANT --> a mayor valor, mayor detalle. Valor fixed. (Aquí los valores están invertidos)
constant_Low =  [20,  30,  40]
constant_Mid =  [55,  65,  75]
constant_High = [95, 110, 125]
# BRUSH --> a menor, mayor detalle. Valor en % de detalle.
brush_Low =     [65, 55, 45]
brush_Mid =     [35, 27, 20]
brush_High =    [15, 10,  5]
# LEVEL OF DETAIL GROUPS FOR EACH STAGE # DE MOMENTO AHÍ SE QUEDA AUNQUE SE PODRÍA USAR (para array 3 dimensiones)
# sketch_Values = [relative_Low, constant_Low, brush_Low]
# detail_Values = [relative_Mid, constant_Mid, brush_Mid]
# polish_Values = [relative_High, constant_High, brush_High]
# STRUCT CLASS
class DyntopoStage:
    # BRUSH VALUES
    relative_Values : FloatVectorProperty(
        subtype='NONE', default=[0, 0, 0],
        size=3,
    )
    constant_Values : FloatVectorProperty(
        subtype='NONE', default=[0, 0, 0],
        size=3,
    )
    brush_Values : FloatVectorProperty(
        subtype='NONE', default=[0, 0, 0],
        size=3,
    )

    def __init__(self, stage_Name, relative_Values = [], constant_Values =[], brush_Values = []):
        self.stage_Name = stage_Name
        self.relative_Values = relative_Values
        self.constant_Values = constant_Values
        self.brush_Values = brush_Values

    def __repr__(self):
        return "DyntopoStage[%s, %i[], %i[], %i[]]" % (self.stage_Name, self.relative_Values, self.constant_Values, self.brush_Values)

# IN LOAD / IF USE CUSTOM VALUES IS CHECKED, GO CREATE DYNSTAGES VALUES WITH PREFS VALUES
try:
    prefs = C.preferences.addons[main_package].preferences
    if prefs.dyntopo_use_custom_values:
        rL = [prefs.relative_Low[0], prefs.relative_Low[1], prefs.relative_Low[2]]
        rM = [prefs.relative_Mid[0], prefs.relative_Mid[1], prefs.relative_Mid[2]]
        rH = [prefs.relative_High[0], prefs.relative_High[1], prefs.relative_High[2]]
        cL = [prefs.constant_Low[0], prefs.constant_Low[1], prefs.constant_Low[2]]
        cM = [prefs.constant_Mid[0], prefs.constant_Mid[1], prefs.constant_Mid[2]]
        cH = [prefs.constant_High[0], prefs.constant_High[1], prefs.constant_High[2]]
        bL = [prefs.brush_Low[0], prefs.brush_Low[1], prefs.brush_Low[2]]
        bM = [prefs.brush_Mid[0], prefs.brush_Mid[1], prefs.brush_Mid[2]]
        bH = [prefs.brush_High[0], prefs.brush_High[1], prefs.brush_High[2]]
        dynStage_Low = DyntopoStage("SKETCH", rL, cL, bL)
        dynStage_Mid = DyntopoStage("DETAILS", rM, cM, bM)
        dynStage_High = DyntopoStage("POLISH", rH, cH, bH)
    # IF NOT, GO CREATE DYNSTAGES VALUES WITH DEFAULT VALUES
    else:
        dynStage_Low = DyntopoStage("SKETCH", relative_Low, constant_Low, brush_Low)
        dynStage_Mid = DyntopoStage("DETAILS", relative_Mid, constant_Mid, brush_Mid)
        dynStage_High = DyntopoStage("POLISH", relative_High, constant_High, brush_High)
except:
    dynStage_Low = DyntopoStage("SKETCH", relative_Low, constant_Low, brush_Low)
    dynStage_Mid = DyntopoStage("DETAILS", relative_Mid, constant_Mid, brush_Mid)
    dynStage_High = DyntopoStage("POLISH", relative_High, constant_High, brush_High)

dyntopoStages = [dynStage_Low, dynStage_Mid, dynStage_High]

def dynStage_toString(_dynStage):
    s_dynStage = ""
    if _dynStage == '1':
        s_dynStage = "SKETCH"
    elif _dynStage == '2':
        s_dynStage = "DETAIL"
    elif _dynStage == '3':
        s_dynStage = "POLISH"
    return s_dynStage

# --------------------------------------------- #
# DYNTOPO STAGES UI PANEL
# --------------------------------------------- #
class BAS_PT_dyntopo_stages(Panel):
    bl_label = "DyntopoStages"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "NONE"
    bl_category = 'Sculpt'
    bl_description = "Stages Panel. Stages improve and divide the workflow in 3 stages and each one has 3 nice values to work with. (also depending of the detailing method)"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        dyntopo = context.scene.bas_dyntopo
        dyn_stage = dyntopo.stage
        use_stage = dyntopo.toggle_stages
        if(context.sculpt_object.use_dynamic_topology_sculpting == True):
            method = dyntopo.detailing
            icon_H = Icon.DYNTOPO_HIGH()
            icon_M = Icon.DYNTOPO_MEDIUM()
            icon_L = Icon.DYNTOPO_LOW()
            wm = context.window_manager
        # STAGES - SKETCH - DETAIL - POLISH
            layout = self.layout
            row = layout.row(align=True)
            #row.label(text="Stage :   ")
            if use_stage:
                row.label(text="DEFAULT MODE")
                row = layout.row(align=True)
                row.prop(dyntopo, 'toggle_stages', text="USE STAGES !", toggle=True, invert_checkbox=True)

            else:
                row.label(text="Actual Stage :    " + dynStage_toString(dyn_stage))
                row.prop(dyntopo, 'toggle_stages', text="", icon='LOOP_BACK', toggle=True, expand=True)
                # STAGES
                col = layout.column()
                row = col.row(align=True)
                row.prop(dyntopo, 'stage', text="Sketch", toggle=True, expand=True)

        # DETAIL METHODS
            col = layout.column()
            row = col.row(align=True)
            if method == 'CONSTANT':
                icon = Icon.DYNTOPO_CONSTANT()
            elif method == 'BRUSH':
                icon = Icon.DYNTOPO_BRUSH()
            elif method == 'RELATIVE': # RELATIVE OR MANUAL
                icon = Icon.DYNTOPO_RELATIVE()
            elif method == 'MANUAL':
                icon = Icon.DYNTOPO_MANUAL()
            row.label(icon_value=icon, text="Detailing Method :   " + method) # Stages - Para niveles de Detalle especificados abajo
            col = layout.column()
            row = col.row(align=True)
            row.prop(dyntopo, 'detailing', text="Relative", toggle=True, expand=True) #icon_value=icon1.icon_id

            if not use_stage:
            # LOOK FOR ACTIVE STAGE
                n = int(dyn_stage) - 1
            # VALUES FOR STAGES
                prefs = context.preferences.addons[main_package].preferences # load preferences (for properties)
                rowH = self.layout.row(align=True)
                rowH.ui_units_x = 5
                rowH.scale_x = 5
                rowH.label(text="Values :") # Valores para el 'Stage' Activo
                rowH.ui_units_x = 9
                rowH.scale_x = 9
                rowH.prop(prefs, "dyntopo_use_custom_values", toggle=False, text="Use Custom Values") # OUTLINER_DATA_GP_LAYER
                row = self.layout.row(align=True)
                if method == 'CONSTANT':
                    row.label(icon_value=icon_L, text=str(dyntopoStages[n].constant_Values[0]))
                    row.label(icon_value=icon_M, text=str(dyntopoStages[n].constant_Values[1]))
                    row.label(icon_value=icon_H, text=str(dyntopoStages[n].constant_Values[2]))
                elif method == 'BRUSH':
                    row.label(icon_value=icon_L, text=str(dyntopoStages[n].brush_Values[0]))
                    row.label(icon_value=icon_M, text=str(dyntopoStages[n].brush_Values[1]))
                    row.label(icon_value=icon_H, text=str(dyntopoStages[n].brush_Values[2]))
                elif method == 'RELATIVE' or 'MANUAL':
                    row.label(icon_value=icon_L, text=str(dyntopoStages[n].relative_Values[0]))
                    row.label(icon_value=icon_M, text=str(dyntopoStages[n].relative_Values[1]))
                    row.label(icon_value=icon_H, text=str(dyntopoStages[n].relative_Values[2]))
                else:
                    row.label(text="NONE! Select a Stage!")

                self.layout.separator()

                if prefs.dyntopo_use_custom_values:
                    _col = self.layout.column(align=True)
                    _col.prop(dyntopo, "stages_edit_values", toggle=True, icon="GREASEPENCIL", text="Edit Values") # OUTLINER_DATA_GP_LAYER
                    if dyntopo.stages_edit_values:
                        box = _col.box()
                        _row = box.row(align=True)

                        stage = dyntopo.stage
                        if method == 'CONSTANT':
                            if stage == '3': # "Polish":
                                _row.prop(prefs, "dyntopo_constant_high", text="")
                            elif stage == '2': # "Details":
                                _row.prop(prefs, "dyntopo_constant_mid", text="")
                            elif stage == '1': #  "Sketch":
                                _row.prop(prefs, "dyntopo_constant_low", text="")

                        elif method == 'RELATIVE': # RELATIVE OR MANUAL
                            if stage == '3': # "Polish":
                                _row.prop(prefs, "dyntopo_relative_high", text="")
                            elif stage == '2': #  "Details":
                                _row.prop(prefs, "dyntopo_relative_mid", text="")
                            elif stage == '1': #  "Sketch":
                                _row.prop(prefs, "dyntopo_relative_low", text="")

                        elif method == 'BRUSH':
                            if stage == '3': #  "Polish":
                                _row.prop(prefs, "dyntopo_brush_high", text="")
                            elif stage == '2': #  "Details":
                                _row.prop(prefs, "dyntopo_brush_mid", text="")
                            elif stage == '1': #  "Sketch":
                                _row.prop(prefs, "dyntopo_brush_low", text="")
