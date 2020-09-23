import argparse
import sys

import zup


@zup.command
def install(args):
    # TODO: replace install dir with config parameter
    args = (args.index, args.version, args.target, './test')
    zup.commands.install(*args)


def main():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers()

    # install
    command = commands.add_parser('install', description='Install Zig compilers.')
    command.add_argument('-i', '--index', help='link to the index of releases', default='https://ziglang.org/download/index.json')
    command.add_argument('-t', '--target', help='target of machine using zig compiler', default=zup.host.target())
    command.add_argument('version', help='version of the release', default='master')
    command.set_defaults(func=install)

    if len(sys.argv) <= 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        sys.exit(args.func(args))

    sys.exit(0)
