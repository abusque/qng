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


def _strip_diacritics(string: str) -> str:
    return (
        unicodedata.normalize('NFKD', string)
        .encode('ascii', 'ignore')
        .decode('utf-8')
    )


def _snakify_name(name: str) -> str:
    name = _strip_diacritics(name)
    name = name.lower()
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    return name


def _format_name(name: str, surname: str, snake_case: bool = False) -> str:
    if snake_case:
        name = _snakify_name(name)
        surname = _snakify_name(surname)
        full_name = f'{name}_{surname}'
    else:
        full_name = f'{name} {surname}'

    return full_name


def _print_name(name: str, surname: str, snake_case: bool):
    full_name = _format_name(name, surname, snake_case=snake_case)
    print(full_name)
