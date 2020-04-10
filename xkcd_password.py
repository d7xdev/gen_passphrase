#!/usr/bin/env python3

# Source #1: https://docs.python.org/3/library/secrets.html#secrets.choice
# Source #2: https://xkcd.com/936/
# Source #3: https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases

import secrets
import sys
import math

WORDLIST='dict/eff_short_wordlist_2_0.txt'
PW_LEN=4

with open(WORDLIST) as f:
    words = [line.strip().split()[1] for line in f]

## sanity check to make sure words are unique
from collections import Counter
wc = Counter(words)
if len(words) != len(wc):
    sys.stderr.write(WORDLIST+": ERROR: duped word detected!\n")
    sys.exit(1)

entropy     = math.log(len(words))/math.log(2)
pw_entropy  = PW_LEN * entropy
password    = ' '.join(secrets.choice(words) for i in range(PW_LEN))

print('''
Dictionary  : %s
Dict Len    : %10d (word)
Entropy     : %10.2f (bit/word)
Pw Len      : %10d (word)
Pw Entropy  : %10.2f (bit)
Password    : %s
''' % (WORDLIST, len(words), entropy, PW_LEN, pw_entropy, password))
