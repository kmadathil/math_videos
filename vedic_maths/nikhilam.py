from manim import *
from numpy import array
from common import *


# Helper Function for Nikhilam
def NikhilamExample(scene, num):
    l = len(num)
    # Text version of input
    t2 = MarkupText(num, font='Cambria Math').set_color(YELLOW).move_to(LEFT)  # Calc
    t22 = MarkupText(num, font='Cambria Math').set_color(YELLOW)  # Final Display

    # Horizontal line
    ln = Line(start=array([-1 * l / 2, 0, 0]), end=array([0, 0, 0])).set_color(YELLOW).next_to(t2, DOWN,
                                                                                               aligned_edge=RIGHT)

    # COmplement
    l9 = l - len(num.lstrip('9'))
    p = str(10 ** l - int(num))
    p0 = '0' * l9 + p
    t3 = MarkupText(p0, font='Cambria Math').set_color(ORANGE).next_to(ln, DOWN, aligned_edge=RIGHT)
    t33 = MarkupText(p, font='Cambria Math').set_color(ORANGE)  # Final Display

    # 9s and 10
    # Trailing zeros
    lz = l - len(num.rstrip('0'))
    t = MarkupText("9" * (l - lz - 1), font='Cambria Math').scale(0.9)
    ts = "10"
    tt = MarkupText(ts, font='Cambria Math').scale(0.7)
    g1 = VGroup(t, tt).arrange(direction=RIGHT, buff=0.1).set_opacity(0.8).next_to(t2,
                                                                                   UP, aligned_edge=LEFT)

    # Answer
    g2 = VGroup(t33, Text("is the complement of", font_size=38), t22).arrange(RIGHT).next_to(t3, 2 * DOWN)

    scene.play(Write(t2))
    scene.play(FadeIn(ln))
    scene.play(AddTextLetterByLetter(tt, time_per_char=0.1))
    scene.play(AddTextLetterByLetter(t, time_per_char=0.5))
    scene.wait(5)
    scene.play(AddTextLetterByLetter(t3, time_per_char=3))
    scene.play(FadeIn(g2))

    scene.wait(4)
    scene.play(FadeOut(t2, g1, ln, t3, g2))


