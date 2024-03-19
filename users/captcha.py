import random


def random_digit_challenge():
    captcha = u''
    for i in range(3):
        captcha += str(random.randint(0, 9))
    return captcha, captcha