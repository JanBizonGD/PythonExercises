#!/usr/bin/python3
# Given a list of integers. 
# Remove duplicates from the list and create a tuple. 
# Find the minimum and maximum number.

# Input : Everything that can be casted to float
# Example: min_max.py 1 100 a ldkfj 84a
# on last 3 - it is not possible to cast to float


import sys


if __name__ == '__main__':
    args = []
    for arg in sys.argv[1:]:
        try:
            args.append(float(arg))
        except ValueError as err:
            print(err.args[0])
        
    
    if len(args) <= 0:
        print('Pass at least one valid argument.')
        exit(1)
    
    unique_args = tuple(set(args))
    print('min:', min(unique_args))
    print('max:', max(unique_args))
