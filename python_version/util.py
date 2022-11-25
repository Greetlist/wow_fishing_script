import random

def roll_for_ratio(ratio):
    if ratio >= 1:
        return True
    cur_rand = random.randint(1, 100)
    if cur_rand / 100.00 <= ratio:
        return True
    return False