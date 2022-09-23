from manim import *
from numpy import array
from common import *
import math


def vinc_str(x):
        ''' Return vinculum representation of negative digits '''
        return "\overline{" + str(abs(int(x))) + "}" if (int(x) < 0) else str(x)

def vinc_list(l):
        ''' Vinculum representation of digit list or string 

            There are two ways this can be used
               a) vinc_list([1, 2, -3, 9, -8])
               b) vinc_list("123'98'")
        '''
        if isinstance(l, str) and "'" in l:
                # String with ' for vinculum
                # We will transform this into a list of digits
                v = []  # This will contain the result
                for l_ in l:
                        # If you see a ', the last digit is negative
                        if l_ == "'":
                                v[-1] = -1 * v[-1]
                        else:
                                # Slurp in next digit
                                v.append(int(l_))
        else:
                v = l   # Directly run vinc_str on elements
        return [vinc_str(x) for x in v]

def MT(snum, color="Yellow"):
    ''' Wrapper - MathTex(*vinc_list(snum)) '''
    el = vinc_list(snum)
    eg = MathTex(*el, color=color)
    return eg

def MTV(snum, color="Yellow"):
    ''' Wrapper - MT + vertical rendering '''
    # syntax {{x}} for MathTex substrings
    # To get than in an f string, we need this
    el = [f'{{{{&{x}}}}}\\\\' for x in vinc_list(snum)]
    eg = MathTex(" ".join(el), color=color)
    return eg

