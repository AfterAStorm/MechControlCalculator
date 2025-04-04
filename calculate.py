
from typing import Tuple

from math import sin, cos, pi
from time import time

from solver import findKnee

class Calculator:
    def __init__(self) -> None:
        pass

    def solve(self, delta) -> Tuple[float, float, float]:
        return (sin(time() + 2 * delta * pi) / 2, findKnee(1, 1, pi / 2), 0)