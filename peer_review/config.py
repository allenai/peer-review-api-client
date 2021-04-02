import json
import os

_config = {}

def get(key):
    if not _config:
        _load()
        if not _config:
            configure()
    return _config[key]

def _load():
    global _config
    config_file = os.path.join(os.path.dirname(__file__), '.config')
    if os.path.isfile(config_file):
        with open(config_file) as f:
            _config = json.load(f)

def configure():
    global _config
    _load()
    def prompt(msg, key, default=None):
        defaultValue = _config.get(key, default)
        if defaultValue:
            newValue = input(f"{msg} ({defaultValue}):")
            if not newValue:
                newValue = defaultValue
            return newValue
        else:
            return input(f"{msg}:")

    api_key = prompt("Enter API Key", "api_key")
    host = prompt("Enter host", "host", "http://conference-api.prod.s2.allenai.org")
    _config = {'api_key': api_key, 'host': host}

    with open(os.path.join(os.path.dirname(__file__), '.config'), 'w') as f:
        json.dump(_config, f)
