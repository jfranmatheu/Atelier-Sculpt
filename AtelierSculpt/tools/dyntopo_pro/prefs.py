from .ui import dyntopoStages


# Relative
def update_relativeLow(self, context):
    dyntopoStages[0].relative_Values = self.dyntopo_relative_low
def update_relativeMid(self, context):
    dyntopoStages[1].relative_Values = self.dyntopo_relative_mid
def update_relativeHigh(self, context):
    dyntopoStages[2].relative_Values = self.dyntopo_relative_high
# Constant
def update_constantLow(self, context):
    dyntopoStages[0].constant_Values = self.dyntopo_constant_low
def update_constantMid(self, context):
    dyntopoStages[1].constant_Values = self.dyntopo_constant_mid
def update_constantHigh(self, context):
    dyntopoStages[2].constant_Values = self.dyntopo_constant_high
# Brush
def update_brushLow(self, context):
    dyntopoStages[0].brush_Values = self.dyntopo_brush_low
def update_brushMid(self, context):
    dyntopoStages[1].brush_Values = self.dyntopo_brush_mid
def update_brushHigh(self, context):
    dyntopoStages[2].brush_Values = self.dyntopo_brush_high

'''
dyntopo_properties = {
    # DYNTOPO LEVELS
    'dyntopo_levels_relative' : (
        'FloatVectorProperty',
        {
            'name'          : "Dyntopo Relative Levels",
            'description'   : "",
            'subtype'       : 'NONE',
            'default'       : [12, 9, 6, 4, 2, 1],
            'size'          : 6,
            'step'          : 1
        }
    ),
    'dyntopo_levels_constant' : (
        'FloatVectorProperty',
        {
            'name'          : "Dyntopo Constant Levels",
            'description'   : "",
            'subtype'       : 'NONE',
            'default'       : [35, 50, 65, 80, 100, 125],
            'size'          : 6,
            'step'          : 1
        }
    ),
    'dyntopo_levels_brush' : (
        'FloatVectorProperty',
        {
            'name'          : "Dyntopo Brush Levels",
            'description'   : "",
            'subtype'       : 'NONE',
            'default'       : [48, 32, 24, 16, 10, 5],
            'size'          : 6,
            'step'          : 1
        }
    ),
    # USE CUSTOM DYNTOPO VALUES
    'dyntopo_use_custom_values': (
        'BoolProperty',
        {
            'name'          : "Custom Values",
            'description'   : "Use Custom Values for Dyntopo's new system by levels and stages",
            'default'       : False
        }
    ),
    # RELATIVE VALUES
    'dyntopo_relative_low' : (
        'FloatVectorProperty',
        {
            'name'          :   "Relative Low Value",
            'description'   :   "",
            'subtype'       :   'NONE',
            'default'       :   [14, 12, 10],
            'soft_min'      :   10,
            'soft_max'      :   20,
            'size'          :   3,
            'step'          :   1,
            'precision'     :   0,
            'update'        :   'update_relativeLow'
        }
    ),
    'dyntopo_relative_mid' : (
        'FloatVectorProperty',
        {
            'name'          :   "Relative Mid Value",
            'description'   :   "",
            'subtype'       :   'NONE',
            'default'       :   [8, 6, 4],
            'soft_min'      :   4,
            'soft_max'      :   10,
            'size'          :   3,
            'step'          :   1,
            'precision'     :   0,
            'update'        :   'update_relativeMid'
        }
    ),
    'dyntopo_relative_high' : (
        'FloatVectorProperty',
        {
            'name'          :   "Relative Mid Value",
            'description'   :   "",
            'subtype'       :   'NONE',
            'default'       :   [3, 2, 1],
            'soft_min'      :   0.1,
            'soft_max'      :   4,
            'size'          :   3,
            'step'          :   1,
            'precision'     :   0,
            'update'        :   'update_relativeHigh'
        }
    ),
    # CONSTANT VALUES
    'dyntopo_constant_low' : (
        'FloatVectorProperty',
        {
            'name'          :   "Constant Low Value",
            'description'   :   "",
            'subtype'       :   'NONE',
            'default'       :   [20, 30, 40],
            'soft_min'      :   0.1,
            'soft_max'      :   50,
            'size'          :   3,
            'step'          :   1,
            'precision'     :   0,
            'update'        :   'update_constantLow'
        }
    ),
    'dyntopo_constant_mid' : (
        'FloatVectorProperty',
        {
            'name'          :   "Constant Mid Value",
            'description'   :   "",
            'subtype'       :   'NONE',
            'default'       :   [55, 65, 75],
            'soft_min'      :   50,
            'soft_max'      :   95,
            'size'          :   3,
            'step'          :   1,
            'precision'     :   0,
            'update'        :   'update_constantMid'
        }
    ),
    'dyntopo_constant_high' : (
        'FloatVectorProperty',
        {
            'name'          :   "Constant High Value",
            'description'   :   "",
            'subtype'       :   'NONE',
            'default'       :   [95, 110, 125],
            'soft_min'      :   95,
            'soft_max'      :   200,
            'size'          :   3,
            'step'          :   1,
            'precision'     :   0,
            'update'        :   'update_constantHigh'
        }
    ),
    # BRUSH VALUES
    'dyntopo_brush_low' : (
        'FloatVectorProperty',
        {
            'name'          :   "Brush Low Value",
            'description'   :   "",
            'subtype'       :   'NONE',
            'default'       :   [65, 55, 45],
            'soft_min'      :   50,
            'soft_max'      :   100,
            'size'          :   3,
            'step'          :   1,
            'precision'     :   0,
            'update'        :   'update_brushLow'
        }
    ),
    'dyntopo_brush_mid' : (
        'FloatVectorProperty',
        {
            'name'          :   "Brush Mid Value",
            'description'   :   "",
            'subtype'       :   'NONE',
            'default'       :   [35, 27, 20],
            'soft_min'      :   20,
            'soft_max'      :   50,
            'size'          :   3,
            'step'          :   1,
            'precision'     :   0,
            'update'        :   'update_brushMid'
        }
    ),
    'dyntopo_brush_high' : (
        'FloatVectorProperty',
        {
            'name'          :   "Brush High Value",
            'description'   :   "",
            'subtype'       :   'NONE',
            'default'       :   [15, 10, 5],
            'soft_min'      :   0.1,
            'soft_max'      :   20,
            'size'          :   3,
            'step'          :   1,
            'precision'     :   0,
            'update'        :   'update_brushHigh'
        }
    )
}
'''

