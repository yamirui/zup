from argparse import Namespace
from pathlib import Path
from runpy import run_path
import subprocess
import shlex
import os

from . import host


def config_path():
    if host.system() == 'windows':
        return Path(os.getenv('APPDATA')) / 'zup/config.py'
    elif host.system() == 'macos':
        return Path.home() / 'Library/Preferences/zup/config.py'
    else:
        return Path.home() / '.config/zup/config.py'


def open():
    path = config_path()
    print(f'opening {path}')
    path.parent.mkdir(parents=True, exist_ok=True)
    if host.system() == 'windows':
        os.startfile(path)
    elif host.system() == 'macos':
        subprocess.call(('open', path))
    else:
        subprocess.call(('xdg-open', path))


def load(zup):
    try:
        config = run_path(config_path(), init_globals={'zup': zup})
        return Namespace(**config)
    except FileNotFoundError:
        pass


def default_install_path():
    if host.system() == 'windows':
        return Path(os.getenv('LOCALAPPDATA')) / 'zup'
    elif host.system() == 'macos':
        return Path.home() / 'Library/Application Support/zup'
    else:
        return Path.home() / '.local/share/zup'


# Path(config_path).parent.mkdir(parents=True, exist_ok=True)
