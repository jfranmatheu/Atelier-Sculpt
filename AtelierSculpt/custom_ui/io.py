from .. import __package__ as main_package


def save_actual_ui_state(context):
    from .blocks.block_data import blocks
    if not blocks:
        return False

    save_path = context.preferences.addons[main_package].preferences.get_custom_ui_presets(True)
    if save_path == "" or save_path == 'NONE':
        from os.path import join
        save_path = join(context.preferences.addons[main_package].preferences.saved_custom_ui_folder,  "autosave.json")

    strings = []
    for block in blocks:
        strings.append(block.id)

    data = {
        'blocks' : strings
    }

    import json

    with open(save_path, 'w+', encoding='utf-8') as json_file: # Después de salir del bloque del "with" el archivo es cerrado automáticamente
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    return True


def duplicate_custom_ui_preset(context):
    from .blocks.block_data import blocks
    if not blocks:
        return False

    save_path = context.preferences.addons[main_package].preferences.get_custom_ui_presets(False)

    last_char = save_path[-1:]
    if last_char.isnumeric():
        new_num = int(last_char) + 1
        save_path += str(new_num)
    else:
        save_path += "_1"

    save_path += ".json"

    from os.path import isfile
    if isfile(save_path):
        print("Save path is not file")
        return False

    strings = []
    for block in blocks:
        strings.append(block.id)

    data = {
        'blocks' : strings
    }

    import json

    with open(save_path, 'w+', encoding='utf-8') as json_file: # Después de salir del bloque del "with" el archivo es cerrado automáticamente
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    # UPDATE ACTIVE PRESET SLOT TO NEW ONE
    # TODO
    return True

def create_custom_ui_preset(context, preset_name):
    from .blocks.block_data import blocks
    if preset_name == "":
        return False

    from os.path import join, isfile
    preset_name += ".json" if not preset_name.endswith('.json') else preset_name
    save_path = join(context.preferences.addons[main_package].preferences.saved_custom_ui_folder,  preset_name)

    if isfile(save_path):
        return False

    strings = []
    for block in blocks:
        strings.append(block.id)

    data = {}

    import json

    with open(save_path, 'x', encoding='utf-8') as json_file: # Después de salir del bloque del "with" el archivo es cerrado automáticamente
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    # UPDATE ACTIVE PRESET SLOT TO NEW ONE
    # TODO
    return True


def load_custom_ui_preset(context):
    from .blocks.block_data import UI_Block, blocks
    from os.path import isfile, join

    blocks.clear()

    prefs = context.preferences.addons[main_package].preferences

    if prefs.custom_ui_presets == 'NONE':
        sculpt_ui_config = ""
    else:
        sculpt_ui_config = prefs.get_custom_ui_presets(True)
    #else:
    #    sculpt_ui_config = join(prefs.saved_custom_ui_folder, prefs.custom_ui_presets) #prefs.sculpt_custom_ui_filepath

    if sculpt_ui_config == "" or not isfile(sculpt_ui_config):
        # LOAD DEFAULT UI CONFIG
        from .config.default_config import default_sculpt_config
        sculpt_ui_config = default_sculpt_config

        if not isfile(sculpt_ui_config):
            print("Default config is not file")
            return False

    import json

    data = {}
    print("[ATELIER SCULPT] Loading custom Sculpt UI from:", sculpt_ui_config)

    with open(sculpt_ui_config, 'r', encoding='utf-8') as json_file:
        if not json_file:
            print("Default config no json")
            return False
        data = json.load(json_file)
        if data == {}:
            print("Default config none")
            return False

        #print(data)

        blocks_str = data.get('blocks', None)
        if not blocks_str:
            return False

        #print(blocks_str)

        for str in blocks_str:
            UI_Block(str)

    return True

def reset_custom_ui_preset(context):
    from .blocks.block_data import UI_Block
    from os.path import isfile, join

    UI_Block.clear()

    # LOAD DEFAULT UI CONFIG
    from .config.default_config import default_sculpt_config
    sculpt_ui_config = default_sculpt_config

    if not isfile(sculpt_ui_config):
        return False

    # READ DEFAULT CONFIG FILE
    import json

    data = {}

    with open(sculpt_ui_config, 'r', encoding='utf-8') as json_file:
        if not json_file:
            return False
        data = json.load(json_file)
        if data == {} or data is None:
            return False

        #print(data)

        blocks_str = data.get('blocks', None)
        if not blocks_str:
            return False

        for str in blocks_str:
            UI_Block(str)

    save_path = context.preferences.addons[main_package].preferences.get_custom_ui_presets(True)
    if save_path == "" or save_path == 'NONE':
        from os.path import join
        save_path = join(context.preferences.addons[main_package].preferences.saved_custom_ui_folder,  "autosave.json")

    # WRITE DEFAULT CONFIG TO ACTIVE PRESET FILE
    with open(save_path, 'w+', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    return True


def remove_custom_ui(context):
    from .blocks.block_data import UI_Block
    from os.path import isfile

    UI_Block.clear()

    prefs = context.preferences.addons[main_package].preferences
    preset = prefs.get_custom_ui_presets(True)

    if not isfile(preset):
        return False

    import os
    os.remove(preset)

    return True