dyntopo_properties = '''
# DYNTOPO LEVELS
dyntopo_levels_relative : FloatVectorProperty(
    name="Dyntopo Relative Levels", description="",
    subtype='NONE', default=[12, 9, 6, 4, 2, 1],
    size=6, step=1
)
dyntopo_levels_constant : FloatVectorProperty(
    name="Dyntopo Constant Levels", description="",
    subtype='NONE', default=[35, 50, 65, 80, 100, 125],
    size=6, step=1
)
dyntopo_levels_brush : FloatVectorProperty(
    name="Dyntopo Brush Levels", description="",
    subtype='NONE', default=[48, 32, 24, 16, 10, 5],
    size=6, step=1
)
# USE CUSTOM DYNTOPO VALUES
dyntopo_use_custom_values: BoolProperty(
    name="Custom Values",
    description="Use Custom Values for Dyntopo's new system by levels and stages",
    default=False,
)
# RELATIVE VALUES
dyntopo_relative_low : FloatVectorProperty(
    name="Relative Low Value", description="",
    subtype='NONE', default=[14, 12, 10], soft_min=10, soft_max=20,
    size=3, step=1, precision=0 ,update=update_relativeLow
)
dyntopo_relative_mid : FloatVectorProperty(
    name="Relative Mid Value", description="",
    subtype='NONE', default=[8, 6, 4], soft_min=4, soft_max=10,
    size=3, step=1, precision=0 ,update=update_relativeMid
)
dyntopo_relative_high : FloatVectorProperty(
    name="Relative High Value", description="",
    subtype='NONE', default=[3, 2, 1], soft_min=0.1, soft_max=4,
    size=3, precision=1 ,update=update_relativeHigh
)
# CONSTANT VALUES
dyntopo_constant_low : FloatVectorProperty(
    name="Constant Low Value", description="",
    subtype='NONE', default=[20, 30, 40], soft_min=0.1, soft_max=50,
    size=3, precision=1 ,update=update_constantLow
)
dyntopo_constant_mid : FloatVectorProperty(
    name="Constant Mid Value", description="",
    subtype='NONE', default=[55, 65, 75], soft_min=50, soft_max=95,
    size=3, step=1, precision=0 ,update=update_constantMid
)
dyntopo_constant_high : FloatVectorProperty(
    name="Constant High Value", description="",
    subtype='NONE', default=[95, 110, 125], soft_min=95, soft_max=200,
    size=3, step=1, precision=0 ,update=update_constantHigh
)
# BRUSH VALUES
dyntopo_brush_low : FloatVectorProperty(
    name="Brush Low Value", description="",
    subtype='NONE', default=[65, 55, 45], soft_min=50, soft_max=100,
    size=3, step=1, precision=0 ,update=update_brushLow
)
dyntopo_brush_mid : FloatVectorProperty(
    name="Brush Mid Value", description="",
    subtype='NONE', default=[35, 27, 20], soft_min=20, soft_max=50,
    size=3, step=1, precision=0 ,update=update_brushMid
)
dyntopo_brush_high : FloatVectorProperty(
    name="Brush High Value", description="",
    subtype='NONE', default=[15, 10, 5], soft_min=0.1, soft_max=20,
    size=3, precision=1 ,update=update_brushHigh
)
'''
