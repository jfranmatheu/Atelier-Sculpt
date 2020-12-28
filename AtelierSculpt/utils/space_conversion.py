from bpy_extras import view3d_utils
from . others import blender_version


def get_regiondata_view3d(_context):
    # Get region and 3d region space data
    return _context.region, _context.space_data.region_3d

def convert_3d_spaceCoords_to_2d_screenCoords(_context, _3dPos):
    region, regionData = get_regiondata_view3d(_context)
    # Returns mathutils.Vector // None if coord is behind the origin of a perspective view.
    return view3d_utils.location_3d_to_region_2d(region, regionData, _3dPos, default = None)  # Vector or None

def convert_2d_screenCoords_to_3d_spaceCoords(_context, _2dPos):
    region, regionData = get_regiondata_view3d(_context)
    # normalized 3d vector from 2d region coords to 3d space # length of 1
    vNormalized = view3d_utils.region_2d_to_vector_3d(region, regionData, _2dPos) # this returns a 3d vector (mathutils.Vector)
    # Get 3D location from relative 2d coords aligned with depth location + using the normalized vector we got
    return view3d_utils.region_2d_to_location_3d(region, regionData, _2dPos, vNormalized)

def raycast_2d_3d(_ctx, _2dPos):
    region, regionData = get_regiondata_view3d(_ctx) # get region data
    # normalized 3d vector from 2d region coords to 3d space # length of 1
    vNormalized = view3d_utils.region_2d_to_vector_3d(region, regionData, _2dPos) # this returns a 3d vector (mathutils.Vector)
    # Get view origin from relative 2d coords of the region to the 3d spcace
    origin = view3d_utils.region_2d_to_origin_3d(region, regionData, _2dPos)
    # hit, pos, normal, index, obj, matrix
    return _ctx.scene.ray_cast(_ctx.view_layer if blender_version()[1] < 91 else _ctx.view_layer.depsgraph, origin, vNormalized, distance=1e+10) # distance can be higher
