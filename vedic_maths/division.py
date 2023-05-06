
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
        if isinstance(l, int):
                v = str(l)
        elif isinstance(l, str) and "'" in l:
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

def vinc_int(l):
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
                i = 0
                for _v in v:
                    i = i*10+_v
                return i
        else:
                v = int(l)   
                return v

def MT(snum, color="Yellow"):
    ''' Wrapper - MathTex(*vinc_list(snum)) '''
    el = vinc_list(snum)
    eg = MathTex(*el, color=color)
    return eg

def MTV(snum, color="Yellow"):
    ''' Wrapper - MT + vertical rendering '''
    # syntax {{x}} for MathTex substrings
    # To get than in an f string, we need this
    el = [f'{{{{&{x}}}}}\\\\' for x in reversed(vinc_list(snum))]
    eg = MathTex(" ".join(el), color=color)
    return eg

# Generic Division operator
class Divop:
    def __init__(self, scene, dividend, divisor, divisor_xform,
                 dividend_xform=None, divisor_xform2 = None,
                 subs=[], carries=[], answer=None, ansplaces=0,
                 vertical = False, nikhilam=False,
                 backtrackp = False, backtrack_en=[],
                 backtrack_subs=[], backtrack_carries=[], backtrack_answer=None,
                 backtrack_next_answer=None,
                 wait=2):
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
        self.e_dividend = MT(dividend_xform).arrange(buff=1)  # Dividend

        if divisor_xform2 is not None:
                self.divisor_x2 = MT(divisor_xform2, color='Lime') # Transformed divisor
                self.divisor_x = MT(divisor_xform)
                self.divisor_x2p = True
        else:
                self.divisor_x = MT(divisor_xform, color='Lime') # Transformed divisor
                self.divisor_x2p = False
        self.scene.wait(1)

        self.is_vertical = False
        if vertical:
                self.is_vertical = True
                if divisor_xform2 is None:
                    self.e_divisor = MTV(divisor_xform, color='Lime')  # Transformed Divisor, vertical
                else:
                    self.e_divisor = MTV(divisor_xform2, color='Lime')  # Transformed Divisor, vertical

                if not nikhilam:
                       self.e_divisor[-2].set_color(YELLOW)
                self.vln = Line(self.e_divisor[0], self.e_divisor[-1])  # Vertical Line
        else:
                if divisor_xform2 is None:
                    self.e_divisor = MT(divisor_xform, color='Lime')  # Transformed Divisor
                else:
                    self.e_divisor = MT(divisor_xform2, color='Lime')  # Transformed Divisor
                if not nikhilam:
                       self.e_divisor[0].set_color(YELLOW)
                self.vln = Text("|")

        self.flag = not nikhilam

        # Setup future subparts
        self.subs = subs
        if isinstance(answer, list):
                a_ = [MT(a) for a in answer]
                self.answer = VGroup(*a_)
        else:
                self.answer  = MT(answer)

        self.carries = carries
        self.ansplaces = ansplaces

        self.backtrackp = backtrackp
        self.backtrack_subs = backtrack_subs
        if backtrack_answer is not None:
                if isinstance(backtrack_answer, list):
                        a_ = [MT(a) for a in backtrack_answer]
                        self.backtrack_answer = VGroup(*a_)
                else:
                        self.backtrack_answer  = MT(backtrack_answer)
        if backtrack_next_answer is not None:
                if isinstance(backtrack_next_answer, list):
                        a_ = [MT(a) for a in backtrack_next_answer]
                        self.backtrack_next_answer = VGroup(*a_)
                else:
                        self.backtrack_next_answer  = MT(backtrack_next_answer)
        self.backtrack_carries = backtrack_carries
        self.backtrack_en = backtrack_en
        
    def clear(self):
            self.scene.remove(self.g1, self.gc, self.ga, self.g2, self.vln)
            if self.flag:
                    for e in self.e_divisor:
                            self.scene.remove(e)
            
    def step_all(self, wait=3):
            ''' Run all steps '''
            for i in range(len(self.answer)+1):
                    self.step(i)
            self.scene.wait(wait)
                    
    def step(self, n=0, wait=1, is_backtracking=False):
        ''' Single step (nth)
        
            n: integer
            
            The zeroth step shows the dividend and divisor
            The n(>0) th step shows the nth answer digit,
              the associated carry and associated flag carries 
        '''
            
        def _realign():   # Update alignments after redisplay
                gc.arrange(RIGHT, buff=1)
                ga.arrange(RIGHT, buff=1)
                # Answer pre-alignment
                for i, ax in enumerate(g2[-1]):
                        ax.next_to(g2[0][i], DOWN, aligned_edge=RIGHT)
                g2.arrange(DOWN, aligned_edge=LEFT)
                g1.arrange(RIGHT, aligned_edge=UP)
                if self.is_vertical:
                       self.e_divisor.next_to(self.vln, LEFT, aligned_edge=DOWN)
                # We do this instead of prepending gc to g2
                # to keep the divisor and vline alignment right

                for i, gcx in enumerate(gc):
                        gcx.next_to(g2[0][i], UP, aligned_edge=RIGHT)
                # Loop over subs for horizontal alignment
                 
                for i in range(1, len(g2)-2):
                        for j, fcx in enumerate(g2[i]):
                                # sub alignment wrt previous row
                                fcx.next_to(g2[i-1][j], DOWN, aligned_edge=RIGHT)
                
        scene = self.scene
        if n==0:
                # Display raw division statement
                scene.add(self.raw)
                scene.wait(3)


                # Transform division sign and divisor
                _t = Text("..").move_to(self.raw[1])
                self.divisor_x.move_to(self.raw[2])
                self.raw[1].become(_t)
                scene.play(Transform(self.raw[2], self.divisor_x))
                if self.divisor_x2p:
                        scene.wait(4)
                        self.divisor_x2.move_to(self.raw[2])
                        scene.play(Transform(self.raw[2], self.divisor_x2))
                scene.wait(4)
                if self.dividend_xformp:
                        self.rx.move_to(self.raw[0])
                        scene.play(Transform(self.raw[0], self.rx))
                        scene.wait(5)
                        
                # Remove transformed division sign
                scene.remove(self.raw[1])

                # Set up division operation
                ga = VGroup()  # Dummy group for answers
                gc = VGroup(MT("0", color="Black"))  # Dummy zeroth carry
                g2 = VGroup(self.e_dividend)  # Setup group for later filling
                # Top group that will contain all elements
                g1 = VGroup(self.e_divisor, self.vln, g2).arrange(RIGHT, aligned_edge=UP)
                #g1.arrange(RIGHT, aligned_edge=UP)
                if self.is_vertical:
                       self.e_divisor.next_to(self.vln, LEFT, aligned_edge=DOWN)

                # Transform dividend and divisor display. This shows only
                # The dividend and transformed divisor as we want to see them
                scene.play(ReplacementTransform(self.raw[2], self.e_divisor))
                scene.play(ReplacementTransform(self.raw[0], self.e_dividend))
                scene.wait(5)

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
        elif ((not self.backtrackp) or (not self.backtrack_en[n-1]) or is_backtracking):
                # Normal, or recursive call after backtracking
                ga = self.ga
                gc=self.gc
                g2 = self.g2
                g1 = self.g1

                # First, show the next answer bit
                if is_backtracking:
                        ga[-1].become(self.answer[n-1])
                else:
                        ga += self.answer[n-1]

                if n > self.ansplaces:
                        self.answer[n-1].set_color(RED)
                else:
                        self.answer[n-1].set_color(GREEN)

                _realign()

                self.scene.wait(5)

                # Next, show the next carry
                # Only nonzero carries are visible
                if n <= len(self.carries):
                        c = self.carries[n-1]
                        _col = "Grey" if vinc_int(c) else "Black"
                        ct = MT(c, color=_col)
                        if is_backtracking:
                                gc[-1].become(ct)
                        else:
                                gc += ct
                        _realign()
                        if vinc_int(c):
                                self.scene.wait(5)

                
                # Show the next flag carries / subs
                if n <= len(self.subs):
                        dlen = len(self.e_dividend)
                        self.scene.play(Indicate(ga[-1]))
                        if self.flag:
                                if self.is_vertical:
                                        self.scene.play(Indicate(self.e_divisor[:-2]))

                                else: 
                                        self.scene.play(Indicate(self.e_divisor[1:]))
                        else:
                                self.scene.play(Indicate(self.e_divisor))

                        scene.wait(5)
                        s = self.subs[n-1]
                        s_ = VGroup()
                        # We pad the subs on both sides with invisible 0s
                        # to get the alignment right later
                        for i in range(n):
                                s_ += MT("0", color='Black')
                        if isinstance(s, list):
                                for sx in s:
                                        s_ += MT(sx, color='White')
                        else:
                                st = MT(s, color='White')
                                for sx in st:
                                        s_ += sx
                        for i in range(dlen-len(s_)):
                                s_ += MT("0", color='Black')
                        if is_backtracking:
                                g2[-3].become(s_)
                        else:
                                g2 -= self.ga
                                g2 -= self.hln
                                g2 += s_
                                g2 += self.hln
                                g2 += self.ga
                        _realign()
                        self.scene.wait(wait)
        else:
                # Need backtracking
                ga = self.ga
                gc=self.gc
                g2 = self.g2
                g1 = self.g1

                # First, show the next answer bit, which we will later backtrack
                ga += self.backtrack_answer[n-1]

                if n > self.ansplaces:
                        self.backtrack_answer[n-1].set_color(RED)
                else:
                        self.backtrack_answer[n-1].set_color(GREEN)

                _realign()

                self.scene.wait(5)

                # Next, show the next carry that will be backtracked
                # Only nonzero carries are visible
                if n <= len(self.backtrack_carries):
                        c = self.backtrack_carries[n-1]
                        _col = "Grey" if vinc_int(c) else "Black"
                        c_ = MT(c, color=_col)
                        gc += c_
                        _realign()
                        if vinc_int(c):
                                self.scene.wait(5)

                
                # Show the next backtracking flag carries
                if n <= len(self.backtrack_subs):
                        dlen = len(self.e_dividend)
                        self.scene.play(Indicate(self.backtrack_answer[n-1]))
                        if self.flag:
                                if self.is_vertical:
                                        self.scene.play(Indicate(self.e_divisor[:-2]))
                                else: 
                                        self.scene.play(Indicate(self.e_divisor[1:]))
                        else:
                                self.scene.play(Indicate(self.e_divisor))

                        scene.wait(5)
                        g2 -= self.ga
                        g2 -= self.hln
                        s = self.backtrack_subs[n-1]
                        s_ = VGroup()
                        # We pad the subs on both sides with invisible 0s
                        # to get the alignment right later
                        for i in range(n):
                                s_ += MT("0", color='Black')
                        if isinstance(s, list):
                                for sx in s:
                                        s_ += MT(sx, color='White')
                        else:
                                st = MT(s, color='White')
                                for sx in st:
                                        s_ += sx
                        for i in range(dlen-len(s_)):
                                s_ += MT("0", color='Black')
                        g2 += s_
                        g2 += self.hln
                        g2 += self.ga
                        _realign()
                        self.scene.wait(5)
                        
                # Show the next answer bit, so we can establish the need to backtrack
                ga += self.backtrack_next_answer[n-1]

                self.backtrack_next_answer[n-1].set_color(GREY)
                _realign()
                self.scene.wait(2)
                self.backtrack_answer[n-1].set_color(GREY)
                if n <= len(self.backtrack_carries):
                        c_.set_color(BLACK)
                if n <= len(self.backtrack_subs):
                        s_[n:n+len(s)].set_color(GREY)
                self.scene.wait(4)
                
                # Now we have established the need to backtrack
                ## Remove next answer
                ga -= self.backtrack_next_answer[n-1]
                # Now we recursively call step with backtracking enabled.
                self.step(n, wait=wait, is_backtracking=True)

                
