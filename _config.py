from os import path
from pathlib import Path
from json import load

config_file = "config.json"

project_dir = Path(__file__).parent
config_path = path.join(project_dir, 'config.json')

if not path.exists(config_path):
    raise FileNotFoundError('Configuration file was not found')

with open(config_file, 'r') as fp:
    config: dict[dict] = load(fp)

coloring: dict[str] = config.get("coloring")
keybindings: dict[str] = config.get("keybindings")

class colors:
    valid_command = coloring.get("valid_command")
    invalid_command = coloring.get("invalid_command")
    quoted_string_complete = coloring.get("quoted_string_complete")
    quoted_string_incomplete = coloring.get("quoted_string_incomplete")
    flags = coloring.get("flags")
    path_exists = coloring.get("path_exists")
    numeric = coloring.get("colorint")
    comment = coloring.get("comment")

class bindings:
        end_of_line = keybindings.get("end_of_line")
        end_of_file = keybindings.get("end_of_file")
        keyboard_interrupt = keybindings.get("keyboard_interrupt")
        history_navigate_up = keybindings.get("history_navigate_up")
        history_navigate_down = keybindings.get("history_navigate_down")
        line_navigate_left = keybindings.get("line_navigate_left")
        line_navigate_right = keybindings.get("line_navigate_right")
        line_navigate_begin = keybindings.get("line_navigate_begin")
        line_navigate_end = keybindings.get("line_navigate_end")
        delete_on_current_position = keybindings.get("delete_on_current_position")
        delete_previous_position = keybindings.get("delete_previous_position")
        delete_previous_word = keybindings.get("delete_previous_word")
        autocomplete = keybindings.get("autocomplete")