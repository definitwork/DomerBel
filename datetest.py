# from datetime import datetime, timedelta
#
# print((datetime.now() - timedelta(days=50)) > (datetime.now() - timedelta(days=51)))
import time


def fn(x):
    def wrapper(*args):
        t1 = time.time()
        x(*args)
        t2 = time.time()
        return t2-t1
    return wrapper

@fn
def fb(a,b,c):
    b.sort()
    return sum(b[-c:])



print(fb(8, [5, 13, 8, 4, 4, 15, 1, 9], 8))
print(fb(11, [14, 8, 15, 19, 2, 21, 13, 21, 12, 10, 8], 5))
print(fb(15, [19, 20, 5, 10, 2, 20, 7, 9, 1, 3, 13, 14, 3, 3, 4], 1))
print(fb(12, [22, 7, 24, 24, 11, 22, 24, 3, 9, 16, 2, 19], 7))
print(fb(7, [10, 3, 21, 23, 6, 3, 8], 4))