def lastscene(self):
    titleL1 = DisplayText(self,
            Span("Thank you for watching this video.", color="yellow"), scale=0.7, wait=1,
            move=(-2.5, -1), fade=False)
    titleL2 = DisplayText(self,
                Span("Please let us know your feedback by your Likes and Comments.", color="yellow"),
                        scale=0.6, wait=2, move=(-1.5, -1),fade=False)
    titleL2 = DisplayText(self,
            Span("Share the video with your friends too.",
            color="yellow"),scale=0.6,wait=3, move=(-1, -1), fade=False)

    titleL3 = DisplayText(self,
                              Span("Do Subscribe to our Channel and press the Bell Icon!", color="yellow"),
                              scale=0.6, wait=2, move=(0, -1),
                              fade=False)

    self.wait(3)
    self.play(FadeOut(titleL3, titleL2, titleL1))

                
class NikhilamDivision(Scene):
    def construct(self):
            Title(self, "हरणम् ", "Division", move=(3, 5), wait=2)
            self.next_section()
            self.wait(1)

            # Introduction

            text = [
                f"When we <span color='cyan'>divide </span> a <span color='cyan'>Dividend </span> by a <span color='cyan'>Divisor</span>, ",
                f"we <span color='cyan'>subtract/ remove </span> the <span color='cyan'>Divisor </span>from the <span color='cyan'>Dividend.</span>",
                f"But, <span color='cyan'>how many </span> times?",
                f"The answer is the <span color='cyan'>Quotient.</span> ",
                f"And what's left over from subtraction is the <span color='cyan'>Remainder.</span>",
                f"All division processes are merely easy ways of doing",
                f" <span color='cyan'>repeated subtraction fast.</span>"]

            e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

            text = [
                f"For example, <span color='cyan'>256÷8 = 32 </span> with <span color='cyan'>Zero Remainder.</span> ",
                f"From 256, <span color='yellow'>8 </span>can be removed <span color='yellow'>32</span> times.",
                f"And you'll be left with <span color='yellow'>Zero.</span>"]

            e = Explanation(self, text, font="Cambria Math",wait=2, fade=True, aligned_edge=LEFT)

            text = [
                f"Another one, <span color='cyan'>260÷8 = 32 </span> with <span color='cyan'>Remainder=4. </span>",
                f"From 260, <span color='yellow'>8 </span>can be removed <span color='yellow'>32</span> times.",
                f"And you'll be left with <span color='yellow'>4.</span>",
                f"(which is less than <span color='yellow'>8</span>, so you can't remove one more <span color='yellow'>8.</span>)"
                ]

            e = Explanation(self, text, font="Cambria Math",wait=2, fade=True, aligned_edge=LEFT)

            text = [
                f"In <span color='crimson'>Vedic Maths,</span>",
                f"just like <span color='cyan'> Multiplication</span>, for <span color='cyan'> Division </span>also, ",
                f"there are some <span color='cyan'> specific methods </span> that are  <span color='cyan'>best </span> in <span color='cyan'>some cases.</span>",
                f"And there is a <span color='cyan'> general method </span> also.",
                f"To begin with, let's look at the <span color='cyan'>special methods.</span>"]
            e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

            text = [
                f"First one is <span color='red'>Nikhilam </span> method.",
                f"Here, we use the <span color='cyan'>Complement </span> of the <span color='cyan'> Divisor </span> for <span color='cyan'>Division.</span>",
                f"The process is :",
                f"<span color='cyan'>Scale the Complement of the Divisor, </span>",
                f"<span color='cyan'>Shift and add to the Dividend.</span>"
               ]
            e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)


            text = [
                f"<span color='cyan'>Before </span> the actual <span color='cyan'>division process,</span> ",
                f"let's assess the <span color='cyan'>number of digits </span> in the <span color='cyan'> Quotient.</span>",
                f"For example, we want to <span color='cyan'>divide </span> <span color='cyan'> 2031 by 89.</span>",
                f"If we multiply <span color='yellow'>89</span> by <span color='yellow'>10</span>, the result <span color='yellow'>890</span> is less than <span color='yellow'>2031.</span>",
                f"And if we do, <span color='yellow'>89</span> x <span color='yellow'>100 </span>, the result <span color='yellow'>8900 </span> is greater than <span color='yellow'>2031.</span>",
                f"From this, we are sure that the <span color='cyan'>answer </span> is a <span color='yellow'> 2 digit number. </span>"]

            e = Explanation(self, text,font="Cambria Math", wait=2, fade=True, aligned_edge=LEFT)

            self.wait(3)

            text = [
                f"1.Replace the <span color='cyan'>Divisor</span> by its <span color='cyan'> Complement. </span> ",
                f"2.Bring down the <span color='cyan'>1st digit </span> of the <span color='cyan'> Dividend </span> as " ,
                f"  the <span color='cyan'>1st Digit </span> of the <span color='cyan'> Quotient.</span>",
                f"3.<span color='cyan'>Multiply </span> this digit by the <span color='cyan'>Divisor complement </span>digits ",
                f"  and write the product <span color='cyan'>below</span> the succeeding <span color='cyan'>Dividend</span> digits.",
                f"4.To obtain the next  <span color='cyan'> Quotient Digit,</span> ",
                f"  add the <span color='cyan'>product </span>  in <span color='cyan'> step 3 </span> with  <span color='cyan'>Dividend digit.</span>",
                f"5.Repeat until we obtain all the <span color='cyan'>Quotient digits.</span> ",
                f"6.Add the remaining <span color='cyan'>Dividend </span>digits to the digits below them ",
                f" to obtain the <span color='cyan'>Remainder. </span>"]

            e = Explanation(self, text,font="Cambria Math", wait=2, fade=True, aligned_edge=LEFT)

            self.wait(1)

            # 2031 / 89
            # DC = 11
            # Subs = 22, 22
            # q = 22, r=73

            title_h1 = DisplayText(self, Span("Divide 2031 by 89: ", color="Turquoise"),
                                scale=0.6, wait=0, move=(-3.5, -1), fade=False)
            title_h2 = DisplayText(self, Span("By assessment, Number of Quotient digits=2 ", color="pink"),
                                 scale=0.5, wait=0, move=(-3, -1), fade=False)

            self.wait(3)

            d = Divop(self, "2031", "89", "11",
                      subs = ["22", "22"],
                      carries = "00",
                      answer = "2273",
                      nikhilam = True,
                      ansplaces = 2)

            d.step_all(wait=4)

            title1 = DisplayText(self, Span("So Quotient =22 and Remainder=73", color="Turquoise"),
                                 scale=0.5, wait=0, move=(2.5, -1),
                                 fade=False)

            self.wait(3)
            self.play(FadeOut(title1,title_h1,title_h2 ))

            d.clear()
            self.next_section()

            self.wait(2)
            # 2112 / 88
            # DC = 12
            # Subs = 24, 36
            # q = 23, r=88

            title_h1 = DisplayText(self, Span("Divide 2112 by 88: ", color="Turquoise"),
                                   scale=0.6, wait=0, move=(-3.5, -1), fade=False)
            self.wait(1)
            title_h2 = DisplayText(self, Span("By assessment, Number of Quotient digits=2 ", color="pink"),
                                   scale=0.5, wait=0, move=(-3, -1), fade=False)

            self.wait(1)


            d = Divop(self, "2112", "88", "12",
                      subs = ["24", "36"],
                      carries = "00",
                      answer = "2388",
                      nikhilam = True,
                      ansplaces = 2)

            d.step_all(wait=5)



            title1 = DisplayText(self, Span("In this case, remainder=divisor.So, once more we can divide it.", color="Turquoise"), scale=0.5, wait=0, move=(2, -1),
                                fade=False)
            self.wait(3)
            title2 = DisplayText(self, Span("So Quotient becomes 23+1=24 and Remainder=0", color="Turquoise"), scale=0.5, wait=0, move=(2.5, -1),
                                fade=False)

            self.wait(3)
            self.play(FadeOut(title1, title2,title_h1,title_h2))
            d.clear()
            self.next_section()


            text = [
                f"<span color='red'>Nikhilam </span> method is relatively easy when below cases are true:",
                f"<span color='cyan'>Face values </span> of digits in the <span color='cyan'>Divisor Complement </span> are<span color='cyan'> small.</span>",
                f"<span color='cyan'>Face values </span> of digits in the <span color='cyan'>Dividend </span> are <span color='cyan'>small.</span>",
                f"<span color='cyan'>Works best</span> when <span color='cyan'>number of digits</span> in the <span color='cyan'>Quotient</span> is <span color='cyan'>not more than 2.</span>"]

            e = Explanation(self, text, font="Cambria Math", wait=2, fade=True, aligned_edge=LEFT)

            text = [
                f"We can use <span color='cyan'>vinculum numbers </span>" ,
                f"<span color='cyan'>to force some of these conditions </span>if necessary.",
                f"In our next video, we can see such cases too."]

            e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

            """
            
            # 1901 / 87 = 21'01 / 87
            # DC = 13
            # Subs = 26, 13
            # q = 21, r=74
            d = Divop(self, 1901, "87", NComp(87),
                      dividend_xform="21'01", 
                      subs = ["26", "13"],
                      carries = "00",
                      answer = "2174",
                      nikhilam = True,
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
                      nikhilam = True,
                      ansplaces = 3)
            d.step_all(wait=3)
            d.clear()
            self.next_section()
            """


