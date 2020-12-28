#  ***** BEGIN GPL LICENSE BLOCK *****
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  ***** END GPL LICENSE BLOCK *****

# INFORMATION #
# THIS CODE IS BASED ON THE ADDON BRUSH QUICKSET BY Jean Ayer
# EXTENDED, IMPROVED AND SOME BUG_ FIXES BY jfranmatheu


def register():
    from .ops import classes
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    from .data import RMBPG
    register_class(RMBPG)

    from bpy.types import Scene as scn
    from bpy.props import PointerProperty as Pointer
    scn.bas_rmb = Pointer(type=RMBPG)
    
    from . km import register_keymap
    register_keymap()

def unregister():
    from . km import unregister_keymap
    unregister_keymap()
    
    from bpy.utils import unregister_class
    from bpy.types import Scene as scn
    del scn.bas_rmb

    from .ops import classes
    for cls in reversed(classes):
        unregister_class(cls)
    
    from .data import RMBPG
    unregister_class(RMBPG)