# Helper function for subtraction example
def SubExample(scene, num1, num2):
    op = MarkupText("-")
    op1 = MarkupText("+")
    sn1 = str(num1)
    sn2 = str(num2)
    # Number lengths
    len1 = len(sn1)
    len2 = len(sn2)
    dlen = abs(len1 - len2)
    mlen = max(len1, len2)
    lenz = len2 - len(sn2.rstrip('0'))
    len9 = len2 - 1 - lenz

    # Prepend shorter number with 0s
    if len1 > len2:
        sn2 = "0" * dlen + sn2
    elif len2 > len1:
        sn1 = "0" * dlen + sn1

    # Setup minuend, subtrahend, complement and answer
    n1 = MarkupText(sn1, font='Cambria Math').set_color(GREEN)
    d1 = MarkupText("Minuend").set_color(GREEN)
    n2 = MarkupText(sn2, font='Cambria Math').set_color(YELLOW)
    d2 = MarkupText("Subtrahend", font='Cambria Math').set_color(YELLOW)
    n3 = MarkupText("?")
    # ans = "172469"
    if num1 >= num2:
        # Positive answer
        ans = "1" + str(num1 - num2).zfill(len(sn1))
        posans = True
    else:
        # Negative answer
        ans = str(10 ** mlen - (num2 - num1))
        posans = False

    res = MarkupText(ans, font='Cambria Math')
    ln = Line(start=array([-1 * 2, 0, 0]), end=array([0, 0, 0])).set_color(YELLOW)
    g1 = VGroup(n1, n2, ln, n3).arrange(DOWN, aligned_edge=RIGHT).move_to(UP * 2)
    g = VGroup(g1, op).arrange(RIGHT, aligned_edge=UP)
    op.next_to(n1, RIGHT)
    g2 = VGroup(d1, d2).arrange(DOWN).next_to(g, LEFT, aligned_edge=UP, buff=1)

    cmpl = MarkupText(str(10 ** mlen - num2), font='Cambria Math').set_color(ORANGE)
    ct = MarkupText("Complement of Subtrahend").scale(0.5).set_color(ORANGE)
    cmpl.next_to(n2, ORIGIN)
    
    DisplayText(scene, Span("Example", color="Turquoise"), scale=0.8, wait=2, move=(-3, -2))
    scene.play(FadeIn(g))
    scene.play(FadeIn(g2))
    scene.wait(3)
    scene.play(FadeOut(g2))

    DisplayText(scene, "1. Find the complement of the <span color='yellow'>Subtrahend</span>.", scale=0.8, wait=1,
                move=(-2, 0), font='Cambria Math')
    
    for ix, c in enumerate(n2):
        scene.play(Transform(n2[ix], cmpl[ix]))
    scene.play(FadeIn(ct.next_to(n2, RIGHT)))
    scene.wait(2)
    pos = n2.get_center()
    opos = op.get_center()
    DisplayText(scene, "2. Add the complement to the Minuend.", scale=0.8, wait=1, move=(-2, 0), font='Cambria Math')

    op1.next_to(op, ORIGIN)
    scene.play(Transform(op, op1))
    scene.play(FadeOut(n3))
    scene.play(FadeIn(res.next_to(ln, DOWN, aligned_edge=RIGHT)))
    scene.wait(3)
    if posans:
        fb = SurroundingRectangle(res[0], buff=0.1)
        scene.play(Create(fb))
        DisplayText(scene, "If the result has an extra digit of 1, the answer is positive.", scale=0.5, wait=3,
                    move=(2, -2), font='Cambria Math')
        DisplayText(scene, "Drop the extra 1 to get the final answer.", scale=0.5, wait=3, move=(2, -2),
                    font='Cambria Math')
        scene.play(res[0].animate.set_opacity(0.3))
        scene.wait(2)
        scene.play(FadeOut(fb))
        DisplayText(scene, f"<span color='Turquoise'>The answer is </span> {ans[1:]}", scale=0.7, wait=5, move=(2, -1), font='Cambria Math')
    else:
        ans2 = -1 * (10 ** mlen - int(ans))
        res2 = MarkupText(str(ans2), font='Cambria Math').next_to(res, ORIGIN)
        assert ans2 == (num1 - num2), f"Problem - {ans2} !- {num1} - {num2}"
        DisplayText(scene, "If the result does not have an extra digit, it is negative.", scale=0.5, wait=3,
                    move=(2, -2))
        DisplayText(scene, "Take the complement of the result and add a negative sign.", scale=0.5, wait=1,
                    move=(2, -2))
        scene.play(Transform(res, res2))
        scene.wait(3)
        DisplayText(scene, f"<span color='Turquoise'>The answer is </span> -{10 ** mlen - int(ans)}",  scale=0.7, wait=5, move=(2, -1), font='Cambria Math')

    scene.remove(n1, ln, n2, op, ct, res)



def ShowNikhilamOp(scene, sn1, sn2, sop, sr, move=(0, 0), wait=3, play=True, fade=True, oplen=0):
    ''' Helper function to display a Nikhilam Operation 
    
        Different from ShowOp in that the Nikhilam minuend is left aligned with 
        the subtrahend (looks better)
    '''
    g = ShowOp(scene, sn1, sn2, sop, sr, move, wait, play, fade, oplen)
    g[0][0].next_to(g[0][1], UP, aligned_edge=LEFT)
    g[1].next_to(g[0][0], RIGHT, aligned_edge=UP)
    return g

