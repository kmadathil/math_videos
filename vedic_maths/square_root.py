from manim import *
from numpy import array
from common import *
from division import vinc_int, vinc_str, vinc_list, MT
import math


def DOpVal(n):
    'D Operator on integer n'
    # blast into digits
    nl = [int(s) for s in str(n)]
    d = 0
    # Multiply each digit with
    # counterpart in reversed number
    # Sum to get result
    for z in zip(nl, reversed(nl)):
        d += z[0] * z[1]
    return d


def DOp(scene, num, wait=0):
    ''' Display a D Operator '''
    n1 = MT(num)  # Initial number
    sr = DOpVal(num)  # D Operator result
    # Arrange number and lines
    g1, lines = DOp_(n1, sr, scene)
    # Add to scene
    scene.add(g1)
    scene.add(*lines)
    if wait:
        scene.wait(wait)
    return g1, lines


def DOPR(scene, num):
    title_h2 = DisplayText(scene, Span("D(" + str(num) + ")", color="Turquoise"),
                           scale=0.6, wait=0, move=(0, -1.5), fade=False)
    g1, lines = DOp(scene, num, wait=5)
    scene.remove(g1[0], g1[1], g1[2], g1[3])
    scene.remove(*lines)
    scene.play(FadeOut(title_h2))
    scene.wait(1)
    scene.next_section()


def DOp_(n1, sr, scene):
    ''' D Operator Internal (num)
       
        Copies num MathTex object, places the copy below original object
        Copy is colored gray
        Generates lines connecting first digit to the last digit of the copy etc
        Returns the copy object and the lines
    '''
    # Copy original number in grey
    n2 = n1.copy()
    n2.set_color(GREY)
    oplen = len(n2)
    # Dividing line
    ln = Line(start=array([-1 * oplen / 2, 0, 0]), end=array([0, 0, 0])).set_color(GRAY)
    # Result
    res = MT(str(sr), color=GRAY)
    # Arrange in group
    g1 = VGroup(n1, n2, ln, res)  # .arrange(DOWN, aligned_edge=RIGHT)
    n2.next_to(n1, DOWN, aligned_edge=RIGHT)
    ln.next_to(n2, DOWN, aligned_edge=RIGHT)
    res.next_to(ln, DOWN, aligned_edge=RIGHT)
    # Generate connecting lines _after_ the group has been
    # arranged
    lines = doplines(scene, n1, n2)
    return g1, lines


# Display D Operator lines pattern.
# This is a stripped down version of utlines from multiply
def doplines(scene, n1, n2, color=GRAY):
    n = len(n1)  # Length of inputs
    lines = [
        Line(n2[i].get_top(), [n2[-1].get_top()[0], n1[-1].get_bottom()[1], n1[-1].get_bottom()[2]]).set_color(color)
        for i in range(n)]

    def _display(show):
        # list show is in the order of top vertices (eg: [5, 4, 3])
        # bottom vertices will be the same reversed (eg: [3, 4, 5])
        # We zip the two to get the connection iterator (eg [(3, 5), (4, 4), (5, 3)])
        cnxns = zip(reversed(show), show)
        for c in cnxns:
            # Update line connections to get each urdhvatiryagbhyam pattern
            lines[c[0]].put_start_and_end_on(
                [n2[c[0]].get_top()[0], n2[c[0]].get_top()[1] + 0.05, n2[c[0]].get_top()[2]],
                [n2[c[1]].get_top()[0], n1[c[1]].get_bottom()[1] - 0.05, n1[c[1]].get_bottom()[2]])
            # This could have been (n2[c[0]].get_top(), [n2[c[1]].get_bottom())
            # However, we see some lines not looking "straight"

    # Display all the lines
    show = list(range(n))
    _display(show)
    return lines


class DOpTest(Scene):
    def construct(self):
        num = 345
        g1, lines = DOp(self, 345, wait=5)
        self.remove(g1[1], g1[2], g1[3])
        self.remove(*lines)
        self.wait(1)
        self.next_section()


