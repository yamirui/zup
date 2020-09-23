import os


def is_installed(url, dest):
    try:
        for f in os.scandir(dest):
            if f.is_dir() and f.name in url:
                return f.name
    except FileNotFoundError:
        pass
    return None
