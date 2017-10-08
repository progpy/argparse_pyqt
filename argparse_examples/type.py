import argparse


def main(args):
    print(args)


def parse_args():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', type=int, default=0)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args)
