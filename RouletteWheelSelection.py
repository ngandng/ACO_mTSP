
import random

def roulette_wheel_selection(P):
    r = random.random()
    C = [sum(P[:i + 1]) for i in range(len(P))]

    for j, c in enumerate(C):
        if r <= c:
            return j