# Square Root Operator
class SqRootOp:
    def __init__(self, scene, dividend, divisor,
                 subs=[], carries=[], answer=None, ansplaces=0,
                 backtrackp=False, backtrack_en=[],
                 backtrack_subs=[], backtrack_carries=[], backtrack_answer=None,
                 backtrack_next_answer=None,
                 buff=1,  # Buffer
                 wait=2):
        '''
        Square Root operator

        inputs:
           dividend: String/List
           divisor : String/List
           subs: List
           carries: List
           answer: List
           answerplaces: List
           scene   : Manim.Scene
        '''
        self.scene = scene

        self.ln = len(str(dividend))

        self.raw = MathTex("\sqrt{" + str(dividend) + "}", color="White")  # Raw divisor
        mtd = MT(dividend)
        if self.ln %2 == 0 :
            # Account for the invisible leading zero
            la = len(answer) + 1   
        else:
            la = len(answer)
        if la> self.ln:
            self.e_dividend = MT(str(dividend) + (la-len(mtd))*"0").arrange(buff=buff)   
            self.e_dividend[self.ln:].set_color(BLACK)
        else:
            self.e_dividend = mtd.arrange(buff=buff)  # Dividend

        # self.divisor_x = MT(divisor)
        self.scene.wait(1)

        self.e_divisor = MT(divisor, color='Lime')  # Transformed Divisor
        self.vln = Text("|")

        # Setup future subparts
        self.subs = subs
        if isinstance(answer, list):
            a_ = [MT(a) for a in answer]
            self.answer = VGroup(*a_)
        else:
            self.answer = MT(answer)

        self.carries = carries
        self.ansplaces = ansplaces

        self.backtrackp = backtrackp
        self.backtrack_subs = backtrack_subs
        if backtrack_answer is not None:
            if isinstance(backtrack_answer, list):
                a_ = [MT(a) for a in backtrack_answer]
                self.backtrack_answer = VGroup(*a_)
            else:
                self.backtrack_answer = MT(backtrack_answer)
        if backtrack_next_answer is not None:
            if isinstance(backtrack_next_answer, list):
                a_ = [MT(a) for a in backtrack_next_answer]
                self.backtrack_next_answer = VGroup(*a_)
            else:
                self.backtrack_next_answer = MT(backtrack_next_answer)
        self.backtrack_carries = backtrack_carries
        self.backtrack_en = backtrack_en
        self.dop_start = 1
        self.neven = 0
        if self.ln % 2 == 0:
            self.dop_start = 2
            self.neven = 1

    def clear(self):
        ''' Remove everything from scene'''
        for i in self.gc:
            self.scene.remove(i)
        for i in self.gs:
            self.scene.remove(i)
        for i in self.ga:
            self.scene.remove(i)
        for i in self.g2:
            self.scene.remove(i)
        for i in self.g1:
            self.scene.remove(i)

    def step_all(self, wait=3):
        ''' Run all steps '''
        for i in range(len(self.answer) + 1):
            self.step(i)
        self.scene.wait(wait)

    def step(self, n=0, wait=1, is_backtracking=False):
        ''' Single step (nth)
        
            n: integer
            
            The zeroth step shows the dividend
            The first step shows the first answer digit and temporary divisor
            The n(>0) th step shows the nth answer digit,
              the associated carry and associated flag carries 
        '''

        def _realign():  # Update alignments after redisplay
            gc.arrange(RIGHT, buff=1)
            ga.arrange(RIGHT, buff=1)
            gs.arrange(RIGHT, buff=1)
            # Answer pre-alignment
            for i, ax in enumerate(g2[-1]):
                ax.next_to(g2[0][i], DOWN, aligned_edge=RIGHT)
            for i, sx in enumerate(g2[1]):
                sx.next_to(g2[0][i], DOWN, aligned_edge=RIGHT)
            g2.arrange(DOWN, aligned_edge=LEFT)
            g1.arrange(RIGHT, aligned_edge=UP)
            # We do this instead of prepending gc to g2
            # to keep the divisor and vline alignment right
            for i, gcx in enumerate(gc):
                gcx.next_to(g2[0][i], UP, aligned_edge=RIGHT)
            # Loop over subs for horizontal alignment

        scene = self.scene
        if n == 0:
            # Display raw division statement
            scene.add(self.raw)
            scene.wait(3)

            # Set up operation
            ga = VGroup()  # Dummy group for answers
            gc = VGroup(MT("0", color="Black"))  # Dummy zeroth carry
            # FIXME change to Black after test
            gs = VGroup(MT("0", color="Black"))  # Dummy subs
            gs += MT("0", color="Black")  #
            # If first segment of dividend has two digits
            # add extra zeros (invisible) for alignment
            if self.ln % 2 == 0:
                gc += MT("0", color="Black")
                ga += MT("0", color="Black")
                gs += MT("0", color="Black")
                # vertical group
            g2 = VGroup(self.e_dividend, gs).arrange(DOWN, aligned_edge=LEFT)
            # Top group that will contain all elements
            g1 = VGroup(self.e_divisor, self.vln, g2).arrange(RIGHT, aligned_edge=UP)
            g1.arrange(RIGHT, aligned_edge=UP)

            # Transform dividend
            scene.play(ReplacementTransform(self.raw, self.e_dividend))
            scene.wait(2)

            # Color alternate groups differently
            # Note the first group being 1 or two digits
            clr = BLUE
            if self.ln % 2 == 0:
                self.e_dividend[0:2].set_color(BLUE)
                s = 2
            else:
                self.e_dividend[0].set_color(BLUE)
                s = 1
            while s < self.ln:
                if clr==BLUE:
                    clr = GREEN
                else:
                    clr = BLUE
                self.e_dividend[s:s + 2].set_color(clr)
                s += 2

            # Add dividend and carry groups
            scene.add(g2, gc)
            self.hln = Line(self.e_dividend[0].get_left(), self.e_dividend[-1].get_right())
            g2 += self.hln
            g2 += ga
            _realign()
            scene.wait(wait)
            self.g1 = g1
            self.g2 = g2
            self.gc = gc
            self.ga = ga
            self.gs = gs
        elif n == 1:
            ga = self.ga
            gc = self.gc
            g2 = self.g2
            g1 = self.g1
            gs = self.gs
            # First digit of answer
            ga += self.answer[0]
            _realign()
            self.scene.play(Indicate(self.answer[0]))
            # Next, show the next carry
            # Only nonzero carries are visible
            if n <= len(self.carries):
                c = self.carries[n - 1]
                _col = "Grey" if vinc_int(c) else "Black"
                ct = MT(c, color=_col)
                gc += ct
                _realign()
            scene.wait(wait)
            # Display temporary divisor
            scene.add(self.g1, self.vln)
            self.scene.play(Indicate(self.e_divisor))
            scene.wait(wait)
        elif ((not self.backtrackp) or (not self.backtrack_en[n - 1]) or is_backtracking):
            # Normal, or recursive call after backtracking
            ga = self.ga
            gc = self.gc
            g2 = self.g2
            g1 = self.g1
            gs = self.gs
            dop_start = self.dop_start
            if self.carries[n - 2]:
                self.scene.play(Indicate(self.gc[n - 1 + self.neven]))
            self.scene.play(Indicate(self.g2[0][n - 1 + self.neven]))
            self.scene.play(Indicate(self.g2[1][n - 1 + self.neven]), color=RED)
            self.scene.play(Indicate(self.e_divisor))

            # First, show the next answer bit
            if is_backtracking:
                ga[-1].become(self.answer[n - 1])
            else:
                ga += self.answer[n - 1]

            if n > self.ansplaces:
                ga[-1].set_color(RED)
            else:
                ga[-1].set_color(GREEN)
            scene.add(ga[-1])
            _realign()

            self.scene.wait(wait)

            # Next, show the next carry
            # Only nonzero carries are visible
            if n <= len(self.carries):
                c = self.carries[n - 1]
                _col = "Grey" if vinc_int(c) else "Black"
                ct = MT(c, color=_col)
                if is_backtracking:
                    gc[-1].become(ct)
                else:
                    gc += ct
                _realign()
                if vinc_int(c):
                    self.scene.wait(5)

            # DOP
            if n < len(self.answer):
                # Extra dividend zeros  
                # Do not  enter while backtracking (since this extension has been done)
                if ((n + self.neven) >= self.ln) and not is_backtracking:   
                        self.e_dividend[n + self.neven].set_color(RED)
                gd, lines = DOp_(ga[dop_start:], self.subs[n - 2], self.scene)
                scene.add(gd)
                scene.add(*lines)
                scene.wait(2)
                # show the next sub
                if is_backtracking:
                    gs[-1].become(gd[-1])
                else:
                    gs += gd[-1]
                gs[-1].set_color(WHITE)
                _realign()
                scene.remove(*gd[1:], *lines)
            self.scene.wait(wait)
        else:
            # Need backtracking
            ga = self.ga
            gc = self.gc
            g2 = self.g2
            g1 = self.g1
            gs = self.gs
            dop_start = self.dop_start
            if self.carries[n - 2]:
                self.scene.play(Indicate(self.gc[-1]))
            self.scene.play(Indicate(self.g2[0][n - 1 + self.neven]))
            self.scene.play(Indicate(self.g2[1][-1]), color=RED)
            self.scene.play(Indicate(self.e_divisor))

            # First, show the next answer bit, which we will later backtrack
            ga += self.backtrack_answer[n - 1]

            if n > self.ansplaces:
                self.backtrack_answer[n - 1].set_color(RED)
            else:
                self.backtrack_answer[n - 1].set_color(GREEN)
            scene.add(ga[-1])
            _realign()

            self.scene.wait(wait)

            # Next, show the next carry that will be backtracked
            # Only nonzero carries are visible
            if n <= len(self.backtrack_carries):
                c = self.backtrack_carries[n - 1]
                _col = "Grey" if vinc_int(c) else "Black"
                c_ = MT(c, color=_col)
                gc += c_
                _realign()
                if vinc_int(c):
                    self.scene.wait(5)

            # DOP
            if n < len(self.answer):
                # Extra dividend zeros  
                if ((n + self.neven) >= self.ln):   
                        self.e_dividend[n + self.neven].set_color(RED)
                gd, lines = DOp_(ga[dop_start:], self.backtrack_subs[n - 2], self.scene)
                scene.add(gd)
                scene.add(*lines)
                scene.wait(2)
                # show the next sub
                if is_backtracking:
                    gs[-1].become(gd[-1])
                else:
                    gs += gd[-1]
                gs[-1].set_color(WHITE)
                _realign()
                scene.remove(*gd[1:3], *lines)

            if self.carries[n - 1]:
                self.scene.play(Indicate(self.gc[-1]))
            self.scene.play(Indicate(self.g2[0][n + self.neven]))
            self.scene.play(Indicate(self.g2[1][-1]), color=RED)
            self.scene.play(Indicate(self.e_divisor))

            # Show the next answer bit, so we can establish the need to backtrack
            ga += self.backtrack_next_answer[n - 1]

            self.backtrack_next_answer[n - 1].set_color(GREY)
            scene.add(ga[-1])
            _realign()
            self.scene.wait(2)
            self.backtrack_answer[n - 1].set_color(GREY)
            if n <= len(self.backtrack_carries):
                c_.set_color(BLACK)
            if n <= len(self.backtrack_subs):
                gs[-1].set_color(GREY)
            self.scene.wait(4)

            # Now we have established the need to backtrack
            ## Remove next answer
            scene.remove(ga[-1])
            ga -= self.backtrack_next_answer[n - 1]
            # Now we recursively call step with backtracking enabled.
            self.step(n, wait=wait, is_backtracking=True)