class NikhilamDivisionVinculum(Scene):
    def construct(self):

        Title(self, "हरणम् 2", "Division 2", move=(3, 5), wait=2)
        self.next_section()
        self.wait(1)

        text = [
            f"In the last video, we learned <span color='cyan'>division</span> using <span color='red'>Nikhilam.</span>",
            f"Also, we saw that ",
            f"if the face values of <span color='cyan'>Dividend Digits</span> and " ,
            f"<span color='cyan'>Divisor Complement</span> are <span color='cyan'>small</span>,<span color='red'> Nikhilam Method</span> is really easy.",
            f"So what if these conditions are not met?",
            f"Let's workout some problems."]


        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        text = [
            f"Let's begin with a problem in which the",
            f"<span color='cyan'>face values </span>of <span color='yellow'>some digits </span>in the <span color='cyan'>Dividend </span>are <span color='cyan'>large.</span>",
            f"In this case, we convert the <span color='cyan'>Dividend</span> to its <span color='cyan'>vinculum form</span>",
            f"and continue the division as we did in the last video."]

        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        title_h1 = DisplayText(self,
                               Span("Divide ", color="Turquoise") +
                               Span("1901 ", color="yellow", font="cambria math") +
                               Span("by ", color="Turquoise") +
                               Span("87: ", color="yellow", font="cambria math"),
                               scale=0.6, wait=0, move=(-3.5, -1), fade=False)
        self.wait(1)
        title_h2 = DisplayText(self, Span("By assessment, number of Quotient digits=", color="pink") +
                               Span("2", color="yellow", font="cambria math"),
                               scale=0.5, wait=0, move=(-3, -1), fade=False)
        self.wait(1)


        # 1901 / 87 = 21'01 / 87
        # DC = 13
        # Subs = 26, 13
        # q = 21, r=74
        d = Divop(self, 1901, "87", NComp(87),
                  dividend_xform="21'01",
                  subs = ["26", "13"],
                  carries = "00",
                  answer = "2174",
                  nikhilam = True,
                 ansplaces = 2)
        d.step_all(wait=3)

        #Span("Thus, the Quotient is 21 and remainder is 74", color="Turquoise")


        title1 = DisplayText(self,Span("Thus, the Quotient is ", color="Turquoise") +
                             Span("21 ", color="yellow", font="cambria math")+
                             Span("and Remainder is ", color="Turquoise")+ Span("74", color="yellow", font="cambria math"),
                             scale=0.5, wait=0, move=(2, -1),
                             fade=False)
        self.wait(3)

        d.clear()
        self.next_section()

        self.play(FadeOut(title1))
        self.play(FadeOut(title_h1,title_h2))


        text = [
            f"Now let's see another example where",
            f"the <span color='cyan'>face values </span>of <span color='yellow'>some digits </span>in the <span color='cyan'>Divisor Complement </span>are<span color='cyan'> large.</span>",
            f"In this case, ",
            f"we convert the <span color='cyan'>Divisor Complement</span> to its <span color='cyan'>vinculum form</span>",
            f"and do the division."]

        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        title_h1 = DisplayText(self, Span("Divide ", color="Turquoise")+
                               Span("2231 ", color="yellow", font="cambria math") +
                               Span("by ", color="Turquoise") +
                               Span("91: ", color="yellow", font="cambria math"),
                               scale=0.6, wait=0, move=(-3.5, -1), fade=False)
        self.wait(1)
        title_h2 = DisplayText(self, Span("By assessment, number of Quotient digits=", color="pink") +
                               Span("2", color="yellow", font="cambria math"),
                               scale=0.5, wait=0, move=(-3, -1), fade=False)

        self.wait(2)
        title_h3 = DisplayText(self,  Span("Complement of the divisor,", color="pink") +
                               Span("91", color="yellow", font="cambria math") +
                               Span("=", color="pink")+
                               Span("09", color="yellow", font="cambria math"),
                               scale=0.5, wait=0, move=(-2.5, -1), fade=False)

        self.wait(2)


        # 2231 / 91 = 2231 / 91
        # DC = 09 = 11'
        # Subs = 22', 44'
        # q = 24, r=53'
        d = Divop(self, "2231", "91","11'",
                  subs = ["22'", "44'"],
                  carries = "00",
                  answer = "2453'",
                  nikhilam = True,
                  ansplaces = 2)
        d.step_all(wait=3)

        title1 = DisplayText(self,
                             Span("Thus, the Quotient is ", color="Turquoise") +
                             Span("24 ", color="yellow", font="cambria math") +
                             Span("and Remainder is ", color="Turquoise") +
                             Span("47", color="yellow", font="cambria math"),
                             scale=0.5, wait=0, move=(2, -1),
                             fade=False)

        self.wait(4)

        d.clear()
        self.next_section()

        self.play(FadeOut(title1))

        self.play(FadeOut(title_h1, title_h2,title_h3))


        text = [
            f"Now let's see another division using the",
            f"vinculum form of both <span color='cyan'>Dividend </span>and <span color='cyan'>Divisor Complement.</span>"]

        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        title_h1 = DisplayText(self, Span("Divide ", color="Turquoise") +
                               Span("7873 ", color="yellow", font="cambria math") +
                               Span("by ", color="Turquoise") +
                               Span("81:", color="yellow", font="cambria math"),
                               scale=0.6, wait=0, move=(-3.5, -1), fade=False)
        self.wait(1)
        title_h2 = DisplayText(self, Span("By assessment, number of Quotient digits=", color="pink") +
                               Span("2 ", color="yellow", font="cambria math"),
                               scale=0.5, wait=0, move=(-3, -1), fade=False)

        self.wait(2)
        title_h3 = DisplayText(self,  Span("Complement of the divisor,", color="pink") +
                               Span("81", color="yellow", font="cambria math") +
                               Span("=", color="pink")+
                               Span("19", color="yellow", font="cambria math"),
                               scale=0.5, wait=0, move=(-2.5, -1), fade=False)

        self.wait(2)


        # 7873 / 81 = 12'1'3'3 / 81
        # DC = 19 = 21'
        # Subs = 21', 00, 4'2
        # q = 21, r=74
        d = Divop(self, 7873, "81","21'",
                  dividend_xform="12'1'3'3",
                  subs = ["21'", "00", "4'2"],
                  carries = "00",
                  answer = "102'7'5",
                  nikhilam = True,
                  ansplaces = 3)
        d.step_all(wait=3)




        title1 = DisplayText(self,
                             Span("Since the remainder is -ve, we add divisor(", color="Turquoise") +
                             Span("81", color="white", font="cambria math") +
                             Span(") to it and subtract ", color="Turquoise") +
                             Span("1 ", color="white", font="cambria math") +
                             Span("from Quotient", color="Turquoise"),
                             scale=0.5, wait=4, move=(2, -1),
                             fade=False)
        self.wait(4)

        title2 = DisplayText(self,
                             Span("Thus, Final values are: Quotient = ", color="Turquoise") +
                             Span("97 ", color="yellow", font="cambria math") +
                             Span("and Remainder = ", color="Turquoise") +
                             Span("16", color="yellow", font="cambria math"), scale=0.5,
                             wait=4, move=(2.5, -1),
                             fade=False)

        self.wait(1)
        
        d.clear()
        self.next_section()




        self.play(FadeOut(title1, title2))

        self.play(FadeOut(title_h1, title_h2,title_h3))
        self.next_section()