def NinesExample(scene, num, mplr, wait=3, fade=True):
    ''' Example for multiply by nines using ekannyUnena'''
    snum = str(num)
    inum = int(num)
    smplr = str(mplr)
    implr = int(mplr)
    ml = max(len(snum), len(smplr))
    snum = snum.zfill(ml)
    cmpl = complement(inum, ml)
    scmpl = "<span color='orange'>" + str(cmpl).zfill(len(snum)) + "</span>"
    # String of 9s
    assert mplr == int('9' * len(smplr)), "This works only for a number that's all nines"
    g0 = ShowOp(scene, num, mplr, "×", "?", fade=False)

    t = DisplayText(scene, " 1. Find the complement of the Multiplicand.", scale=0.7, wait=0, move=(-3, -1),
                    fade=False, font='Cambria Math')

    if len(str(num)) < len(str(mplr)):
        t2 = DisplayText(scene, "Zero prefixed as multiplicand digits are less.", scale=0.7, wait=0, move=(2, -1),
                         fade=False)

    g = ShowNikhilamOp(scene, niks(num, len(snum)), snum, "-", scmpl, oplen=len(snum), fade=False, play=False)
    scene.play(Transform(g0, g))
    scene.wait(3)

    scene.play(FadeOut(t))
    if len(str(num)) < len(str(mplr)):
        scene.play(FadeOut(t2))

    t = DisplayText(scene, "2. Prepend it with a -1 (single negative digit).", scale=0.7, wait=0, move=(-3, -1),
                    fade=False, font='Cambria Math')
    s2 = "<span size='small'>-1</span>" + scmpl
    t1 = DisplayText(scene, "Note, this doesn't make the whole number negative!", scale=0.7, wait=0, move=(2, -1),
                     fade=False)
    ds2 = MarkupText(s2, font='Cambria Math')
    #ds2.move_to(g0[0][3].get_center())
    ds2.next_to(g0[0][3], ORIGIN, aligned_edge=RIGHT)
    scene.play(Transform(g0[0][3], ds2))
    scene.wait(3)

    scene.play(FadeOut(t, t1))
    t = DisplayText(scene, "3. Append one zero to the multiplicand for each 9 in the multiplier.",
                    scale=0.7, wait=0, move=(-3, 0), fade=False, font='Cambria Math')
    ans = inum * (10 ** len(smplr)) + cmpl - 10 ** ml
    assert ans == (inum * implr), f"Error> Compute error in ekanyunena {ans} {inum * implr}"
    snumz = snum + '0' * len(smplr)
    g3 = ShowOp(scene, snumz, s2, "+", ans, play=False, wait=7, fade=False)
    scene.play(Transform(g0, g3))
    scene.wait(3)
    scene.play(FadeOut(t))

    t = DisplayText(scene, "4. Add with the result of step 2.", scale=0.7, wait=0, move=(-3, -1), fade=False,
                    font='Cambria Math')
    t1 = DisplayText(scene, "Note how the negative digit is handled!", scale=0.7, wait=0, move=(2, -1), fade=False)
    scene.wait(3)
    scene.play(FadeOut(t, t1))
    t = DisplayText(scene, "5. That sum is our answer.", scale=0.7, wait=5, move=(-3, 0), fade=False, font='Cambria Math')
    g4 = ShowOp(scene, num, mplr, "×", ans, wait=0, move=(0, 3), fade=False, play=False)
    scene.play(Transform(g0, g4))

    scene.wait(7)
    scene.play(FadeOut(t, g0))


# Nikhilam Minuend for complement
def niks(num, oplen=0):
    snum = str(num)
    length = len(snum)
    lz = length - len(snum.rstrip('0'))
    if oplen == 0:
        len9 = length - 1 - lz
    else:
        len9 = oplen - 1 - lz
    return "9" * len9 + "<span size='small'>10</span>"


# 10s Complement
def complement(i: int, l: int = 0):
    if l == 0:
        l = len(str(i))
    return (10 ** l - i)

