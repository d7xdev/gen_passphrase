#!/usr/bin/env python3

# This password generator is inspired by NES Snake's Revenge (SR) video game.
# The video game was published in 1990 by Ultra Software Corporation,
# a shell company for Konami of America.
#
# Compared to other confusing NES passwords of the time, SR passwords are
# very user friendly to write on paper. Nevertheless, the system has
# few error-prone characters: single symbol `!!` and two symbols `!`,
# `!` and `1`, `2` and `Z`, `6` and `G`, `3` and `8` and `B`.
#
# The original SR password charset contains 35 symbols.
# 
#   !! !  ?  .  '  #  %
#   0  1  2  3  4  5  6  7  8  9
#   B  D  G  H  J  K  L  M  N  P
#   Q  R  T  V  W  X  Y  Z 
#
# The password charset has been modified to be more visually distinct when
# written on paper. It contains 32 symbols. The quote symbol `'` has been
# replaced with the star `*` symbol. While there is no standard way for drawing
# a star on paper, the `*` symbol is easily recognizable from old telephone.
# Also, the quote/apostrophe (U+0027) symbol was often mistaken with the
# back-quote/grave accent (U+0060) symbol. Exclamation symbols `!!` and `!` and
# symbol `Z` were removed to reduce transcription error. Symbols `B` and `G`
# are shifted to symbols `C` and `F` respectively for similar reason.
#
#   ?  .  *  #  %
#   0  1  2  3  4  5  6  7  8  9  
#   C  D  F  H  J  K  L  M  N  P
#   Q  R  T  V  W  X  Y
#
# A password of 16 symbols would provides 80 bits entropy, and can be
# conveniently written as four groups of four characters on a post-it note.
#
#   >>> math.log(32**16)/math.log(2)
#   80.0
#

import argparse
import secrets
import sys
import math

CHARSET = "?.*#%0123456789CDFHJKLMNPQRTVWXY"
CHARS_PER_WORD = 4

##------------------------------------------------------------------------------
def _strict_positive_int(value):
    try:
        ivalue = int(value)
        if ivalue <= 0: raise ValueError
    except ValueError:
        raise argparse.ArgumentTypeError("invalid strict positive int value: '%s'" % value)
    return ivalue

def parse_args():
    DEFAULT_PASSWORD_LEN = 4
    parser = argparse.ArgumentParser(description="""
A password generator inspired by NES Snake's Revenge video game
""")
    parser.add_argument("NUM_WORDS", type=_strict_positive_int, nargs='?',
                        default=DEFAULT_PASSWORD_LEN,
                        help="number of words to generate (default: %s)" % DEFAULT_PASSWORD_LEN)
    parser.add_argument("-b", "--brief", action="store_true",
                        help="do not output password metric")
    return parser.parse_args()

##------------------------------------------------------------------------------
def gen_word():
    return "".join(secrets.choice(CHARSET) for x in range(CHARS_PER_WORD))

##------------------------------------------------------------------------------
if __name__ == '__main__':
    args = parse_args()
    num_words = args.NUM_WORDS

    entropy_per_char = math.log(len(CHARSET))/math.log(2)
    entropy_per_word = entropy_per_char * CHARS_PER_WORD

    pw_entropy = entropy_per_word * num_words
    password = " ".join(gen_word() for x in range(num_words))

    if args.brief:
        print(password)
    else:
        print('''
Charset     : %s
            : %10d (char)
Entropy     : %10.2f (bit/char)
            : %10.2f (bit/word)
Pw Len      : %10d (word)
            : %10d (char)
Pw Entropy  : %10.2f (bit)
Password    : %s
''' % (CHARSET, len(CHARSET),
       entropy_per_char, entropy_per_word,
       num_words, len(password),
       pw_entropy,
       password))
