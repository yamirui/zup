from pathlib import Path
import shutil
import os


def ls(dest):
    versions = []
    try:
        for f in os.scandir(dest):
            if f.is_dir():
                versions.append(f.name)
    except FileNotFoundError:
        pass
    return versions


def name_from_path(path):
    stem = Path(path).stem
    if stem.endswith('.tar'):
        return stem.rsplit('.', 1)[0]
    return stem


def is_installed(name, dest):
    try:
        for f in os.scandir(dest):
            if f.is_dir() and f.name == name:
                return f.name
    except FileNotFoundError:
        pass
    return None


def remove(dest, name):
    shutil.rmtree(Path(dest) / name, ignore_errors=True)
    print(f'\t✖ {name}')
