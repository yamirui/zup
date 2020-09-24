from pathlib import Path
import contextlib
import platform
import os


def cpu():
    return platform.machine()


def system():
    system = platform.system().lower()
    return { 'darwin': 'macos' }.get(system, system)


def target():
    return f'{cpu()}-{system()}'


def link(src, dest):
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if system() == 'windows':
        with open(dest, 'w') as f:
            f.write(f'@echo off\r\n"{src}" %*')
    else:
        with contextlib.suppress(FileNotFoundError):
            os.remove(dest)
        os.symlink(src, dest)
    print(f'\t🠒 {src.parent.name}')