class ParavartyaDivision(Scene):
    def Iqr(self, quotient, remainder):
            q1 = MarkupText("Thus, the Quotient is").scale(0.65).set_color(TEAL_C).move_to(2*LEFT + DOWN*2)
            q2 = MarkupText(str(quotient)).scale(0.65).set_color(YELLOW).next_to(q1, RIGHT)
            r1 = MarkupText("and Remainder is").scale(0.65).set_color(TEAL_C).next_to(q2, RIGHT)
            r2 = MarkupText(str(remainder)).scale(0.65).set_color(YELLOW).next_to(r1, RIGHT)
            self.play(FadeIn(q1, q2, r1, r2))
            self.play(Indicate(q2))
            self.play(Indicate(r2))
            return(q1, q2, r1, r2)
    
    def construct(self):
            Title(self, "हरणम् 3", "Division 3", move=(3, 5), wait=2)
            self.next_section()
            self.wait(1)

            text = [
                    f"Today we learn a new method of division: <span color='cyan'>Paravartya (परावर्त्य).</span> ",
                    f"This method is applicable",
                    f"when the <span color='cyan'>first digit </span>of the <span color='cyan'>divisor</span> is <span color='yellow'>1.</span> ",
                ]

            e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)


            text = [
                    f"How does it differ from <span color='yellow'>Nikhilam?</span>",
                    f"Instead of the  <span color='yellow'>divisor complement</span>, as in <span color='yellow'>Nikhilam</span>,",
                    f"in <span color='cyan'>Paravartya</span> the <span color='cyan'>divisor</span> itself is used.",
                    f"Also, <span color='cyan'>first digit </span>of the<span color='cyan'> divisor </span>(which is always 1)",
                    f"is <span color='cyan'>not involved</span> in the <span color='cyan'>division process.</span>",
                    f"<span color='cyan'>Other divisor digits</span> are marked as <span color='cyan'>-ve</span>.",
                    f"The rest of the method is just like <span color='yellow'>Nikhilam.</span>",
            ]

            e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

            text = [f"<span color='OrangeRed'>Let's learn the process through an example.</span>" ]

            e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)



            title_h1 = DisplayText(self, Span("Divide ", color="Turquoise") +
                                   Span("2818 ", color="yellow", font="cambria math") +
                                   Span("by ", color="Turquoise") +
                                   Span("14:", color="yellow", font="cambria math"),
                                   scale=0.6, wait=0, move=(-3, -1), fade=False)
            self.wait(1)

            title_h2 = DisplayText(self, Span("By assessment, number of Quotient digits=", color="pink") +
                                   Span("3 ", color="yellow", font="cambria math"),
                                   scale=0.5, wait=0, move=(-2.5, -1), fade=False)

            self.wait(2)

            d = Divop(self, "2818", "14", "14'",
                      subs=["8'", "0", "4'"],
                      carries="00",
                      answer="2014",
                      ansplaces=3)
            d.step_all(wait=3)

            (q1, q2, r1, r2) = self.Iqr(201, 4)
            self.wait(1)
            
            d.clear()
            self.play(FadeOut(q1, q2, r1, r2))
            self.play(FadeOut(title_h1, title_h2))
            self.next_section()

            title_h1 = DisplayText(self, Span("Divide ", color="Turquoise") +
                                   Span("12321 ", color="yellow", font="cambria math") +
                                   Span("by ", color="Turquoise") +
                                   Span("112:", color="yellow", font="cambria math"),
                                   scale=0.6, wait=0, move=(-3, -1), fade=False)
            self.wait(2)

            title_h2 = DisplayText(self, Span("By assessment, number of Quotient digits=", color="pink") +
                                   Span("3", color="yellow", font="cambria math"),
                                   scale=0.5, wait=0, move=(-2.5, -1), fade=False)

            self.wait(2)

            # 12321 / 11
            # Subs = 1', 1', 2'
            # q = 1120, r=1

            """
            d = Divop(self, "12321", "11","11'",
                      subs = ["1'", "1'", "2'"],
                      carries = "00",
                      answer = "11201",
                      ansplaces = 4)
            d.step_all(wait=3)
            """
            d = Divop(self, "12321", "112", "11'2'",
                      subs=["1'2'", "1'2'", "00"],
                      carries="00",
                      answer="11001",
                      ansplaces=3)
            d.step_all(wait=3)

            (q1, q2, r1, r2) = self.Iqr(110, 1)
            self.wait(1)

            d.clear()
            self.play(FadeOut(q1, q2, r1, r2))
            self.play(FadeOut(title_h1, title_h2))
            self.next_section()

            text = [
                f"Just like <span color='cyan'>Nikhilam,</span> in <span color='cyan'>Paravartya</span> too, ",
                f"we can use <span color='cyan'>vinculum notation</span> for further digits of the  <span color='cyan'>divisor</span>",
                f"as long as its <span color='yellow'>first digit</span> remains as<span color='yellow'> 1.</span>",
                f"The <span color='cyan'>Dividend</span> can also be converted to vinculum if needed."]

            e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

            lastscene(self)

