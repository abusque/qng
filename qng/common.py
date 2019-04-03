import argparse
import json
import operator
import os
import random
import sys
import unicodedata
import re
from typing import Optional

import qng


_BASE_DIR = os.path.dirname(os.path.realpath(__file__))
_DATA_DIR = os.path.join(_BASE_DIR, 'data')


def _validate_snake_kebab_args(args):
    if args.kebab_case and args.snake_case:
        print('Cannot specify --snake-case and --kebab-case.', file=sys.stderr)
        sys.exit(1)


def _strip_diacritics(string: str) -> str:
    return (
        unicodedata.normalize('NFKD', string)
        .encode('ascii', 'ignore')
        .decode('utf-8')
    )


def _snakebabify_name(name: str, sep: str) -> str:
    name = _strip_diacritics(name)
    name = name.lower()
    name = re.sub(r'[^a-zA-Z0-9_]', sep, name)
    return name


class _Format:
    DEFAULT = 0
    SNAKE = 1
    KEBAB = 2


def _format_name(name: str, surname: str, fmt=_Format.DEFAULT) -> str:
    if fmt == _Format.DEFAULT:
        full_name = f'{name} {surname}'
    elif fmt == _Format.SNAKE:
        name = _snakebabify_name(name, '_')
        surname = _snakebabify_name(surname, '_')
        full_name = f'{name}_{surname}'
    elif fmt == _Format.KEBAB:
        name = _snakebabify_name(name, '-')
        surname = _snakebabify_name(surname, '-')
        full_name = f'{name}-{surname}'

    return full_name


def _print_name(name: str, surname: str, args):
    fmt = _Format.DEFAULT

    if args.snake_case:
        fmt = _Format.SNAKE
    elif args.kebab_case:
        fmt = _Format.KEBAB

    full_name = _format_name(name, surname, fmt=fmt)
    print(full_name)