def sqr(scene, num):

    el1 = [x for x in num]
    eg1 = MathTex(*el1, color="orange")
    eg1.move_to(UP * 2)

    for _el in eg1:
        scene.play(AddTextLetterByLetter(_el, time_per_letter=1))
    scene.wait(2)

    ndig = len(num)
    DCalc = []

    for i in range(ndig):
        st = ""
        for j in range(i + 1):
            st += num[j]
        DCalc.append("D(" + st + ")")

    for i in range(1, ndig):
        st = ""
        for j in range(i, ndig):
            st += num[j]
        DCalc.append("D(" + st + ")")

    el2 = [x for x in DCalc]
    eg2 = MathTex(*el2, color="Yellow").arrange(RIGHT * 2, aligned_edge=ORIGIN)
    eg2.next_to(eg1, DOWN)

    for _el in eg2:
        scene.play(AddTextLetterByLetter(_el, time_per_letter=1))
        scene.wait(1)
    scene.wait(2)

    D_Op_Val = [DOpVal(((DCalc[i].replace("D", "")).replace("(","")).replace(")","")) for i in range(len(DCalc))]

    el3 = [x for x in D_Op_Val]
    eg3 = MathTex(*el3, color="cyan").arrange(RIGHT, aligned_edge=ORIGIN)
    for i, _el in enumerate(eg3):
        _el.next_to(eg2[i], DOWN)

    for _el in eg3:
        scene.play(AddTextLetterByLetter(_el, time_per_letter=1))
        scene.wait(1)
    scene.wait(2)
    for _el in eg3:
        # Digits before lsb are carries
        _el[0:-1].set_color(GRAY)
    scene.wait(1)
    ans = []
    cy = 0
    for i in reversed(range(len(D_Op_Val))):
        sdig = str(cy + int(D_Op_Val[i]))
        if i == 0:
            ans.append(sdig)
        else:
            ans.append(sdig[-1])
        if len(sdig) > 1:
            cy = int(sdig[0:-1])
        else:
            cy = 0

    el4 = [x for x in ans]
    eg4 = MathTex(*el4, color="cyan").arrange(LEFT, aligned_edge=ORIGIN)
    l3 = len(eg3)-1
    for i, _el in enumerate(eg4):
        eg4[i].next_to(eg3[l3-i], DOWN, aligned_edge=RIGHT)

    for _el in eg4:
        scene.play(AddTextLetterByLetter(_el, time_per_letter=1))
        scene.wait(1)
    scene.wait(2)
    scene.play(FadeOut(eg1, eg2, eg3, eg4))


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

