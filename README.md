# zup

### dependencies
* Python 3.8

### Installation
```bash
$ pip install zup
```

### Installing Zig
This will install latest master Zig release and set it as default `zig` command in your system.

Note that zup never modifies your system configuration and you must add the symlink directory that zup manages to your `%PATH%` on Windows or `$PATH` on other platforms.
```bash
zup install master -d
```

### Configuration
Config file is a python script that gets executed before any command is ran.
It can be opened with `zup config`.

```python
# config.py
# windows: Path(os.getenv('APPDATA')) / 'zup/config.py'
# macos: Path.home() / 'Library/Preferences/zup/config.py'
# other: Path.home() / '.config/zup/config.py'

# url where index will be fetched from
# default: 'https://ziglang.org/download/index.json'
index_url = zup.config.default_index_url()

# directory where zig compilers are installed
# windows: Path(os.getenv('LOCALAPPDATA')) / 'zup'
# macos: Path.home() / 'Library/Application Support/zup'
# other: Path.home() / '.local/share/zup'
install_dir = zup.config.default_install_dir()

# directory where symlinks to compilers are created
# windows: install_dir
# macos: install_dir
# other: Path.home() / '.local/bin'
symlink_dir = zup.config.default_symlink_dir()
```

