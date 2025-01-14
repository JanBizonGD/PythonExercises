#!/usr/bin/python3
# Create a script that accepts the file name and puts its extension to output.
#   If there is no extension - an exception should be raised.

# Input : Any filename - no dots on folders names

""" Module sys provides argument parsing """
import sys
from os.path import splitext

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) <= 0:
        print('Pass at least one argument.')
        exit(1)

    for arg in args:
        try:
            ext = splitext(arg)[1]
            if ext == '' or ext == '.':
                raise ValueError(arg)
            print(f'Extention: {ext}')
        except ValueError as err:
            print(f'{err.args[0]} has no extention.')
