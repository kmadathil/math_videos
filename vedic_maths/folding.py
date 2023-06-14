from manim import *
from manim.camera.camera import Camera
from numpy import array
from common import *
from division import vinc_int, vinc_str, vinc_list, MT
import math

class FoldingOp:
    def __init__(self, scene, num, divisor, fold_gen=19, fold_multiplier = 2) -> None:
        self.scene = scene
        self.num = num
        self.fold_t = num
        self.e_num = MT(num, color="Yellow")
        self.fold_gen = fold_gen
        self.og = MT(fold_gen, color="Yellow")
        self.multiplier = vinc_int(fold_multiplier)
        self.e_mult = MathTex(fold_multiplier, color="Yellow")
        self.divisor = divisor
        self.e_divisor = MT(divisor, color="Yellow")
        self.div_fact = int(fold_gen/divisor)
        self.n_folds = 0

    def idisplay(self, wait = 1):
        ''' Initial display of folding '''
        t00=MarkupText(f"Is {Span(self.num, color='yellow')} divisible by {Span(self.divisor, color='yellow')} ?")
        self.scene.add(t00)
        self.scene.wait(1)
        t01= MarkupText(f"We note that {self.divisor} x {self.div_fact} = {self.fold_gen}")
        t01.next_to(t00, DOWN, buff=1)
        self.scene.add(t01)
        self.scene.wait(wait)
        g0 = VGroup(Text("Folding Generator = ").scale(0.7), self.og).arrange(RIGHT)
        t1 = Text(f"Folding Multiplier = ").scale(0.7)
        gm = VGroup(t1, self.e_mult).arrange(RIGHT)
        gd = VGroup(g0, gm).arrange(DOWN)
        t2 = Text("Fold: ").scale(0.7)
        gn = VGroup(t2, self.e_num).arrange(RIGHT)
        gt = VGroup(gn, gd).arrange(DOWN, buff=1)
        self.scene.play(ReplacementTransform(t00,gn))
        self.scene.play(t01.animate.become(g0))
        self.scene.play(FadeIn(gm, shift=DOWN))
        self.scene.wait(wait)
        self.scene.play(FadeOut(t01))
        self.scene.play(gm.animate.shift(DOWN))
        self.scene.play(gn.animate.arrange(DOWN).shift(UP))
        self.scene.wait(wait)
        self.g0 = gn
        self.g1 = gm
        return gn, gm
    
    def fold(self, wait=2):
        ''' One folding step '''
        nd = (self.fold_t % 10)* self.multiplier
        self.fold_t = int(self.fold_t/10) + nd
        o = Text("+")
        tl = [x for x in str(self.fold_t)]
        t = MathTex(*tl, color="Yellow")
        ndm = MathTex(nd)
        self.scene.play(self.g0[1][-1].animate.next_to(self.g0[1][-2], DOWN))
        t.next_to(self.g0[1][-1], DOWN, aligned_edge=RIGHT)
        o.next_to(self.g0[1][-2], RIGHT)
        ndm.next_to(t, UP, aligned_edge=RIGHT)
        self.scene.play(Indicate(self.g0[1][-1]))   
        self.scene.play(Indicate(self.g1[-1]))
        self.scene.play(Transform(self.g0[1][-1], ndm))
        self.scene.add(t, o)
        self.scene.wait(2)
        self.scene.remove(self.g0[1][-1], o)
        self.g0[1].become(t)
        self.scene.play(self.g0.animate.arrange(DOWN).shift(UP))
        self.scene.remove(t)
        self.scene.wait(wait)
        self.n_folds += 1

    def clear(self):
        self.scene.remove(self.g0, self.g1)

    def end(self):
        assert (((self.fold_t % self.divisor) == 0) == ((self.num % self.divisor) == 0))
        if self.n_folds == (self.divisor - 1):
            assert ((self.fold_t % self.divisor) == (self.num % self.divisor))
        self.scene.remove(self.g1)
        dp = Span("divisible by", color="Green") if (self.fold_t % self.divisor) == 0 else Span("not divisible by", color="Red")
        t = f"{Span(self.fold_t, color='Yellow')} is {dp} {Span(self.divisor, color='Yellow')}, and therefore so is {Span(self.num, color='Yellow')}"
        g = DisplayText(self.scene, t, scale=0.7, move=(2, 0), wait=3, fade=True)
        self.scene.remove(self.g0)

class FoldingTest(Scene):
    def construct(self):
        n = 533
        d = 13
        f = FoldingOp(self, n, d, d*3, 4)
        t0, t1 = f.idisplay(3)
        f.fold()
        f.fold()
        f.end()
        n = 948
        d = 7
        f = FoldingOp(self, n, d, d*3, -2)
        t0, t1 = f.idisplay(3)
        f.fold()    
        f.fold()    
        f.end()
        self.next_section()


class Reciprocal():
    ''' Class for Reciprocal calculation'''
    def __init__(self, scene, numerator, denominator, multiplier = None) -> None:
        self.scene = scene
        assert numerator<10
        self.numerator = numerator
        self.denominator = denominator
        if multiplier is None:
            multiplier = int((denominator+1)/10)
        self.multiplier = multiplier
    def display(self):
        '''Initial display'''
        frac = MathTex("\\frac{"+str(self.numerator)+"}{"+str(self.denominator)+"}", color="Yellow")
        e = Text(" = ")
        z = MathTex("0.", color="Yellow")
        t = Text("...")
        n = MathTex(str(self.numerator), color="Yellow")
        ng = VGroup(n).arrange(LEFT)
        self.tg = VGroup(frac, e, z, t, ng).arrange(RIGHT)
        self.mg = VGroup(Text("Multiplier:").scale(0.6), MathTex(self.multiplier, color="Yellow")).arrange(RIGHT)
        self.mg.next_to(self.tg, RIGHT, buff=1)
        self.scene.play(FadeIn(self.tg))
        self.scene.play(FadeIn(self.mg))
        return self.tg, self.mg
    
    def step(self):
        '''Single Step'''
        return None

class ReciprocalTest(Scene):
    def construct(self):
        r = Reciprocal(self, 1, 19, 2)
        r.display()
        self.wait(3)
        self.next_section()