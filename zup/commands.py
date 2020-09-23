from pathlib import Path
import shutil
import sys

from . import fetch
from . import installs
from .error import CommandWarning, CommandError


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
            print('\n\nCancelled.')
        return 0
    return wrapper


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
            print(f'\t✖ {name}')
            shutil.rmtree(dest / Path(name), ignore_errors=True)
        else:
            raise CommandWarning(f'{name} is already installed.')
    fetch.release(url, dest)
