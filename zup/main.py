import argparse
import sys

import zup


@zup.command
def config(args):
    args = zup,
    zup.commands.config(*args)


@zup.command
def ls(args):
    args = (getattr(args.cfg, 'index_url', args.index),
            args.remote,
            getattr(args.cfg, 'install_dir', zup.config.default_install_dir()))
    zup.commands.ls(*args)


@zup.command
def install(args):
    args = (getattr(args.cfg, 'index_url', args.index),
            args.version,
            args.target,
            getattr(args.cfg, 'install_dir', zup.config.default_install_dir()),
            getattr(args.cfg, 'symlink_dir', zup.config.default_symlink_dir()),
            args.default,
            args.force)
    zup.commands.install(*args)


@zup.command
def remove(args):
    args = (getattr(args.cfg, 'install_dir', zup.config.default_install_dir()),
            args.name)
    zup.commands.remove(*args)


@zup.command
def default(args):
    args = (getattr(args.cfg, 'install_dir', zup.config.default_install_dir()),
            getattr(args.cfg, 'symlink_dir', zup.config.default_symlink_dir()),
            args.name)
    zup.commands.default(*args)


def main():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers()

    # config
    command = commands.add_parser('config', description='Configure zup. (opens config.py in text editor)')
    command.set_defaults(func=config)

    # list
    command = commands.add_parser('list', description='List zig compiler releases. (local by default)')
    command.add_argument('-i', '--index', help='link to the index of releases', default=zup.config.default_index_url())
    command.add_argument('-r', '--remote', action='store_true', help='list remote releases', default=False)
    command.set_defaults(func=ls)

    # install
    command = commands.add_parser('install', description='Install Zig compilers.')
    command.add_argument('-i', '--index', help='link to the index of releases', default=zup.config.default_index_url())
    command.add_argument('-t', '--target', help='target of machine using zig compiler', default=zup.host.target())
    command.add_argument('-d', '--default', action='store_true', help='make installed compiler the default', default=False)
    command.add_argument('--force', action='store_true', help='install even if version already exists', default=False)
    command.add_argument('version', help='version of the release', default='master')
    command.set_defaults(func=install)

    # remove
    command = commands.add_parser('remove', description='Remove installed Zig compilers.')
    command.add_argument('name', help='full version name')
    command.set_defaults(func=remove)

    # default
    command = commands.add_parser('default', description='Set default zig compiler. (symlink to selected version)')
    command.add_argument('name', help='full version name')
    command.set_defaults(func=default)

    if len(sys.argv) <= 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        if args.func.__name__ != 'config':
            args.cfg = zup.config.load(zup)
        sys.exit(args.func(args))
    sys.exit(0)
