#!/usr/bin/python3
# Given a list of integers. 
# Remove duplicates from the list and create a tuple. 
# Find the minimum and maximum number.

# TO DO : input verfication
#import pyinputplus as pyip
import sys


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) <= 0:
        print('Pass at least one argument.')
        exit(1)
    unique_args = tuple(set(args))
    print('min:', min(unique_args))
    print('max:', max(unique_args))
