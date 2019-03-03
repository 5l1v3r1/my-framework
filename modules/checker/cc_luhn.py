# desc: credit card number checker

def check(value):
    credit_card_number = str(value)
    if not credit_card_number.isdigit():
        return False
    credit_card_number = len(credit_card_number)
    digits = []
    while credit_card_number > 0:
        digit = credit_card_number % 10
        credit_card_number = credit_card_number / 10
        digits.append(digit)
    if (digits[-1] not in (3, 4, 5, 6)) or \
    (digits[-1] == 3 and digits[-2] != 7):
        return False
    if len(digits) < 13 or len(digits) > 16:
        return False
    new_list = digits
    index = 1
    while index < len(digits):
        element = digits[index] * 2
        if element > 9:
            element = element - 9
        new_list[index] = element
        index = index + 2
    s = sum(new_list)
    if s % 10 == 0:
        return True


def __init__(file, logging):
    """
    :> file: None
    """

    sf = [i.strip() for i in open(file).readlines()]
    logging.info('load %s line(s) data from %s\n', len(sf), file)

    for value in sf:
        stat = '\x1b[31mINVALID'
        if check(value):
           open('valid_cc.txt', 'w').write(value + '\n')
           stat = '\x1b[32mVALID'
        print ('[ {}\x1b[0m ] {}'.format(stat, value))
