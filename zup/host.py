import platform


def target():
    system = platform.system().lower()
    system = { 'darwin': 'macos' }.get(system, system)
    return f'{platform.machine()}-{system}'
