#!/usr/bin/python3
# Given an input string, count occurrences of all characters within a string

# sys.argv - always string
# Input : Enything 

import sys

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) <= 0:
        print('Pass at least one argument.')
        exit(1)
    
    for arg in args:
        print(arg)
        unique_letters = set(arg)
        letter_count = { (letter, arg.count(letter)) for letter in unique_letters }
        for letter, count in letter_count:
            print(letter, ":", count)