class ParavartyaDivisionVinculum(Scene):
    def Iqr(self, quotient, remainder):
            q1 = MarkupText("Thus, the Quotient is").scale(0.65).set_color(TEAL_C).move_to(2 * LEFT + DOWN * 2)
            q2 = MarkupText(str(quotient)).scale(0.65).set_color(YELLOW).next_to(q1, RIGHT)
            r1 = MarkupText("and Remainder is").scale(0.65).set_color(TEAL_C).next_to(q2, RIGHT)
            r2 = MarkupText(str(remainder)).scale(0.65).set_color(YELLOW).next_to(r1, RIGHT)
            self.play(FadeIn(q1, q2, r1, r2))
            self.play(Indicate(q2))
            self.play(Indicate(r2))
            return (q1, q2, r1, r2)

    def construct(self):
            Title(self, "हरणम् 4", "Division 4", move=(3, 5), wait=2)
            self.next_section()
            self.wait(1)

            text = [
                f"Let's continue <span color='cyan'>Paravartya(परावर्त्य) division.</span> ",
                f"In this video, we learn to solve some problems",
                f"in which the dividend or divisor is in the <span color='cyan'>vinculum form.</span>",
            ]

            e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)


            text = [
                f"By now, we know the <span color='yellow'>benefit</span> of <span color='cyan'>Vinculum numbers.</span>",
                f"<span color='cyan'>Face value</span> of the number is <span color='cyan'>reduced</span> in the <span color='cyan'>vinculum </span>form ",
                f"and this makes the <span color='yellow'>mathematical operations much easier.</span>",
                f"And if we are good in <span color='cyan'>negative number handling</span>,",
                f"<span color='cyan'>Vinculum form </span>of a number will surely <span color='yellow'>save our time.</span>"
            ]

            e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

            text = [
                f"Let's recap the <span color='cyan'>Paraavartya</span> Method.",
                f"We use this method only when the <span color='cyan'>first digit of the divisor is 1</span>",
                f"and <span color='cyan'>divisor</span> itself is <span color='cyan'>used for the Division Process</span>.",
                f"<span color='cyan'>First digit</span> of the <span color='cyan'>divisor</span> is <span color='cyan'>not used </span>in the Division.",
                f"Rest of the digits are marked as <span color='cyan'>negative.</span>"
            ]

            e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

            text = [
                f"In our first example,",
                f"we are doing the division with <span color='cyan'>vinculum of Divisor</span>.",
                f"So, <span color='cyan'>first we convert the divisor</span> to its <span color='cyan'>Vinculum</span> form.",
                f"Then we alter the <span color='cyan'>sign of all digits </span><span color='yellow'>except </span> <span color='cyan'>the first digit.</span>",
                f"Let's see the process in detail. "
                            ]

            e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

            title_h1 = DisplayText(self, Span("Divide ", color="Turquoise") +
                                   Span("2412 ", color="yellow", font="cambria math") +
                                   Span("by ", color="Turquoise") +
                                   Span("108:", color="yellow", font="cambria math"),
                                   scale=0.6, wait=0, move=(-3, -1), fade=False)
            self.wait(1)

            title_h2 = DisplayText(self, Span("By assessment, number of Quotient digits=", color="pink") +
                                   Span("2 ", color="yellow", font="cambria math"),
                                   scale=0.5, wait=0, move=(-2.5, -1), fade=False)

            self.wait(2)
             
            d = Divop(self, "2412", "108",
                      divisor_xform="112'", divisor_xform2="11'2",
                      subs=["2'4", "2'4"],
                      carries="00",
                      answer="2236",
                      ansplaces=2)
            d.step_all(wait=3)

             

            (q1, q2, r1, r2) = self.Iqr(22, 36)
            self.wait(1)

            d.clear()

            self.play(FadeOut(q1, q2, r1, r2))
            self.play(FadeOut(title_h1, title_h2))

            self.next_section()

            title_h1 = DisplayText(self, Span("Divide ", color="Turquoise") +
                                   Span("1298 ", color="yellow", font="cambria math") +
                                   Span("by ", color="Turquoise") +
                                   Span("12:", color="yellow", font="cambria math"),
                                   scale=0.6, wait=0, move=(-3, -1), fade=False)
            self.wait(1)

            title_h2 = DisplayText(self, Span("By assessment, number of Quotient digits=", color="pink") +
                                   Span("3 ", color="yellow", font="cambria math"),
                                   scale=0.5, wait=0, move=(-2.5, -1), fade=False)

            self.wait(2)

            d = Divop(self, "1298", "12",
                      divisor_xform="12'",
                      subs=["2'", "2'","4"],
                      carries="00",dividend_xform="1302'",
                      answer="112'2",
                      ansplaces=3)
                      
            d.step_all(wait=3)

            (q1, q2, r1, r2) = self.Iqr(108,2)
            self.wait(1)

            d.clear()
            #self.play(FadeOut(title_h1, title_h2))
            self.play(FadeOut(q1, q2, r1, r2))

            lastscene(self)

