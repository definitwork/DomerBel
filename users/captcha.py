import random


def random_digit_challenge():
    captha = u''
    for i in range(3):
        captha += str(random.randint(0, 9))

    return captha, captha
