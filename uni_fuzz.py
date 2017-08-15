#!/usr/bin/env python2

import random

from unicodedata import bidirectional
from optparse import OptionParser

TYPE_TABLE = """
The following is a table of acceptable unicode --types.
| L   | Left_To_Right           | any strong left-to-right character
| LRE | Left_To_Right_Embedding | U+202A: the LR embedding control
| LRO | Left_To_Right_Override  | U+202D: the LR override control
| R   | Right_To_Left           | any strong right-to-left (non-Arabic-type) character
| AL  | Arabic_Letter           | any strong right-to-left (Arabic-type) character
| RLE | Right_To_Left_Embedding | U+202B: the RL embedding control
| RLO | Right_To_Left_Override  | U+202E: the RL override control
| PDF | Pop_Directional_Format  | U+202C: terminates an embedding or override control
| EN  | European_Number         | any ASCII digit or Eastern Arabic-Indic digit
| ES  | European_Separator      | plus and minus signs
| ET  | European_Terminator     | a terminator in a numeric format context, includes currency signs
| AN  | Arabic_Number           | any Arabic-Indic digit
| CS  | Common_Separator        | commas, colons, and slashes
| NSM | Nonspacing_Mark         | any nonspacing mark
| BN  | Boundary_Neutral        | most format characters, control codes, or noncharacters
| B   | Paragraph_Separator     | various newline characters
| S   | Segment_Separator       | various segment-related control codes
| WS  | White_Space             | spaces
| ON  | Other_Neutral           | most other symbols and punctuation marks
| UNK | Unknown                 | no response from unicodedata.bidirectional()
"""

unicode_dict = {}

def get_lines(file_name):
    """Return list of lines from a given file.
    Format for file should be:
    lower_range upper_range #comment
    """
    fd    = open(file_name, 'r')
    lines = fd.readlines()
    fd.close()

    return lines

def categorize(lower, upper):
    """Place each character in the range of lower,upper into unicode_dict
    based on the directionality of the character.
    """
    global unicode_dict
    for x in xrange(lower, upper):
        bidi = bidirectional(unichr(x))
        if len(bidi) == 0:
            bidi = "UNK"
        if bidi in unicode_dict.keys():
            unicode_dict[bidi].append(unichr(x))
        else:
            unicode_dict[bidi] = [unichr(x)]

def parse_ranges(file_name):
    """Grab the lines from the given file_name. Populate unicode_dict based on
    the bidi characteristic of each char in the given ranges"""
    lines = get_lines(file_name)

    for line in lines:
        tmp   = line.split(' ')
        lower = int(tmp[0], 16)
        upper = int(tmp[1], 16)
        categorize(lower, upper)

def generate_random_unicode(length, types):
    data = u""
    for x in xrange(0, length):
        bidi_type = random.choice(types)
        data      = data + random.choice(unicode_dict[bidi_type])
    return data

def split_callback(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))

def main():
    from sys import exit
    acceptable_types = ["L", "LRE", "LRO", "R", "AL", "RLE", "RLO", "PDF", "EN", "ES", "ET", "AN",
                        "CS", "NSM", "BN", "B", "WS", "ON", "UNK"]

    usage = "usage: %prog [options] length\n" + TYPE_TABLE
    parser = OptionParser(usage=usage)
    parser.add_option("-t", "--types", action="callback", type="string", 
                      help="See above table. Default all types.", callback=split_callback)

    (opts, args) = parser.parse_args()

    # Default length 50. Otherwise args[0]
    try:
        length = int(args[0])
    except (IndexError, ValueError):
        length = 50

    if opts.types:
        types = list(set(acceptable_types) & set(opts.types))
    else:
        types = acceptable_types

    parse_ranges('unicode_ranges.txt')

    print(generate_random_unicode(length, types))


if __name__=='__main__':
    main()
