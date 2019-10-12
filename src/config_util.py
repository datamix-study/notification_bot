import os
from configparser import ConfigParser
from pathlib import Path


def get_config() -> ConfigParser:
    file_name = 'config_prod.ini' if os.getenv('notification_bot_env') == 'prod' else 'config.ini'
    abs_path = to_resource_file_abs_path(file_name)
    if not abs_path.exists():
        raise FileNotFoundError('resource file does not exist: {}'.format(abs_path))
    config = ConfigParser()
    config.read(abs_path.resolve(), 'UTF-8')
    return config


def to_resource_file_abs_path(file_name: str) -> Path:
    return Path(os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources', file_name)))