# Generic Division operator
class Divop:
    def __init__(self, scene, dividend, divisor, divisor_xform,
                 dividend_xform=None,
                 subs=[], carries=[], answer=None, ansplaces=0, wait=1):
        '''
        Division operator

        inputs:
           dividend: String/List
           divisor : String/List
           divisor_xform: String/List
           subs: List
           carries: List
           answer: List
           answerplaces: List
           scene   : Manim.Scene
        '''
        self.scene = scene
        if dividend_xform is None:
                dividend_xform = dividend
                self.dividend_xformp = False
        else:
                self.dividend_xformp = True
                
        self.raw = MathTex(dividend, "\divisionsymbol", divisor, color="White")  # Raw divisor
        self.rx  = MT(dividend_xform)
        self.divisor_x = MT(divisor_xform, color='Lime') # Transformed divisor
        self.e_dividend = MT(dividend_xform).arrange(buff=1)  # Dividend
        #self.e_divisor = MTV(divisor_xform, color='Lime').scale(0.6)  # Transformed Divisor, vertical
        self.e_divisor = MT(divisor_xform, color='Lime')  # Transformed Divisor
        #self.vln = Line(self.e_divisor[0], self.e_divisor[-1])  # Vertical Line
        self.vln = Text("|")
        # Setup future subparts
        self.subs = subs
        self.answer  = MT(answer)
        self.carries = carries
        self.ansplaces = ansplaces

    def clear(self):
            self.scene.remove(self.g1, self.gc)
            
    def step_all(self, wait=3):
            ''' Run all steps '''
            for i in range(len(self.answer)+1):
                    self.step(i)
            self.scene.wait(wait)
                    
    def step(self, n=0, wait=1):
        ''' Single step (nth)
        
            n: integer
            
            The zeroth step shows the dividend and divisor
            The n(>0) th step shows the nth answer digit,
              the associated carry and associated flag carries 
        '''
            
        def _realign():   # Update alignments after redisplay
                gc.arrange(RIGHT, buff=1)
                ga.arrange(RIGHT, buff=1)
                g2.arrange(DOWN, aligned_edge=LEFT)
                g1.arrange(RIGHT, aligned_edge=UP)
                # We do this instead of prepending gc to g2
                # to keep the divisor and vline alignment right
                gc.next_to(g2, UP, aligned_edge=LEFT)
                
                
        scene = self.scene
        if n==0:
                # Display raw division statement
                scene.add(self.raw)
                scene.wait(1)

                # Transform division sign and divisor
                _t = Text("..").move_to(self.raw[1])
                self.divisor_x.move_to(self.raw[2])
                self.raw[1].become(_t)
                scene.play(Transform(self.raw[2], self.divisor_x))
                scene.wait(1)
                if self.dividend_xformp:
                        self.rx.move_to(self.raw[0])
                        scene.play(Transform(self.raw[0], self.rx))
                        scene.wait(1)
                        
                # Remove transformed division sign
                scene.remove(self.raw[1])

                # Set up division operation
                ga = VGroup()  # Dummy group for answers
                gc = VGroup(MT("0", color="Black"))  # Dummy zeroth carry
                g2 = VGroup(self.e_dividend)  # Setup group for later filling
                # Top group that will contain all elements
                g1 = VGroup(self.e_divisor, self.vln, g2).arrange(RIGHT, aligned_edge=UP)
                g1.arrange(RIGHT, aligned_edge=UP)

                # Transform dividend and divisor display. This shows only
                # The dividend and transformed divisor as we want to see them
                scene.play(ReplacementTransform(self.raw[2], self.e_divisor))
                scene.play(ReplacementTransform(self.raw[0], self.e_dividend))
                scene.wait(1)

                # Add rest of division operation to scene
                scene.add(g1, gc)
                self.hln = Line(self.e_dividend[0].get_left(), self.e_dividend[-1].get_right())
                g2 += self.hln
                g2 += ga
                _realign()
                scene.wait(wait)
                self.g1 = g1
                self.g2 = g2
                self.gc = gc
                self.ga = ga
        else:
                ga = self.ga
                gc=self.gc
                g2 = self.g2
                g1 = self.g1

                # First, show the next answer bit
                ga += self.answer[n-1]
                if n > self.ansplaces:
                        self.answer[n-1].set_color(RED)
                else:
                        self.answer[n-1].set_color(GREEN_C)
                _realign()
                self.scene.wait(1)

                # Next, show the next carry
                # Only nonzero carries are visible
                if n <= len(self.carries):
                        c = self.carries[n-1]
                        _col = "Grey" if int(c) else "Black"
                        gc += MT(c, color=_col)
                        _realign()
                        if int(c):
                                self.scene.wait(1)

                
                # Show the next flag carries
                if n <= len(self.subs):
                        self.scene.play(Indicate(self.answer[n-1]))
                        self.scene.play(Indicate(self.e_divisor))
                        scene.wait(0.5)
                        g2 -= self.ga
                        g2 -= self.hln
                        s = self.subs[n-1]
                        # Prepend dots so we align to the
                        # correct divisor digit
                        s_ = MT("0"*n + s, color='White').arrange(buff=1)
                        # Set the prepended digits color to black to hide it
                        # FIXME: find a more elegant solution
                        s_[0:n].set_color(BLACK)
                        g2 += s_
                        g2 += self.hln
                        g2 += self.ga
                        _realign()
                        self.scene.wait(wait)
                
                
                
class NikhikamDivison(Scene):
    def construct(self):
            # 2112 / 88
            # DC = 12
            # Subs = 24, 36
            # q = 23, r=88
            d = Divop(self, "2112", "88", "12",
                      subs = ["24", "36"],
                      carries = "00",
                      answer = "2388",
                      ansplaces = 2)
            d.step_all(wait=3)
            d.clear()
            self.next_section()
            # 1901 / 87 = 21'01 / 87
            # DC = 13
            # Subs = 26, 13
            # q = 21, r=74
            d = Divop(self, 1901, "87", NComp(87),
                      dividend_xform="21'01", 
                      subs = ["26", "13"],
                      carries = "00",
                      answer = "2174",
                      ansplaces = 2)
            d.step_all(wait=3)
            d.clear()
            self.next_section()

            # 7873 / 81 = 12'1'3'3 / 81
            # DC = 19 = 21'
            # Subs = 21', 00, 4'2
            # q = 21, r=74
            d = Divop(self, 7873, "81","21'",
                      dividend_xform="12'1'3'3", 
                      subs = ["21'", "00", "4'2"],
                      carries = "00",
                      answer = "102'7'5",
                      ansplaces = 3)
            d.step_all(wait=3)
            d.clear()
            self.next_section()
       