class Vilokanam(Scene):
    def Iqr(self, quotient, remainder):
        q1 = MarkupText("Thus, the Quotient is").scale(0.65).set_color(TEAL_C).move_to(2 * LEFT + DOWN * 2.5)
        q2 = MarkupText(str(quotient)).scale(0.65).set_color(YELLOW).next_to(q1, RIGHT)
        r1 = MarkupText("and the Remainder is").scale(0.65).set_color(TEAL_C).next_to(q2, RIGHT)
        r2 = MarkupText(str(remainder)).scale(0.65).set_color(YELLOW).next_to(r1, RIGHT)
        self.play(FadeIn(q1, q2, r1, r2))
        self.play(Indicate(q2))
        self.play(Indicate(r2))
        return (q1, q2, r1, r2)



    def construct(self):

            Title(self, "विलोकनेन हरणम्  ", "Division by Observation ", move=(3, 5), wait=2)
            self.next_section()
            self.wait(1)

            text = [
                    f"In this video,",
                    f"we learn to make <span color='yellow'>division simpler </span>",
                    f"using the sutra <span color='cyan'>Vilokanam.</span> ",
                    f"First, let's note a <span color='yellow'>problem with the basic method</span>",
                    f"and then we solve it by <span color='cyan'>Vilokanam.</span>"
            ]
            
            e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)
          
            text = [
                    f"During division, quotient or remainder digits may be >10,",
                    f"causing a 2 digit number where we want only a <span color='cyan'>single digit.</span>",
                    f"As we have seen, we can continue forward",
                    f"and assemble the final answer",
                    f"by <span color='yellow'>keeping the unit digits </span> and treating the <span color='yellow'>remaining digits as carry.</span>",
                    f"But <span color='cyan'> if we control each digit to be single,</span>",
                    f"<span color='cyan'>the division process will be even easier.</span>"
                ]
            e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

            text = [
                    f"So, how can we do this?",
                    f"We <span color='cyan'>fix the current digit after looking ahead</span>",
                    f"<span color='cyan'>to the value of the </span><span color='yellow'>next digit.</span>",
                    f"If the next digit won't be single,",
                    f"we <span color='cyan'> take a part of the current digit as carry to</span> <span color='yellow'>next digit </span> ",
                    f"so that next digit will be single."
            ]

            e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)           


            title_h1 = DisplayText(self, Span("Divide ", color="Turquoise") +
                                   Span("23276 ", color="yellow", font="cambria math") +
                                   Span("by ", color="Turquoise") +
                                   Span("81:", color="yellow", font="cambria math"),
                                   scale=0.4, wait=0, move=(-3, -1), fade=False)
            self.wait(1)

            title_h2 = DisplayText(self, Span("By assessment, number of Quotient digits=", color="pink") +
                                   Span("3", color="yellow", font="cambria math")+
                                   Span(" and Complement of the divisor, ", color="pink") +
                                   Span("81", color="yellow", font="cambria math") +
                                   Span("=", color="pink") +
                                   Span("19", color="yellow", font="cambria math"),
                                   scale=0.4, wait=0, move=(-2.5, -1), fade=False)

            self.wait(2)


            d = Divop(self, "23276", "81", "21'",
                      subs = ["42'", ["14", "7'"], ["28", "1'4'"]],
                      carries = "00",
                      answer = ["2","7","14", "28", "8'"],
                      nikhilam = True,
                      ansplaces = 3)
            
            d.step_all(wait=4)

            self.wait(2)

            title_h3 = DisplayText(self, Span("284", color="YELLOW", font="cambria math") ,
                                   scale=0.7, wait=0, move=(2.5, -1), fade=False)

            self.wait(5)

            title_h4 = DisplayText(self, Span("272", color="YELLOW")+
                                   Span("       3 | 29 ", color="YELLOW", font="cambria math"),
                                   scale=0.7, wait=0, move=(2.5, 2.5), fade=False)

            self.wait(11)

            self.play(FadeOut(title_h3, title_h4))
           
            (q1, q2, r1, r2) = self.Iqr(287,29)


            d.clear()
            self.play(FadeOut(title_h1, title_h2))
            self.play(FadeOut(q1, q2, r1, r2))

            text = [
                    f"Now, let's do the same process with <span color='cyan'>Vilokanam</span>"
            ]

            e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

            
            d = Divop(self, "23276", "81", "21'",
                       subs = ["42'", ["16", "8'"], ["14", "7'"]],
                       carries = ["0","1'0'", "1'0'", "10"],
                       answer = "28729",
                       backtrack_subs = ["42'", ["14", "7'"], ["12", "6'"]],
                       backtrack_carries = "0000",
                       backtrack_answer = ["2","7","6", "3", "1'"],
                       backtrack_next_answer = ["7","14", "11", "1'"],
                       backtrack_en=[False, True, True, True, False],
                       nikhilam = True,
                       backtrackp = True,
                       ansplaces = 3)

            d.step_all(wait=1)


            (q1, q2, r1, r2) = self.Iqr(287, 29)
            self.wait(1)

            d.clear()
            self.play(FadeOut(title_h1, title_h2))
            self.play(FadeOut(q1, q2, r1, r2))

            title_h1 = DisplayText(self, Span("Divide ", color="Turquoise") +
                                   Span("32458 ", color="yellow", font="cambria math") +
                                   Span("by ", color="Turquoise") +
                                   Span("88:", color="yellow", font="cambria math"),
                                   scale=0.4, wait=0, move=(-3, -1), fade=False)
            self.wait(1)

            title_h2 = DisplayText(self, Span("By assessment, number of Quotient digits=", color="pink") +
                                   Span("3", color="yellow", font="cambria math")+
                                   Span(" and Complement of the divisor,", color="pink") +
                                   Span("88", color="yellow", font="cambria math") +
                                   Span("=", color="pink") +
                                   Span("12", color="yellow", font="cambria math"),
                                   scale=0.4, wait=0, move=(-2.5, -1), fade=False)

            self.wait(2)


            d = Divop(self, "32458", "88", "12",
                       subs = ["36", ["6", "12"], ["8", "16"]],
                       carries = ["0","1'0'", "2'0'", "2'0'"],
                       answer = "36874",
                       backtrack_subs = ["36", ["5", "10"], ["6", "12"]],
                       backtrack_carries = "0000",
                       backtrack_answer = ["3","5","6", "5", "24"],
                       backtrack_next_answer = ["5","15", "23", "24"],
                       backtrack_en=[False, True, True, True, False],
                       nikhilam = True,
                       backtrackp = True,
                       ansplaces = 3)

            d.step_all(wait=1)

            (q1, q2, r1, r2) = self.Iqr(368,74)
            self.wait(1)

            d.clear()
            self.play(FadeOut(title_h1, title_h2))
            self.play(FadeOut(q1, q2, r1, r2))

            text = [
                f"Using the same procedure, ",
                f"we can simplify <span color='cyan'>Paravartya</span> division also.",
                f"Let's see an example of that."
            ]

            e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

            title_h1 = DisplayText(self, Span("Divide ", color="Turquoise") +
                                   Span("3458 ", color="yellow", font="cambria math") +
                                   Span("by ", color="Turquoise") +
                                   Span("13:", color="yellow", font="cambria math"),
                                   scale=0.4, wait=0, move=(-3, -1), fade=False)
            self.wait(1)

            title_h2 = DisplayText(self, Span("By assessment, number of Quotient digits=", color="pink") +
                                   Span("3", color="yellow", font="cambria math"),
                                   scale=0.4, wait=0, move=(-2.5, -1), fade=False)

            self.wait(2)

            d = Divop(self, "3458", "13",
                       divisor_xform="13'",
                       subs = ["6'", ["1'8'"], ["1'8'"]],
                       carries = ["10", "20", "10"],
                       answer = "2660",
                       backtrack_subs = [["9'"],["2'4'"],["2'1'"]],
                       backtrack_carries = "0000",
                       backtrack_answer = ["3","8","7","0"],
                       backtrack_next_answer = ["5'","1'9'","1'3'"],
                       backtrack_en=[True, True, True,False],
                       backtrackp = True,
                       ansplaces = 3)

            d.step_all(wait=1)

            (q1, q2, r1, r2) = self.Iqr(266, 0)
            self.wait(1)

            d.clear()

            self.play(FadeOut(title_h1, title_h2))
            self.play(FadeOut(q1, q2, r1, r2))
            lastscene(self)

            