def NikhilamGraph(scene, num, wait=3, fade=True):
    snum = str(num)
    tpow = 10**len(snum)
    cmpl = tpow - num
    nl = NumberLine([0, tpow, int(tpow/10)],
                    length=10,
                    include_ticks=True,
                    include_numbers=True)
    nump = nl.number_to_point(num)
    tpowp = nl.number_to_point(tpow)
    zp = nl.number_to_point(0)
    b1 = BraceBetweenPoints(nump, zp)
    b2 = BraceBetweenPoints(tpowp, nump)
    l1 = MarkupText(Span(snum, color='yellow'))
    l2 = MarkupText(Span(str(cmpl), color='orange'))
    l1.next_to(b1, UP)
    l2.next_to(b2, UP)
    for o in [l1, l2, nl, b1, b2]:
        scene.play(Create(o))
    scene.wait(wait)
    if fade:
        scene.play(FadeOut(nl, b1, b2, l1, l2))

class Nikhilam(Scene):
    def construct(self):

        # Title Scene
        Title(self, "परिपूरकम्", "Complement")
        self.next_section()

        # Definition
        el = ["A <span foreground='Turquoise'>Complement </span>Completes a Number.",
              "A <span foreground='yellow'>Number</span> and its <span foreground='orange'>Complement</span>",
              "always add up to the next higher power of 10."]
        eg = Explanation(self, el, wait=3, font='Cambria Math')
        self.play(eg.animate.move_to(UP * 2.5))
        for k in [17, 543, 192]:
            NikhilamGraph(self, k)
        self.play(FadeOut(eg))
        self.next_section()
        DisplayText(self, Span("One obvious way to calculate complements is to subtract.", color="yellow"), scale=0.6)
        t = ShowOp(self, 100, 17, "-", 83, wait=2, fade=True)
        t = ShowOp(self, 1000, 534, "-", 1000-534, wait=2, fade=True)
        tl = [
            "Is there an easier way to calculate complements?",
            "As it turns out, there is.",
            "And there is a sutra (aphorism) that helps us remember how."
            ]
        t = Explanation(self, tl, wait=3, aligned_edge=LEFT)
        
        # Sutra Scene
        t0 = "निखिलं नवतश्चरमं दशतः"
        t1 = ["निखिलं नवतः ", "चरमं दशतः"]
        t2 = ["All from 9, ", "Last from 10"]

        Sutra(self, t0, t1, t2, wait=3, scale=1, move=None, fade=True, font='Cambria Math')
        self.next_section()

        # Explanation
        el = ["<span color='Turquoise'>To Calculate the Complement of a Number:</span>",
              Span("Subtract the last nonzero digit from 10,", color='yellow'),
              Span("And all other digits to the left of it from 9.", color='yellow'),
              "This treats every digit independently,",
              "And is easier to calculate mentally."
              ]
        eg = Explanation(self, el, wait=5, font='Cambria Math', aligned_edge=LEFT)
        #self.play(eg.animate.scale(0.4).move_to(RIGHT * 5))
        self.next_section()

        # Example 1
        # 17, 83, 189, 320, 765432 , 58730, 982000
        titex = Text("Examples", color='Turquoise', font_size=40)
        self.play(Write(titex))
        self.wait(3)
        self.play(titex.animate.move_to(UP * 2 + LEFT))

        examples = ["17", "83", "189", "320", "765432", "58730", "982000"]
        for num in examples:
            NikhilamExample(self, num)
        self.play(FadeOut(titex))
        
        self.wait(10)


