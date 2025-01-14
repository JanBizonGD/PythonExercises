#!/usr/bin/python3
# Create a script that reads the access log from a file.
# The name of the file is provided as an argument.
# An output of the script should provide the total number of different User Agents
#  and then provide statistics with the number of requests from each of them

# Search :
# search from closing " and "..." in line - should occure only once in line

# Input : access.log.5

""" Module sys provides argument parsing 
    Module re provides findall and M flag """
import sys
import re

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) <= 0:
        print('Pass at least one argument.')
        exit(1)
    with open(args[0], 'r', encoding="utf-8") as f:
        user_agents = re.findall(r'\" \"(.*?)\"$', f.read(), re.M)
    for unique_agent in set(user_agents):
        print(user_agents.count(unique_agent), ":", unique_agent)
