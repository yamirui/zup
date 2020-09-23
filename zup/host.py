import platform


def cpu():
    return platform.machine()


def system():
    system = platform.system().lower()
    return { 'darwin': 'macos' }.get(system, system)


def target():
    return f'{cpu()}-{system()}'