class StraightDivision(Scene):
    def Iqr(self, quotient, remainder):
        q1 = MarkupText("Thus, the Quotient is").scale(0.65).set_color(TEAL_C).move_to(2 * LEFT + DOWN * 2.5)
        q2 = MarkupText(str(quotient)).scale(0.65).set_color(YELLOW).next_to(q1, RIGHT)
        r1 = MarkupText("and the Remainder is").scale(0.65).set_color(TEAL_C).next_to(q2, RIGHT)
        r2 = MarkupText(str(remainder)).scale(0.65).set_color(YELLOW).next_to(r1, RIGHT)
        self.play(FadeIn(q1, q2, r1, r2))
        self.play(Indicate(q2))
        self.play(Indicate(r2))
        return (q1, q2, r1, r2)

    def construct(self):
        Title(self, "ध्वजहरणम्", "Straight Division", move=(3, 5), wait=2)
        self.next_section()
        self.wait(1)

        text = [
            f"In the previous videos,",
            f"we saw division using <span color='yellow'>Nikhilam</span> and <span color='yellow'>Paravartya.</span>",
            f"These two were really easy methods,",
            f"but can be applied only when  <span color='yellow'>certain conditions are met.</span>",
        ]

        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)


        text = [
            f"Today we are learning <span color='yellow'>Straight Division,</span>",
            f"the <span color='yellow'>Universal Method</span> of division. ",
            f"Let's first understand this division process",
            f"and then we shall <span color='yellow'>simplify</span> the same by <span color='yellow'>observation.</span>",
        ]

        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        text = [
            f"Straight Division is almost same like <span color='yellow'>Paravartya</span>",
            f"but the <span color='yellow'>first digit of the divisor</span> also takes part in division. ",
            f"In the process, it is named as <span color='yellow'>temporary divisor.</span>",
            f"Actually the division is performed only by the <span color='yellow'>temporary divisor.</span>"
            ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        text = [
            f"Let's see the process in detail--",
            f"1.Just like <span color='yellow'>Nikhilam</span> and <span color='yellow'>Paravartya</span>",
            f"  first we estimate the <span color='yellow'>number of Quotient Digits.</span>",
            f"2.Divisor digits except the first are marked as <span color='yellow'>negative.</span>",
            f"  (Digits in the Vinculum form will become normal). ",
            f"3.The <span color='yellow'>first digit of the dividend </span>is divided by the <span color='yellow'>temporary divisor.</span>",
            f"  <span color='cyan'>Quotient</span> of this division is the <span color='yellow'>first answer digit</span>",
            f"  and the <span color='cyan'>carry</span> if any <span color='yellow'>is multiplied by 10</span> ",
            f"  and is written <span color='yellow'>above the next dividend digit.</span>"
            ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        text = [
            f"4.Then this first <span color='yellow'>Quotient digit</span> is multiplied with <span color='yellow'>flag digit(s)</span>",
            f"  and the <span color='yellow'>products</span> are written in the <span color='yellow'>next columns.</span>",
            f"5.Then the <span color='yellow'>digits in the 2nd column</span>",
            f"   <span color='cyan'>-carry if any, dividend digit and products from last step</span> ",
            f"   are added and the <span color='yellow'>result is divided by temporary divisor.</span>",
            f"Steps 3-5 are repeated until all the result digits are obtained."
        ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        text = [
            f"If we want the answer in <span color='cyan'>decimal form,</span> ",
            f"the result of <span color='cyan'>addition</span> in the columns for <span color='cyan'>remainder digits</span> ",
            f"are also <span color='yellow'>divided by the temporary Divisor.</span> ",
            f"<span color='cyan'>Otherwise this division is not needed.</span>",
        ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        #straight division

        title_h1 = DisplayText(self, Span("Divide ", color="Turquoise") +
                               Span("3393 ", color="yellow", font="cambria math") +
                               Span("by ", color="Turquoise") +
                               Span("24:", color="yellow", font="cambria math"),
                               scale=0.4, wait=0, move=(-3, -1), fade=False)
        self.wait(1)

        title_h2 = DisplayText(self, Span("By assessment, number of Quotient digits=", color="pink") +
                               Span("3", color="yellow", font="cambria math"),
                               scale=0.4, wait=0, move=(-2.5, -1), fade=False)

        self.wait(2)

        d = Divop(self, "3393", "24",
                  divisor_xform="24'",
                  subs=["4'", ["1'6'"], "4'"],
                  carries=["10","10","10"],
                  answer="1419",
                  ansplaces=3,
                  vertical=False)

        d.step_all(wait=3)
        self.wait(1)

        (q1, q2, r1, r2) = self.Iqr(141,9)
        self.wait(1)

        d.clear()

        self.play(FadeOut(title_h1, title_h2))
        self.play(FadeOut(q1, q2, r1, r2))


        title_h1 = DisplayText(self, Span("Divide ", color="Turquoise") +
                               Span("7468 ", color="yellow", font="cambria math") +
                               Span("by ", color="Turquoise") +
                               Span("38:", color="yellow", font="cambria math"),
                               scale=0.4, wait=0, move=(-3, -1), fade=False)
        self.wait(1)

        title_h2 = DisplayText(self, Span("By assessment, number of Quotient digits=", color="pink") +
                               Span("3", color="yellow", font="cambria math"),
                               scale=0.4, wait=0, move=(-2.5, -1), fade=False)

        self.wait(2)

        #straight division with observation
        d = Divop(self, "7468", "38",
                  divisor_xform="38'",
                  subs=[["8'"], ["7'2'"], ["4'8'"]],
                  carries=["40", "90", "60"],
                  answer=["1", "9", "6", "20"],
                  backtrack_subs=[["1'6'"], ["9'6'"], ["6'4'"]],
                  backtrack_carries=["10", "0", "0"],
                  backtrack_answer=["2", "12", "8", "20"],
                  backtrack_next_answer=["", "", "", "9"],
                  backtrack_en=[True, True, True, False],
                  backtrackp=True,
                  ansplaces=3)

        d.step_all(wait=1)
        self.wait(3)

        (q1, q2, r1, r2) = self.Iqr(196,20)
        self.wait(1)

        d.clear()

        self.play(FadeOut(title_h1, title_h2))
        self.play(FadeOut(q1, q2, r1, r2))

        title_h1 = DisplayText(self, Span("Divide ", color="Turquoise") +
                               Span("7172 ", color="yellow", font="cambria math") +
                               Span("by ", color="Turquoise") +
                               Span("246:", color="yellow", font="cambria math"),
                               scale=0.4, wait=0, move=(-3, -1), fade=False)
        self.wait(1)

        title_h2 = DisplayText(self, Span("By assessment, number of Quotient digits=", color="pink") +
                               Span("2", color="yellow", font="cambria math"),
                               scale=0.4, wait=0, move=(-2.5, -1), fade=False)

        self.wait(2)

        #straight division with observation 3 digit divisor

        d = Divop(self, "7172", "246",
                  divisor_xform="24'6'",
                  subs=[["8'", "1'2'"], ["3'6'", "5'4'"]],
                  carries=["30", "50", "60"],
                  answer=["2", "9", "3", "8"],
                  backtrack_subs=[["1'2'", "1'8'"], [""]],
                  backtrack_carries=["10", "10", "0"],
                  backtrack_answer=["3", "11", "9", ""],
                  backtrack_next_answer=["", "", "", ""],
                  backtrack_en=[True, True, True, False],
                  backtrackp=True,
                  ansplaces=2,
                  vertical=False)


        d.step_all(wait=1)

        (q1, q2, r1, r2) = self.Iqr(29, 38)
        self.wait(1)

        d.clear()

        self.play(FadeOut(title_h1, title_h2))
        self.play(FadeOut(q1, q2, r1, r2))
        lastscene(self)

        






