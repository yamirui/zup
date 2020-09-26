from argparse import Namespace
from pathlib import Path
from runpy import run_path
import subprocess
import os

from . import host


def default_config(zup):
    return '\n'.join([
        f'# url where index will be fetched from',
        f'index_url = "{str(zup.config.default_index_url())}"',
        f'',
        f'# directory where zig compilers are installed',
        f'install_dir = "{str(zup.config.default_install_dir().as_posix())}"',
        f'',
        f'# directory where symlinks to compilers are created',
        f'symlink_dir = "{str(zup.config.default_symlink_dir().as_posix())}"'
    ])


def config_path():
    if host.system() == 'windows':
        return Path(os.getenv('APPDATA')) / 'zup/config.py'
    elif host.system() == 'macos':
        return Path.home() / 'Library/Preferences/zup/config.py'
    else:
        return Path.home() / '.config/zup/config.py'


def open_config(zup):
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.is_file():
        with open(path, 'w') as f:
            f.write(default_config(zup))
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


def default_index_url():
    return 'https://ziglang.org/download/index.json'


def default_install_dir():
    if host.system() == 'windows':
        return Path(os.getenv('LOCALAPPDATA')) / 'zup'
    elif host.system() == 'macos':
        return Path.home() / 'Library/Application Support/zup'
    else:
        return Path.home() / '.local/share/zup'


def default_symlink_dir():
    if host.system() == 'windows':
        return default_install_dir()
    elif host.system() == 'macos':
        return default_install_dir()
    else:
        return Path.home() / '.local/bin'
