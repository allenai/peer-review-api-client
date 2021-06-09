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

    api_key = prompt("Enter API Key", "api_key", "zq83r8JXjm1azwm0rmA5l6EMAE80sgfK8u3clGFL")
    url = prompt("Enter service URL", "url", "http://api.semanticscholar.org/v1/peer-review")
    _config = {'api_key': api_key, 'url': url}

    with open(os.path.join(os.path.dirname(__file__), '.config'), 'w') as f:
        json.dump(_config, f)
