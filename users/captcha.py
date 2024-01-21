import random


def random_digit_challenge():
    # russian_alphabet = ''.join([chr(1040 + i) + chr(1072 + i) for i in range(32)])
    captha = u''
    for i in range(3):
        # captha += russian_alphabet[random.randint(0,64)]
        captha += str(random.randint(0, 9))
    print(captha)
    return captha, captha
