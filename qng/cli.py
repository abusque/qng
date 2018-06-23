import argparse
import sys

import qng
import qng.generator


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

def _run(args):
    name_generator = qng.generator.QuebNameGenerator()

    if args.no_nl:
        endl = ''
    elif args.print0:
        endl = '\0'
    else:
        endl = '\n'

    for _ in range(args.n):
        disp_name = name_generator.generate(
            gender=args.gender,
            part=args.part,
            snake_case=args.snake_case,
            weighted=args.weighted,
        )
        print(disp_name, end=endl)


def main():
    args = _parse_args()

    try:
        _run(args)
    except KeyboardInterrupt:
        sys.exit(1)