class Squares(Scene):
    def construct(self):
        Title(self, "वर्गगणनम्", "Finding Squares", move=(3, 5), wait=2)
        self.next_section()
        self.wait(1)

        text = [
            f"In our previous videos we learned to <span color='yellow'>Square</span> any number",
            f"satisfying one of these conditions:",
            f"1. If the <span color='cyan'>last digit is 5</span>",
            f"2. If the number is <span color='cyan'>near a power of 10</span>"
        ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        text = [
            f"In this video, we learn a <span color='cyan'>general method for squaring.</span>",
            f"Here we come across a new term: the <span color='cyan'>D Operator.</span>",
            f"It can be defined as the result of the",
            f"<span color='yellow'>longest step of the Vertically and Crosswise method</span> ",
            f"when a number is multiplied by itself."
        ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        title_h1 = DisplayText(self, Span("D Operator Examples ", color="Turquoise"),
                               scale=0.6, wait=0, move=(-3, -1), fade=False)

        DOPR(self, 8)
        DOPR(self, 67)
        DOPR(self, 345)
        DOPR(self, 2314)

        self.play(FadeOut(title_h1))

        text = [
            f"Let's see the process of squaring a number with <span color='yellow'>D Operator:</span>",
            f"Apply <span color='cyan'>D Operator</span> on each <span color='cyan'>segment</span> of the number.",
            f"Segments are chosen starting from the left-most digit,",
            f"adding one digit at a time. After all digits have been covered, ",
            f"we remove one digit at a time from the left,",
            f"until only the right-most digit remains."]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        text = [
            f"The answers from applying D operators on each segment",
            f"are considered as <span color='cyan'>partial products.</span>",
            f"To get the <span color='cyan'>final answer</span>,",
            f"starting from the right-most partial product,",
            f"we <span color='cyan'>retain only the unit digit</span> of each partial product,",
            f"and <span color='cyan'>carry the previous digits</span> to previous answer digits."
        ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        sqr(self, "27")
        sqr(self, "123")
        sqr(self, "3476")
        lastscene(self)

class SquareRoot(Scene):
    def construct(self):
        Title(self, "वर्गमूलम्", "Square Root", move=(3, 5), wait=2)
        self.next_section()
        self.wait(1)

        text = [
            f"We learned <span color='yellow'>straight division</span> in previous videos.",
            f"A variant of straight division can be used",
            f"to find the <span color='cyan'>Square Root</span> of any number.",
            F"The <span color='yellow'>D Operator</span> is also used in this method.",
            f"Let's learn this method in this video."
        ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        text = [
            f"To find the square root of a number:",
            f"Starting from the <span color='yellow'>right most digit,</span>",
            f"divide the number into <span color='cyan'>groups of 2 digits.</span>",
            f"It's ok to have <span color='orange'>1 or 2 digits</span> in the <span color='yellow'>left most group.</span>",
            f"The <span color='orange'>number of digits in the answer</span> before the decimal point",
            f"is equal to <span color='cyan'>the number of groups.</span>"
        ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        text = [
            f"Consider the number in the <span color='cyan'>left most group.</span>",
            f"Find the <span color='yellow'>perfect square</span> <span color='cyan'>less than or equal</span> to it.", 
            f"<span color='yellow'>Square root</span> of this <span color='cyan'>perfect square</span> is the <span color='orange'>first digit</span> of the answer.",
            f"<span color='yellow'>Double</span> of this <span color='orange'>first digit</span> is called the <span color='cyan'>temporary divisor.</span>",
            f"Prepend the <span color='yellow'>difference </span>between the <span color='cyan'>left group</span> of the number",
            f"and the <span color='cyan'>square of the </span><span color='orange'>first digit</span> of the answer",
            f"to the next digit of the number as <span color='orange'>carry.</span> "
            ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        text = [
            f"<span color='yellow'>Grouping</span> was done to find the <span color='orange'>first digit </span>",
            f"and <span color='yellow'>number of digits</span> in the answer,",
            f"and groups have no significance in the rest of the process."
        ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        text = [
            f"<span color='yellow'>Divide</span> the next digit of the number by the <span color='cyan'>temporary divisor</span> ",
            f"and bring down the <span color='yellow'>quotient</span> as the <span color='yellow'>second digit</span> of the answer. ",
            f"Prepend the <span color='orange'>remainder</span> to the <span color='yellow'>succeeding digit </span>of the number."
        ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        text = [
            f"At each step, from the next digit of the number,",
            f"1. <span color='yellow'>Subtract</span> the result of the <span color='cyan'>D operator</span> ",
            f"  on the <span color='yellow'>previous digits of the answer</span>",
            f"  (not including the number we estimated as first answer digit) ",
            f"2. Then, <span color='yellow'>divide</span> it by the <span color='cyan'>temporary divisor,</span> ",
            f"3. Bring the <span color='yellow'>quotient</span> down as the  <span color='yellow'>next digit</span> of the answer.",
            f"4. Prepend any  <span color='orange'>remainder</span> to the  <span color='yellow'>next digit</span> as usual."
        ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        text = [
            f"The answer for any step cannot be  <span color='yellow'>negative.</span>",
            f"If it is, reduce the answer for the previous step ",
            f" till it becomes positive or zero.",
            f"We can use the  <span color='yellow'>backtracking procedure</span> for this. "
        ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        text = [
            f"If the <span color='cyan'>number</span> is not a <span color='yellow'>perfect square,</span>",
            f"continue past the <span color='yellow'>decimal point</span> of the answer ",
            f"adding decimal zeros to the number as necessary,",
            f"and use the same procedure to get <span color='yellow'>decimal digits</span>",
            f"of the answer."
        ]
        e = Explanation(self, text, wait=3, fade=True, aligned_edge=LEFT)

        s = SqRootOp(self, 2025, 8,
                  subs = [25],
                  carries=[40, 20],
                  answer=[4, 5, 0],
                  ansplaces=2,
                  backtrackp=False,
                  wait=5)
        s.step_all()
        self.wait(5)
        s.clear()
        self.next_section()

        s = SqRootOp(self, 14641, 2,
                 subs = [4, 4, 1],
                 carries=[0, 0, 0, 0],
                 answer=[1, 2, 1, 0, 0],
                 ansplaces=3,
                 backtrackp=False,
                 wait=5)
        s.step_all()
        self.wait(5)
        s.clear()

        self.next_section() 
        s = SqRootOp(self, 16129, 2,
                     subs = [4, 28, 49],
                     carries=[0, 20, 30, 40],
                     answer=[1, 2, 7, 0, 0],
                     ansplaces=3,
                     backtrackp=True,
                     backtrack_en = [False, True, True, True, False],
                     backtrack_answer = [1, 3, 8, 2, 0],
                     backtrack_next_answer = [1, "2'", "1'0", "2'2'"],
                     backtrack_subs = [6, 32, 53],
                     backtrack_carries = [0, 0, 10, 0],
                     wait=5)
        s.step_all()
        self.wait(5)
        s.clear()
        self.next_section()
        s = SqRootOp(self, 1000, 6,
                     subs = [1, 12, 40, 28],   # 56
                     carries=[10, 40, 30, 60, 80],  # 100
                     answer=[3,1,6,2,2,8],
                     ansplaces=2,
                     backtrackp=True,
                     backtrack_en = [False, False, False, True, True, False],
                     backtrack_answer = [3, 1, 6, 3, 3, 8],
                     backtrack_next_answer = [1, 6, 3, "7'", "2'"],   # "0'"
                     backtrack_subs = [1, 12, 42, 30, 44],
                     backtrack_carries = [0, 0, 0, 0, 20],  # 40
                     wait=5)
        s.step_all()
        self.wait(5)
        s.clear()
        lastscene(self)


