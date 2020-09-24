from pathlib import Path
import shutil
import sys

from .error import CommandWarning, CommandError
from . import fetch
from . import installs
from . import host
from . import config as cfg


def command(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except CommandWarning as w:
            print(f'\t⚠ {str(w)}')
        except CommandError as e:
            print(f'\t✖ {str(e)}', file=sys.stderr)
            return 1
        except KeyboardInterrupt:
            print('\n\t␘ Cancelled.')
        return 0
    return wrapper


def config():
    cfg.open_config()


def ls(index, remote, dest):
    if remote:
        if (versions := fetch.index(index)) is None:
            raise CommandError(f'Could not fetch index from "{index}".')
        for version in versions.keys():
            print(f'{version}')
            targets = versions[version]
            for target in targets.keys():
                if 'tarball' in targets[target]:
                    print(f'  {target}')
    else:
        for version in installs.ls(dest):
            print(f'{version}')


def install(index, version, target, dest, force):
    if (versions := fetch.index(index)) is None:
        raise CommandError(f'Could not fetch index from "{index}".')
    if (targets := versions.get(version, None)) is None:
        raise CommandError(f'Version "{version}" does not exist.')
    if (meta := targets.get(target, None)) is None:
        raise CommandError(f'Target "{target}" does not exist for version "{version}".')
    if (url := meta.get('tarball', None)) is None:
        raise CommandError('Could not find archived download link for this version.\nThis is a bug.')
    if name := installs.is_installed(url, dest):
        if force:
            installs.remove(dest / Path(name))
        else:
            raise CommandWarning(f'{name} is already installed.')
    fetch.release(url, dest)


def default(src, dest, name):
    if host.system() == 'windows':
        exec_ext = '.exe'
        link_ext = '.bat'
    else:
        exec_ext = ''
        link_ext = ''
    executable = Path(src) / f'{name}/zig{exec_ext}'
    link = f'{dest}/zig{link_ext}'

    if not Path(executable).is_file():
        raise CommandError(f'"{name}" is not an installed binary release.')
    host.link(executable, link)
