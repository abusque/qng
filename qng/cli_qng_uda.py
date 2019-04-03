import argparse
import json
import operator
import os
import random
import sys
import unicodedata
from typing import Optional

import qng
from qng import common


def _parse_args():
    parser = argparse.ArgumentParser(description=qng.__description__)
    parser.add_argument('--gender', '-g', choices=['male', 'female'],
                        help='Filter first names by gender')
    parser.add_argument('--snake-case', '-s', action='store_true',
                        help='Print names in "snake_case" format')
    parser.add_argument('--type', '-t', choices=['actor', 'host', 'singer'],
                        help='Filter names by UDA membership type')
    args = parser.parse_args()
    return args


def _read_name_file(filename: str):
    file_path = os.path.join(common._DATA_DIR, f'uda-{filename}.json')

    with open(file_path) as f:
        names = json.load(f)

    return names


def _append_entries(entries, filename_male, filename_female, gender):
    if gender == 'male' or gender is None:
        entries += _read_name_file(filename_male)

    if gender == 'female' or gender is None:
        entries += _read_name_file(filename_female)


def _get_random_entry(entries):
    return entries[random.randrange(len(entries))]


def _run(args):
    entries = []

    if args.type:
        if args.type == 'actor':
            _append_entries(entries, 'actors', 'actresses', args.gender)
        elif args.type == 'host':
            _append_entries(entries, 'hosts-m', 'hosts-f', args.gender)
        elif args.type == 'singer':
            _append_entries(entries, 'singers-m', 'singers-f', args.gender)
    else:
        _append_entries(entries, 'actors', 'actresses', args.gender)
        _append_entries(entries, 'hosts-m', 'hosts-f', args.gender)
        _append_entries(entries, 'singers-m', 'singers-f', args.gender)

    entry = _get_random_entry(entries)
    common._print_name(entry['name'], entry['surname'], args.snake_case)


def main():
    args = _parse_args()

    try:
        _run(args)
    except KeyboardInterrupt:
        sys.exit(1)
