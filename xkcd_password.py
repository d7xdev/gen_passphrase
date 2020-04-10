#!/usr/bin/env python3

# Source #1: https://docs.python.org/3/library/secrets.html#secrets.choice
# Source #2: https://xkcd.com/936/
# Source #3: https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases

import secrets
import sys
import math

USAGE = "Usage: %s [ -h | --help ] [ NUM_WORDS ]" % sys.argv[0]

##------------------------------------------------------------------------------
def parse_args():
    DEFAULT_WORDLIST = 'dict/eff_short_wordlist_2_0.txt'
    DEFAULT_PASSWORD_LEN = 4

    if len(sys.argv) == 1:
        return DEFAULT_WORDLIST, DEFAULT_PASSWORD_LEN
    elif len(sys.argv) == 2:
        arg1 = sys.argv[1]
        if arg1 == "-h" or arg1 == "--help":
            print(USAGE)
            sys.exit(0)
        else:
            try:
                num = int(arg1)
                if num > 0:
                    return DEFAULT_WORDLIST, num
                else:
                    sys.stderr.write("ERROR: '%s' is not greater than zero\n" % arg1)
                    sys.exit(1)
            except ValueError:
                sys.stderr.write("ERROR: '%s' is not an integer\n" % arg1)
                sys.exit(1)
    else:
        sys.stderr.write(USAGE)
        sys.exit(1)

##------------------------------------------------------------------------------
def load(path):
    with open(path) as f:
        words = [line.strip().split()[1] for line in f]
    return words

##------------------------------------------------------------------------------
def validate(words):
    from collections import Counter
    wc = Counter(words)
    if len(words) != len(wc):
        duped = []
        for word, count in wc.items():
            if count > 1: duped.append(word)
        sys.stderr.write("ERROR: duped word detected: %s\n" % ', '.join(duped))
        sys.exit(1)

##------------------------------------------------------------------------------
if __name__ == '__main__':
    wordlist, pw_len = parse_args()
    words = load(wordlist)
    validate(words)

    entropy     = math.log(len(words))/math.log(2)
    pw_entropy  = pw_len * entropy
    password    = ' '.join(secrets.choice(words) for i in range(pw_len))

    print('''
Dictionary  : %s
Dict Len    : %10d (word)
Entropy     : %10.2f (bit/word)
Pw Len      : %10d (word)
Pw Entropy  : %10.2f (bit)
Password    : %s
''' % (wordlist, len(words), entropy, pw_len, pw_entropy, password))