class Subtraction(Scene):
    def construct(self):
        # Title
        Title(self, "परिपूरकेण व्यवकलनम् ", " Subtraction using Complement", move=(3, 5), wait=1)
        self.next_section()
        # Introduction
        text = [" <span color='Turquoise'>A basic application of Complements - </span>",
                "Subtraction without the pain of borrowing."]
        Explanation(self, text, wait=5)
        self.next_section()
        text = ["Subtraction is a simple operation.",
                "However, long borrow chains make mental subtraction non-trivial.",
                "Take, for example, this problem.",
                "Can you do this mentally without strain?"
                ]
        
        Explanation(self, text, scale=0.5)
        self.next_section()
        g = ShowOp(self, 11231, 8764, "-", "?", wait=3)
        self.next_section()
        
        text = [
            "Once you visually determine the need for borrowing,",
            "Use this method instead."
              ]
        Explanation(self, text, scale=0.5, aligned_edge=LEFT)
        self.next_section()

        # Explanation
        text = ["<span color='Turquoise'>To subtract using complements:</span>",
                "Calculate the complement of the second number (subtrahend) using nikhilam,",
                "Add it to the first number (minuend).",
                "This removes the need to borrow.",
                "If the answer has an extra 1, it is positive, just drop the 1.",
                "If not, take the complement of the answer, and add a minus sign.",
                "Each of these steps can (and should) be done mentally with practice!",
                ]
        Explanation(self, text, scale=0.5, aligned_edge=LEFT, font="Cambria Math")
        self.next_section()

        # Detailed Example
        SubExample(self,  11231, 8764)
        self.next_section()
        SubExample(self, 91234, 18765)
        self.next_section()
        
        # Detailed Example - Negative Answer
        SubExample(self, 432, 798)
        self.next_section()
        SubExample(self, 14569, 69875)
        self.next_section()
        self.wait(10)
        
# Subtracting sequence of nines with ekyanyunena
class Ekanyunena(Scene):
    def construct(self):
        # Title
        Title(self, "नवश्रेणीगुणनम्", "Multiplying by nines", move=(3, 5), wait=1)
        self.next_section()
        # Introduction
        text = ["<span color='Turquoise'>Multiplying by a series of nines</span>",
                "Using complement, shift, and a bit more (or less?)"]
        Explanation(self, text)
        self.next_section()
        # # Revision and Example

        # eg = DisplayText(self, "Revision (Complement)", fade=True)
        # self.next_section()

        # # Sutra Scene
        # t0 = "निखिलं नवतश्चरमं दशतः"
        # t1 = ["निखिलं नवतः ", "चरमं दशतः"]
        # t2 = ["All from 9, ", "Last from 10"]
        # Sutra(self, t0, t1, t2, wait=1, scale=0.5, move=None, fade=True, font='Cambria Math')
        # self.next_section()
        # # Explanation
        # el = ["<span color='Turquoise'>To Calculate the Complement of a Number</span>", "Subtract the last nonzero digit from 10",
        #       "And all other digits to the left of it from 9."]
        # eg = Explanation(self, el, wait=2, fade=True, font='Cambria Math')
        # self.next_section()

        # NikhilamExample(self, "6583200")
        # self.next_section()

        # eg = DisplayText(self, "How do we use this for multiplying by nines?", scale=0.7, wait=0, move=(-3, 0), fade=False)
        # g = ShowOp(self, 98765, 999, "×", "?", wait=0, fade=False)
        # self.wait(5)
        # self.play(FadeOut(eg, g))

        # self.next_section()

        # Sutra Scene
        t0 = "एकन्यूनेन पूर्वेण"
        t1 = ["एकन्यूनेन", "पूर्वेण"]
        t2 = ["By one less than", "the previous"]
        Sutra(self, t0, t1, t2, wait=3, scale=1, move=None, fade=True, font='Cambria Math')
        self.next_section()

        text = ["<span color='Turquoise'>To multiply by a series of nines </span>",
                "1. Calculate the complement of the multiplicand",
                "2. Prepend it with a -1 (single digit)",
                "3. Append as many zeros to the multiplicand",
                "    ...  as there are nines in the multiplier",
                "4. Add with the result of step 2",
                "5. The sum is our answer."]
        Explanation(self, text, aligned_edge=LEFT, font='Cambria Math')
        self.next_section()
        # Example

        NinesExample(self, 123, 99)
        self.next_section()

        NinesExample(self, 9876, 999)
        self.next_section()

        NinesExample(self, 451, 9999)
        self.next_section()
        self.wait(10)
