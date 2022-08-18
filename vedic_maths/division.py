from manim import *
from numpy import array
from common import *
import math


def vinc_str(x):
        return "\overline{" + str(abs(int(x))) + "}" if (int(x) < 0) else str(x)

def MT(snum, color="Yellow"):
    el = [x for x in snum]
    eg = MathTex(*el, color=color)
    return eg

def MTV(snum, color="Yellow"):
    el = [f'{x}////' for x in snum]
    eg = MathTex(*el, color=color)
    return eg

# Division operator
class Divop:
    def __init__(self, dividend, divisor, scene):
        self.scene = scene
        self.e_dividend = MT(dividend)
        self.e_divisor = MTV(divisor)
        self.e_divisor.next_to(self.e_dividend, LEFT, aligned_edge=UP)
        scene.add(self.e_dividend)
        scene.add(self.e_divisor)
        scene.wait()

class DivisionTest(Scene):

    def construct(self):
        d = Divop("5678", "123", self)
