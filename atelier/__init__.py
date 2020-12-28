# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

'''
    Copyright (C) 2019-2020 Juan Fran Matheu G.
    Contact: jfmatheug@gmail.com
'''

bl_info = {
    "name" : "AtelierSculpt",
    "author" : "J. Fran Matheu (@jfranmatheu)",
    "description" : "New and custom UI plus brand new Sculpt Tools for Sculpt Mode! :D",
    "blender" : (2, 91, 0),
    "version" : (2, 0, 0),
    "location" : "Everywhere in Sculpt Mode!",
    "warning" : "Beta version! REMAKE OF BLENDER ATELIER: SCULPT",
    "category" : "Generic"
}

# ----------------------------------------------------------------- #
# PRE-CHECKING
# ----------------------------------------------------------------- #
from os.path import basename, dirname, realpath
root = dirname(realpath(__file__))

if basename(root) != "AtelierSculpt":
    message = ("\n\n"
        "The name of the folder containing this addon has to be 'AtelierSculpt'.\n"
        "Please rename it.")
    raise Exception(message)

# ----------------------------------------------------------------- #
# INITIALIZATION - DEPENDENCIES
# ----------------------------------------------------------------- #
'''
try:
    import mouse
except Exception as e:
    print(e, "Package have to be installed")
    from .utils.package_installer import admin_install_package
    admin_install_package('mouse')
'''

# ----------------------------------------------------------------- #
# REGISTRATION
# ----------------------------------------------------------------- #

def register():
    from .icons import load_icons
    load_icons()

    from .addon_utils import register as register_addon_utils
    #from .data import register as register_data
    from .tools import register as register_tools
    from .custom_ui import register as register_interface

    register_addon_utils()
    #register_data()
    register_tools()
    
    try:
        from .experimental import register as register_experimental
    except:
        pass
    finally:
        register_experimental()
    
    register_interface()

def unregister():
    from .addon_utils import unregister as unregister_addon_utils
    #from .data import unregister as unregister_data
    from .tools import unregister as unregister_tools
    from .custom_ui import unregister as unregister_interface

    # REVERSED
    unregister_interface()
    
    try:
        from .experimental import unregister as unregister_experimental
    except:
        pass
    finally:
        unregister_experimental()
    
    unregister_tools()
    #unregister_data()
    unregister_addon_utils()


    from .icons import remove_icons
    remove_icons()
