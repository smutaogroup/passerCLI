# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import sys
from passer import Passer

def parse_args():
    parser = ArgumentParser(description='PASSer CLI')
    parser.add_argument('-i', '--id', required=False, \
        help='PDB ID')
    parser.add_argument('-f', '--file', required=False, \
        help='PDB file')
    parser.add_argument('-c', '--chain', required=False, \
        help='chain ID')
    parser.add_argument('-s', '--save', required=False, \
        help='save FPocket results (y/n)')
    args = parser.parse_args()
    return args


def main(args):
    if not (args.id or args.file):
        raise ValueError("One input is required!")
    if args.id and args.file:
        raise ValueError("Please specify only one input!")
    model = Passer(args.id, args.file, args.chain, args.save)
    model.predict()


def entry_point():
    args = parse_args()
    main(args)


if __name__ == '__main__':
    entry_point()
