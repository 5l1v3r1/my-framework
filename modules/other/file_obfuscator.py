from collections import OrderedDict
from pprint import pformat

# desc: change string to emoji
# author: Chris Rands

try:
    range = xrange
except NameError:
    pass  # Python 3

EMOTICONS = [':-)', '=-O', ':-!', ':-D', ':\'(', ':-\\', 'O:-)', ':-[', ':-P', ';-)']
# TODO: Add other alphabets as options including real emojis
MAX_STR_LEN = 70


def chunk_string(in_s, n):
    """Chunk string to max length of n"""
    return '\n'.join('{}\\'.format(in_s[i:i+n]) for i in range(0, len(in_s), n)).rstrip('\\')


def encode_string(in_s, alphabet):
    """Convert input string to encoded output string with the given alphabet"""
    # Using OrderedDict to guarantee output order is the same
    # Note Python 2 and 3 inputs differ slightly due to pformat()
    d1 = OrderedDict(enumerate(alphabet))
    d2 = OrderedDict((v, k) for k, v in d1.items())
    return ('from collections import OrderedDict\n'
            'exec("".join(map(chr,[int("".join(str({}[i]) for i in x.split())) for x in\n'
            '"{}"\n.split("  ")])))\n'.format(pformat(d2), chunk_string('  '.join(
            ' '.join(d1[int(i)] for i in str(ord(c))) for c in in_s), MAX_STR_LEN)))


def main(in_file, out_file):
    """Read input and write output file"""
    with open(in_file) as in_f, open(out_file, 'w') as out_f:
        # This assumes it's ok to read the entire input file into memory
        out_f.write(encode_string(in_f.read(), EMOTICONS))

def __zvm__(input, output, logging):
    """
    :> output: out.py
    """
    main(input, output)
    logging.info(f'saved as {output}')
