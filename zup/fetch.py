from urllib.request import urlopen, urlretrieve
from pathlib import Path
from time import time
from itertools import cycle
import tempfile
import tarfile
import zipfile
import shutil
import json
import math
import os


def index(url):
    with urlopen(url) as response:
        return json.load(response)


def release(url, dest):
    with tempfile.TemporaryDirectory() as tmp_dir:
        fname = Path(url).name
        print(f'\t⌕ {fname}')
        path, _ = urlretrieve(url,
                                filename=Path(tmp_dir) / fname,
                                reporthook=download_hook(unit=(1048576, 'MiB')))
        unpack(path, dest)


def download_hook(unit):
    t = time()
    (unit_sz, unit_name) = unit
    def inner(blk, blksz, sz):
        dl_sz = blksz * blk
        sz_unit = sz / unit_sz
        dl_sz_unit = min(dl_sz / unit_sz, sz_unit)
        unit_s = dl_sz_unit / (time() - t)
        print(f'\t⭳ {dl_sz_unit:.2f}{unit_name} / {sz_unit:.2f}{unit_name} @ {unit_s:.2f}{unit_name}/s',
              end='\n' if sz / blksz <= blk else '\r')
    return inner


def unpack(path, dest):
    if tarfile.is_tarfile(path):
        with tarfile.open(path, 'r') as tf:
            tf.extractall(dest, members=unpack_hook(tf, path.stem.rsplit('.', 1)[0]))
    elif zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as zf:
            zf.extractall(dest, members=unpack_hook(zf.namelist(), path.stem))
    else:
        print(f'{path} is unsupported archive format.\nThis is a bug.')

def unpack_hook(files, name):
    spinner = cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
    t = 0
    for f in files:
        if time() - t > 0.05:
            t = time()
            print(f'\t➥ {next(spinner)}', end='\r')
        yield f
    print(f'\t➥ {name}')
