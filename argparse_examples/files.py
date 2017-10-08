import argparse
import sys


def main(args):
    print(args.infile)
    print(args.outfile)
    for line in args.infile:
        args.outfile.write(line)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args)
