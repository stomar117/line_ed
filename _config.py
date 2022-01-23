import json
from pathlib import Path
config_path=Path(__file__).parent
with open(Path.joinpath(config_path,'./config.json'), 'r') as conf:
    conf_dict=json.loads(conf.read())

valid_command=conf_dict.get('valid_command')
invalid_command=conf_dict.get('invalid_command')
quoted_string_complete=conf_dict.get('quoted_string_complete')
quoted_string_incomplete=conf_dict.get('quoted_string_incomplete')
flags=conf_dict.get('flags')
bracketed=conf_dict.get('bracketed')
comment=conf_dict.get('comment')
path_exists=conf_dict.get('path_exists')