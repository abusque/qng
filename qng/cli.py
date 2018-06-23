import argparse
import json
import operator
import os
import random
import sys
import unicodedata

import qng


_BASE_DIR = os.path.dirname(os.path.realpath(__file__))
_DATA_DIR = os.path.join(_BASE_DIR, 'data')


def _print_error(msg):
    print('qng: error: {}'.format(msg), file=sys.stderr)
    sys.exit(1)


def _parse_args():
    parser = argparse.ArgumentParser(description=qng.__description__)

    parser.add_argument('--gender', '-g', choices=['male', 'female'],
                        help='Filter first names by gender')
    parser.add_argument('-n', type=int, default=1,
                        help='Number of names to generate')
    parser.add_argument('--no-nl', '-N', action='store_true',
                        help='Do not print a newline after the generated name')
    parser.add_argument('--part', '-p', choices=['first', 'last'],
                        help='Only print first or last name')
    parser.add_argument('--print0', '-0', action='store_true',
                        help='Print a null-byte instead of newline after the generated name')
    parser.add_argument('--snake-case', '-s', action='store_true',
                        help='Print names in "snake_case" format')
    parser.add_argument('--version', '-V', action='version',
                        version='%(prog)s {}'.format(qng.__version__))
    parser.add_argument('--weighted', '-w', action='store_true',
                        help='Pick names according to their relative popularity')

    args = parser.parse_args()

    if args.n > 1 and args.no_nl:
        _print_error('argument --no-nl/-N not allowed with -n > 1')

    if args.no_nl and args.print0:
        _print_error('argument --no-nl/-N not allowed with --print0/-0')

    return args


def _read_name_file(filename):
    file_path = os.path.join(_DATA_DIR, filename)
    with open(file_path) as f:
        names = json.load(f)

    return names


def _get_names(gender=None):
    names = _read_name_file('names.json')

    if gender:
        names = [name for name in names if name['gender'] == gender]

    return names


def _get_surnames():
    return _read_name_file('surnames.json')


def _get_random_name(name_list):
    length = len(name_list)
    index = random.randrange(length)

    return name_list[index]['name']


def _get_weighted_random_name(name_list):
    name_list = sorted(
        name_list,
        key=operator.itemgetter('weight'),
        reverse=True,
    )

    total_weight = sum(entry['weight'] for entry in name_list)
    random_weight = random.randrange(total_weight + 1)

    for entry in name_list:
        random_weight -= entry['weight']
        if random_weight <= 0:
            return entry['name']


def _strip_diacritics(string):
    return (
        unicodedata.normalize('NFKD', string)
        .encode('ascii', 'ignore')
        .decode('utf-8')
    )


def _snakify_name(name):
    name = _strip_diacritics(name)
    name = name.lower()
    name = name.replace(' ', '-')

    return name


def _format_name(name, surname, snake_case=False):
    if not name or not surname:
        sep = ''
    elif snake_case:
        sep = '_'
    else:
        sep = ' '

    if snake_case:
        name = _snakify_name(name)
        surname = _snakify_name(surname)

    disp_name = '{}{}{}'.format(name, sep, surname)

    return disp_name


def _generate_name(get_random_name, names, surnames, part, snake_case):
    name = ''
    surname = ''

    if part == 'first':
        name = get_random_name(names)
    elif part == 'last':
        surname = get_random_name(surnames)
    else:
        name = get_random_name(names)
        surname = get_random_name(surnames)

    return _format_name(name, surname, snake_case=snake_case)


def _run(args):
    names = _get_names(gender=args.gender)
    surnames = _get_surnames()

    if args.weighted:
        get_random_name = _get_weighted_random_name
    else:
        get_random_name = _get_random_name

    endl = '\n'

    if args.no_nl:
        endl = ''
    elif args.print0:
        endl = '\0'

    for _ in range(args.n):
        disp_name = _generate_name(get_random_name, names, surnames, args.part,
                                   args.snake_case)
        print(disp_name, end=endl)


def main():
    args = _parse_args()

    try:
        _run(args)
    except KeyboardInterrupt:
        sys.exit(1)
