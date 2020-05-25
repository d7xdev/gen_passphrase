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

import secrets
import sys
import math

USAGE = "Usage: %s [ -h | --help ] [ NUM_WORDS ]" % sys.argv[0]

CHARSET = "?.*#%0123456789CDFHJKLMNPQRTVWXY"
CHARS_PER_WORD = 4

##------------------------------------------------------------------------------
def parse_args():
    DEFAULT_PASSWORD_LEN = 4

    if len(sys.argv) == 1:
        return DEFAULT_PASSWORD_LEN
    elif len(sys.argv) == 2:
        arg1 = sys.argv[1]
        if arg1 == "-h" or arg1 == "--help":
            print(USAGE)
            sys.exit(0)
        else:
            try:
                num = int(arg1)
                if num > 0:
                    return num
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
def gen_word():
    return "".join(secrets.choice(CHARSET) for x in range(CHARS_PER_WORD))

##------------------------------------------------------------------------------
if __name__ == '__main__':
    num_words = parse_args()

    entropy_per_char = math.log(len(CHARSET))/math.log(2)
    entropy_per_word = entropy_per_char * CHARS_PER_WORD

    pw_entropy = entropy_per_word * num_words
    password = " ".join(gen_word() for x in range(num_words))

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
