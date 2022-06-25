from manim import *
from numpy import array
from common import *
import math


def EkadhikenaSquare(scene, num, wait=5, fade=True):
    snum = str(num)
    inum = int(num)
    sprev = snum[:-1]
    prev = int(sprev)
    assert snum[-1] == "5", "Only works with numbers ending in 5"
    text= [
        f"<span color='Turquoise'>Find the Square of </span><span color='yellow'>{snum}</span>.",
#        f"Digit(s) before 5 are <span color='yellow'>{sprev}</span>",
#        f"One more than that is  <span color='yellow'>{prev+1}</span>",
#        f"Our answer is simply <span color='yellow'>{prev} times {prev+1}, suffixed with 25</span>",
#        f"Which is <span color='yellow'>{prev*(prev+1)}{25}</span>."
    ]
    Explanation(scene, text, font='Cambria Math', aligned_edge=LEFT)
    scene.next_section()
    ans = inum**2
    assert ans == prev*(prev+1)*100+25
    snum2 = snum
    f1 = f2 = 5
    return EkCom(scene, snum, snum2, prev, f1, f2, ans, wait, fade)

def EkCom(scene, snum, snum2, prev, f1, f2, ans, wait=5, fade=True):
    lans = prev*(prev + 1)
    rans = f1*f2
    ndig = 2

    g   = ShowOp(scene, snum, snum2, "×", "?", wait=1, fade=False)
    gc = g.copy()
    g11   = ShowOp(scene, prev, "<span color='red'>"+str(prev+1)+"</span>", "×", lans, play=False)
    g12   = ShowOp(scene, f1, f2, "×", rans, play=False)

    ar = Text("_" * ndig, color='yellow').scale(1.2)
    arf = Text(str(rans).zfill(ndig), color='yellow', font='Cambria Math').scale(1.2)
    al = Text("_" * len(str(lans)), color='yellow').scale(1.2)
    alf = Text(str(lans), color='yellow', font='Cambria Math').scale(1.2)
    br = SurroundingRectangle(ar, buff=0.5)
    bl = SurroundingRectangle(al, buff=0.5)
    ga = VGroup(VGroup(al, bl), VGroup(ar, br)).arrange(RIGHT)
    
    ga.move_to(DOWN*2)
    arf.next_to(ar, ORIGIN)
    alf.next_to(al, ORIGIN)
    scene.add(ga)
    scene.wait()
    g11.next_to(ga[0], UP)
    g12.next_to(ga[1], UP)
    scene.add(gc.move_to(4*LEFT))
    scene.play(Transform(g, g11))
    scene.add(g12)
    scene.wait(1)
    t11 = MarkupText(Span(f"{prev} × ({prev}+1)", color="Teal")).scale(0.5)
    if f1 == f2:
        t12 = MarkupText(Span("Square of 5", color="Teal")).scale(0.5)
    else:
        t12 = MarkupText(Span("Product of final digits", color="Teal")).scale(0.5)
    t11.next_to(bl, LEFT)
    t12.next_to(br, RIGHT)
    scene.add(t11)
    scene.wait(2)
    scene.play(Transform(al, alf))
    scene.wait(2)
    scene.add(t12)
    scene.wait(2)    
    scene.play(Transform(ar, arf))
    scene.wait(2)
    #scene.play(FadeOut(g[1]))
    #scene.play(g12.animate.next_to(g[0], RIGHT, aligned_edge=UP))
    scene.play(FadeOut(g, g12, t11, t12))
    scene.wait(2)
    g2  = ShowOp(scene, snum, snum2, "×", ans, play=False)
    #scene.remove(g12)
    scene.play(Transform(ga, g2))
    scene.wait(wait)
    if fade:
        scene.play(FadeOut(ga, gc))
    return ga

def EkadhikenaMult(scene, num, num2, wait=5, fade=True):
    snum = str(num)
    inum = int(num)
    sprev = snum[:-1]
    fin = int(snum[-1])
    prev = int(sprev)
    snum2 = str(num2)
    sprev2 = snum2[:-1]
    inum2 = int(num2)
    fin2 = int(snum2[-1])

    assert (int(snum[-1]) + int(snum2[-1])) == 10, "Only works with numbers with last digits ending in 10"
    assert sprev == sprev2, "Only works with numbers with previous digits the same"

    ans = inum*inum2
    assert ans == prev*(prev+1)*100+fin*fin2

    text= [
        f"<span color='Turquoise'>Find the product of </span><span color='yellow'>{snum} and {snum2}</span>.",
#        f"Final digits are <span color='yellow'>{snum[-1]} and {snum2[-1]}</span>",
#        f"Their product is <span color='yellow'>{int(snum[-1])*int(snum2[-1])}</span>",
#       f"Pre-final Digit(s) are <span color='yellow'>{sprev}</span>",
#        f"One more than that is  <span color='yellow'>{prev+1}</span>",
#        f"As before, our answer begins with <span color='yellow'>{prev} times {prev+1}</span>",
#        f"It is now suffixed with <span color='yellow'>{int(snum[-1])*int(snum2[-1])}</span>",
#        f"Which leads us to <span color='yellow'>{inum*inum2}</span>."
    ]
    Explanation(scene, text, font='Cambria Math', aligned_edge=LEFT)
    scene.next_section()
    return EkCom(scene, snum, snum2, prev, fin, fin2, ans, wait, fade)


def findbase(num):
    ''' Nearest power of 10 '''
    snum = str(num)
    inum = int(num)
    hbase = 10**len(snum)
    lbase = 10**(len(snum)-1)
    return hbase if (hbase - inum) < hbase/2 else lbase


def YavadunamMult(scene, num1, num2, wait=5, fade=True, base=None, pretend_base=None):
    snum1 = str(num1)
    inum1 = int(num1)
    snum2 = str(num2)
    inum2 = int(num2)
    if base is None:
        base = findbase(num1)  # Nearest power of 10
        assert findbase(num2) == base, "{num1} and {num2} seem to be near different bases, force one by using base="
    if pretend_base is not None:
        pbase = pretend_base
    else:
        pbase = base
    diff1 = (pbase - inum1)  # Difference from that
    diff2 = (pbase - inum2)  # Difference from that
    ndig = len(str(base))-1   # Number of zeros in base

    rans = diff1 * diff2  # Right part of answer, has ndig digits
    lans = inum1 - diff2  # Left part of answer - number + diff from base 
    
    negp1 = (diff1 > 0)     # Are we below base?
    dirs1 = " - " if negp1 else " + "
    bdiff1 = "less than" if negp1 else "greater than"

    negp2 = (diff2 > 0)     # Are we below base?
    dirs2 = " - " if negp2 else " + "
    bdiff2 = "less than" if negp2 else "greater than"

    ans = inum1*inum2
    assert ans == lans * pbase/base * 10**ndig + rans, f" {ans} != {lans * pbase/base * 10**ndig + rans}, {base, pbase, diff, lans, ndig, rans}"
    
    text= [
        f"<span color='Turquoise'>Find the product of </span><span color='yellow'>{snum1}</span> and <span color='yellow'>{snum2}</span>.",
#        "1.  The nearest power of 10 is: " + Span(str(base),color='red') + " with " + Span(str(ndig), color='green') + " zeros",
#        f"2. <span color='yellow'>{snum1}</span> and <span color='yellow'>{snum2}</span> are " + Span(str(abs(diff1)), color='orange') + f" {bdiff1} and " + Span(str(abs(diff2)), color='orange') +  f" {bdiff2} the base " + Span(str(base),color='red'),
#        "3.  The right part of the answer is " + Span(f"{abs(diff1)} * {abs(diff2)}", color='orange') + " = " + Span(str(rans).zfill(ndig), color='yellow'),
#        "4.  The left part of the answer is " + Span(snum1, color='yellow') + dirs1 + Span(str(abs(diff2)), color='orange') + " = " + Span(lans, color='yellow'),
#        ".. The left part of the answer can also be written as " + Span(snum2, color='yellow') + dirs2 + Span(str(abs(diff1)), color='orange') + " = " + Span(lans, color='yellow'),
#        f"5. Putting them together, <span color='yellow'>{snum1}×{snum2}</span> = " + Span(ans, color='yellow')
    ]
    
    Explanation(scene, text, font='Cambria Math', aligned_edge=LEFT)
    scene.next_section()
    return YCom(scene, snum1, snum2, base, pbase, negp1, negp2, abs(diff1), abs(diff2), rans, lans, ans, ndig, wait, fade)


def YavadunamSquare(scene, num, wait=5, fade=True, base=None, pretend_base=None):
    snum = str(num)
    inum = int(num)
    if base is None:
        base = findbase(num)  # Nearest power of 10
    if pretend_base is not None:
        pbase = pretend_base
    else:
        pbase = base
    diff = (pbase - inum)  # Difference from that
    negp = (diff > 0)     # Are we below base?
    ndig = len(str(base))-1   # Number of zeros in base

    rans = diff **2  # Right part of answer, has ndig digits
    lans = inum - diff  # Left part of answer - number + diff from base 
    
    dirs = " - " if negp else " + "
    bdiff = "less than" if negp else "greater than"

    ans = inum**2
    assert ans == lans * pbase/base * 10**ndig + rans, f" {ans} != {lans * pbase/base * 10**ndig + rans}, {base, pbase, diff, lans, ndig, rans}"
    
    text= [
        f"<span color='Turquoise'>Find the square of </span><span color='yellow'>{snum}</span>.",
 #       "1.  The nearest power of 10 is: " + Span(str(base),color='red') + " with " + Span(str(ndig), color='green') + " zeros",
 #       f"2. <span color='yellow'>{snum}</span> is " + Span(str(abs(diff)), color='orange') + f" {bdiff} the base " + Span(str(base),color='red'),
 #       "3.  The right part of the answer is " + Span(str(abs(diff)), color='orange') + "² = " + Span(str(rans).zfill(ndig), color='yellow'),
 #       "4.  The left part of the answer is " + Span(snum, color='yellow') + dirs + Span(str(abs(diff)), color='orange') + " = " + Span(lans, color='yellow'),
 #       f"5. Putting them together: <span color='yellow'>{snum}</span>² = "  + Span(ans, color='yellow')
    ]
    
    Explanation(scene, text, font='Cambria Math', aligned_edge=LEFT)
    scene.next_section()
    return YCom(scene, snum, snum, base, pbase, negp, negp, abs(diff), abs(diff), rans, lans, ans, ndig, wait, fade)

def YCom(scene, snum, snum2, base, pbase, negp1, negp2, diff, diff2,  rans, lans, ans, ndig, wait, fade):
    g   = ShowOp(scene, snum, snum2, "×", "?", wait=1, fade=False)

    factor = pbase/base
    if factor>1:
        factor = int(factor)
        
    if pbase != base:
        tb = MarkupText(f"Pretend base is <span color='red'>{pbase}</span>, which is {factor} times  <span color='red'>{base}</span>", color="Turquoise", font='Cambria Math').scale(0.75)
    else:
        tb = MarkupText(f"Nearest base is <span color='red'>{base}</span>", color="Turquoise", font='Cambria Math')
        
    if negp1:
        g1 = ShowOp(scene, pbase, snum, "-", diff, play=False)
    else:
        g1 = ShowOp(scene, snum, pbase, "-", diff, play=False)
    if negp2:
        g12 = ShowOp(scene, pbase, snum2, "-", diff2, play=False)
    else:
        g12 = ShowOp(scene, snum2, pbase, "-", diff2, play=False)

    op = "-" if negp2 else "+"
    g2 = ShowOp(scene, snum, diff2, op, lans, play=False)
    op2 = "-" if negp1 else "+"
    g22 = ShowOp(scene, snum2, diff, op2, lans, play=False)
    g3 = ShowOp(scene, diff, diff2, "×", str(rans).zfill(ndig), play=False)
    g4  = ShowOp(scene, snum, snum2, "×", ans, play=False)

    ar = Text("_" * ndig, color='yellow').scale(1.2)
    arf = Text(str(rans).zfill(ndig), color='yellow', font='Cambria Math').scale(1.2)
    al = Text("_" * len(snum), color='yellow').scale(1.2)
    alf = Text(str(lans), color='yellow', font='Cambria Math').scale(1.2)
    if pbase != base:
        s_lans = lans*factor
        if isinstance(s_lans, float) and s_lans.is_integer():
            s_lans = int(s_lans) 
        alf2 = Text(str(s_lans), color='yellow', font='Cambria Math').scale(1.2)
        g23 = ShowOp(scene, lans, factor, "×", s_lans, play=False)
    br = SurroundingRectangle(ar, buff=0.5)
    bl = SurroundingRectangle(al, buff=0.5)
    ga = VGroup(VGroup(al, bl), VGroup(ar, br)).arrange(RIGHT)    

    ga.move_to(DOWN*2)
    g.next_to(ga[0], UP)
    alf.next_to(al, ORIGIN)
    arf.next_to(ar, ORIGIN)
    g2.next_to(ga[0], UP)
    g22.next_to(ga[0], UP)
    g1.next_to(ga[1], UP)
    g12.next_to(g1, ORIGIN, aligned_edge=RIGHT)
    g3.next_to(g1, ORIGIN, aligned_edge=RIGHT)

    scene.play(g.animate.move_to(LEFT*4))
    scene.wait(1)
    scene.add(tb.next_to(g, UP*3, aligned_edge=LEFT))
    scene.wait(2)
    scene.add(ga)
    scene.wait(3)
    scene.add(g1)
    scene.wait(3)
    if diff != diff2:
        scene.play(Transform(g1, g12))
        scene.wait(3)
    scene.play(Transform(g1, g3))
    scene.wait(3)
    scene.play(Transform(ar, arf))
    scene.wait(2)
    #scene.play(Transform(g, g2))
    scene.add(g2)
    scene.wait(3)
    if diff != diff2:
        scene.play(Transform(g2, g22))
        scene.wait()
    scene.play(Transform(al, alf))
    scene.wait(2)
    if pbase != base:
        g23.next_to(ga[0], UP)
        scene.play(Transform(g2, g23))
        scene.wait(4)
        alf2.next_to(al, ORIGIN)
        scene.play(Transform(al, alf2))
        scene.wait(4)
    scene.play(FadeOut(g2, g1))
    scene.wait(2)
    scene.remove(g1, g3)
    scene.play(Transform(ga, g4))
    scene.wait(wait)
    if fade:
        scene.play(FadeOut(ga, g, tb))
    return ga


def by12to19(scene, num, guNaka, wait=5, fade=True, scale=0.3, move=(3, 6)):
    snum = "0" + str(num) + "0"
    numdig = len(snum)
    n = numdig - 1
    ld = str(guNaka)[-1]

    title = DisplayText(scene, Span("Examples", color="Turquoise"), scale=0.8, wait=0, move=(-3, -4), fade=False)

    qs = ShowOp(scene, num, guNaka, "×", "?", move=(0, 0), play=False)
    qs.move_to(LEFT * 3)
    scene.add(qs)
    scene.wait(1)
    scene.next_section()

    numdig = len(snum)
    n = numdig - 1
    i = 0

    # numg = []
    # while i <= n:
    #    dig1 = str(snum[i])
    #    numg.append(dig1)
    #    i = i + 1
    numg = [s for s in snum]

    t = DisplayText(scene, Span("1.Add zeros at both ends of the number.", color="Turquoise"), scale=0.5, wait=0,
                    move=(-2, 3),
                    fade=False, font='Cambria Math')

    el = [MarkupText(x, font_size=130) for x in numg]
    eg = VGroup(*el).scale(scale).arrange(RIGHT * 2, aligned_edge=ORIGIN)
    eg.move_to(UP + RIGHT * 4)

    for _el in el:
        scene.play(AddTextLetterByLetter(_el, time_per_letter=1))
    scene.wait(3)

    # sp = []
    # j = n
    # while j > 0:
    #    sum = int(snum[j])
    #    j = j-1
    #    sum = sum + int(snum[j])
    #    sp.append(str(sum))
    sp = [str(int(snum[i]) * int(ld) + int(snum[i + 1])) for i in reversed(range(len(snum) - 1))]

    scene.play(FadeOut(t))
    t = DisplayText(scene, Span("2. Penultimate digit x " + ld + " is added with final digit", color="Turquoise"),
                    scale=0.5, wait=0, move=(-2.4, 3),
                    fade=False, font='Cambria Math')
    t4 = DisplayText(scene, Span("This makes each digit of answer.",
                                 color="Turquoise"),
                     scale=0.5, wait=0, move=(-2, 3),
                     fade=False, font='Cambria Math')

    spl = [MarkupText(x, font_size=130) for x in sp]
    spg = VGroup(*spl).scale(scale).arrange(LEFT * 2, aligned_edge=ORIGIN)
    spg.next_to(eg, DOWN)

    """
    j = n
    for _spl in spl:
        scene.play(eg[j].animate.set_color(YELLOW))
        j = j - 1
        scene.play(eg[j].animate.set_color(YELLOW))
        scene.play(AddTextLetterByLetter(_spl, time_per_letter=1))
        scene.play(eg[j + 1].animate.set_color(RED))
    scene.wait(1)
    """

    splen = len(sp)
    carry = 0
    fp = []
    cy_found = False

    for i in range(0, splen, 1):
        if int(carry) > 0:
            cy_found = True
            curr_dig = int(sp[i]) + int(carry)
        else:
            curr_dig = int(sp[i])
            cy_found = True

        curr_dig_len = len(str(curr_dig))
        str_currDig = str(curr_dig)

        if i < splen - 1:
            unitdig = str_currDig[curr_dig_len - 1]
        else:
            unitdig = curr_dig

        if curr_dig_len > 1:
            carry = str_currDig[:curr_dig_len - 1]
        else:
            carry = 0

        fp.append(str(unitdig))

    fpl = [MarkupText(x, font_size=130) for x in fp]
    fpg = VGroup(*fpl).scale(scale).arrange(LEFT * 2, aligned_edge=ORIGIN)
    fpg.next_to(spg, DOWN)

    j = 0
    k = n
    for _fpl in fpl:
        scene.play(eg[k].animate.set_color(YELLOW_C))
        scene.play(eg[k - 1].animate.set_color(PURE_RED))
        scene.play(AddTextLetterByLetter(_fpl, time_per_letter=1))
        scene.play(fpg[j].animate.set_color(ORANGE))
        scene.wait(1)
        scene.play(eg[k].animate.set_color(DARKER_GRAY))
        j = j + 1
        k = k - 1
        scene.wait(2)
    scene.wait(2)

    g2 = ShowOp(scene, num, guNaka, "×", int(num) * guNaka, move=(0, 0), play=False)
    g2.next_to(qs, ORIGIN, aligned_edge=RIGHT)
    scene.play(Transform(qs, g2))
    scene.wait(1)

    scene.play(FadeOut(qs, eg, g2, fpg, title, t, t4))
    scene.wait(2)
    return g2


def by11(scene, num, wait=5, fade=True, scale=0.3, move=(3, 6)):
    snum = "0" + str(num) + "0"
    numdig = len(snum)
    n = numdig - 1

    title = DisplayText(scene, Span("Examples", color="Turquoise"), scale=0.8, wait=0, move=(-3, -4), fade=False)

    qs = ShowOp(scene, num, 11, "×", "?", move=(0, 0), play=False, wait=1)
    qs.move_to(LEFT * 3)
    scene.add(qs)
    scene.wait(2)
    scene.next_section()

    numdig = len(snum)
    n = numdig - 1
    i = 0

    # numg = []
    # while i <= n:
    #    dig1 = str(snum[i])
    #    numg.append(dig1)
    #    i = i + 1
    numg = [s for s in snum]

    t = DisplayText(scene, Span("1.Add zeros at both ends of the number.", color="Turquoise"), scale=0.5, wait=1,
                    move=(-2, 3),
                    fade=False, font='Cambria Math')

    el = [MarkupText(x, font_size=130) for x in numg]
    eg = VGroup(*el).scale(scale).arrange(RIGHT * 2, aligned_edge=ORIGIN)
    eg.move_to(UP + RIGHT * 4)

    for _el in el:
        scene.play(AddTextLetterByLetter(_el, time_per_letter=1))
    scene.wait(2)

    # sp = []
    # j = n
    # while j > 0:
    #    sum = int(snum[j])
    #    j = j-1
    #    sum = sum + int(snum[j])
    #    sp.append(str(sum))
    sp = [str(int(snum[i]) + int(snum[i + 1])) for i in reversed(range(len(snum) - 1))]

    scene.play(FadeOut(t))
    t = DisplayText(scene, Span("2. Add the last two digits to get one digit of the Answer.", color="Turquoise"),
                    scale=0.5, wait=1, move=(-2, 3),
                    fade=False, font='Cambria Math')

    spl = [MarkupText(x, font_size=130) for x in sp]
    spg = VGroup(*spl).scale(scale).arrange(LEFT * 2, aligned_edge=ORIGIN)
    spg.next_to(eg, DOWN)

    j = n
    for _spl in spl:
        scene.play(eg[j].animate.set_color(YELLOW))
        j = j - 1
        scene.play(eg[j].animate.set_color(YELLOW))
        scene.play(AddTextLetterByLetter(_spl, time_per_letter=1))
        scene.play(eg[j + 1].animate.set_color(RED))
    scene.wait(2)

    splen = len(sp)
    carry = 0
    fp = []
    cy_found = False
    for i in range(0, splen, 1):
        if int(carry) > 0:
            cy_found = True
            curr_dig = int(sp[i]) + int(carry)
        else:
            curr_dig = int(sp[i])

        curr_dig_len = len(str(curr_dig))
        str_currDig = str(curr_dig)
        unitdig = str_currDig[curr_dig_len - 1]

        if curr_dig_len > 1:
            carry = str_currDig[:curr_dig_len - 1]
        fp.append(str(unitdig))

    if cy_found == True:

        scene.play(FadeOut(t))
        t1 = DisplayText(scene, Span("3. Retain only the unit digit in each place...", color="Turquoise"),
                         scale=0.5, wait=1, move=(-2.4, 3),
                         fade=False, font='Cambria Math')
        t2 = DisplayText(scene, Span("...  other digits are added to the digits to its left.",
                                     color="Turquoise"),
                         scale=0.5, wait=1, move=(-2, 3),
                         fade=False, font='Cambria Math')

        t3 = DisplayText(scene, Span("With more practice, we can do this directly in 2nd step",
                                     color="Turquoise"),
                         scale=0.5, wait=1, move=(2, 3),
                         fade=False, font='Cambria Math')

        fpl = [MarkupText(x, font_size=130) for x in fp]
        fpg = VGroup(*fpl).scale(scale).arrange(LEFT * 2, aligned_edge=ORIGIN)
        fpg.next_to(spg, DOWN)

        j = 0
        for _fpl in fpl:
            scene.play(spg[j].animate.set_color(YELLOW))
            scene.play(AddTextLetterByLetter(_fpl, time_per_letter=1))
            scene.wait(1)
            scene.play(spg[j].animate.set_color(WHITE))
            j = j + 1
            scene.wait(2)

    scene.wait(2)

    if cy_found == True:
        scene.play(FadeOut(t1, t2, t3))

    g2 = ShowOp(scene, num, 11, "×", int(num) * 11, move=(0, 0), play=False, wait=1)
    g2.move_to(LEFT * 2)
    scene.play(Transform(qs, g2))
    scene.wait(3)

    if cy_found == True:
        scene.play(FadeOut(fpg))
    else:
        scene.play(FadeOut(t))

    scene.play(FadeOut(qs, eg, spg, g2, title))

    scene.wait(2)
    return g2


class Ekadhikena(Scene):
    ''' Ekadhikena Purvena '''
    def construct(self):
        # Title
        Title(self, "एकाधिकेन पूर्वेण", "Squares and Products with Ekadhikena ",
              move=(3, 5), wait=2)
        self.next_section()

        # Introduction

        text = ["<span color='Turquoise'>Simple multiplication and squaring</span>",
                "Before we introduce a general method for multiplication",
                "We will look at special cases which are easier."]

        Explanation(self, text, aligned_edge=LEFT)
        self.next_section()

        # Introduction
        text = ["<span color='Turquoise'>Our first method works for</span> ",
                "1. Squares of numbers ending in 5.",
                "2. Products of numbers with last digits adding to 10   ",
                "      and other digits identical."]
        Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)
        self.next_section()

        # Sutra Scene
        t0 = "एकाधिकेन पूर्वेण"
        t1 = ["एकाधिकेन", "पूर्वेण"]
        t2 = ["<span size='smaller'>By one more than</span>", "<span size='smaller'>the previous</span>"]
        Sutra(self, t0, t1, t2, wait=3, scale=0.75, move=None, fade=True, font='Cambria Math')
        self.next_section()

        EkadhikenaSquare(self, 35)
        self.next_section()

        EkadhikenaSquare(self, 85)
        self.next_section()

        # Introduction
        text = ["<span color='Turquoise'>We can use this to multiply numbers that</span>",
                "1. have identical digits barring the final one.",
                "2. have their final digits adding up to 10."]
        Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)
        self.next_section()
        
        # Sutra Scene
        t0 = "अन्त्ययोर्दशकेऽपि"
        t1 = ["अन्त्ययोः", "दशके अपि"]
        t2 = ["<span size='smaller'>When the last</span>", "<span size='smaller'>sum to 10</span>"]
        Sutra(self, t0, t1, t2, wait=3, scale=0.75, move=None, fade=True, font='Cambria Math')
        self.next_section()
        
        EkadhikenaMult(self, 33, 37)
        self.next_section()
        
        EkadhikenaMult(self, 72, 78)
        self.next_section()
        self.wait(5)

class Yavadunam(Scene):
    ''' Multiplication with Yavadunam '''
    def construct(self):
        # Title
        Title(self, "यावदूनम्", "Squares and Products with Yavadunam",
              move=(3, 5), wait=2)
        self.next_section()

        # Introduction
        text = [Span("This method works for", color='Turquoise'),
                "1. Squares  of numbers near a power of 10. ",
                "2. Products of numbers near a power of 10. ",
                ]
        e = Explanation(self, text, font='Cambria Math', wait=0, fade=False, aligned_edge=LEFT)
        t = DisplayText(self, Span("Powers of 10 are 10, 100, 1000, etc.", size='x-small', color='Turquoise'), font='Cambria Math',
                        scale=0.75, move=(1.5, 1.5), wait=0, fade=False)
        self.wait(5)
        self.play(FadeOut(e, t))
        self.next_section()


        # Sutra Scene
        t0 = Span("यावदूनम् तावदूनीकृत्य वर्गं च योजयेत्")
        t1 = [Span("यावद् ऊनम् तावद् ऊनीकृत्य"), Span("वर्गं च योजयेत्")]
        t2 = [Span("Reduce further by the difference from the base"),
              Span("and append the square")]
        Sutra(self, t0, t1, t2, wait=3, scale=0.65, move=None, fade=True, font='Cambria Math', dir1=DOWN, dir2=DOWN)
        self.next_section()

        text= [
            f"<span color='Turquoise'>To find the square of a number </span><span color='yellow'>n</span>",
            "1. Find the nearest base <span color='red'>b</span>, and note its number of zeros <span color='green'>k</span>.",
            "2. Note if <span color='yellow'>n</span> is above or below <span color='red'>b</span>, and note the difference <span color='orange'>d</span>.",
            "3. We then divide the answer into two parts - left and right.",
            "4. The right part of the answer is <span color='orange'>d²</span>, padded to " + Span("k", color='green') + " digits.",
            "5. The left part of the answer is,",
            "..  if n less than b    ⇒ <span color='yellow'>n-</span><span color='orange'>d</span>.",
            "..  if n greater than b ⇒ <span color='yellow'>n+</span><span color='orange'>d</span>.",
            "6. Combine the left and right parts."
        ]
    
        Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)

        YavadunamSquare(self, 94)
        self.next_section()

        YavadunamSquare(self, 1003)
        self.next_section()

        YavadunamSquare(self, 89) 
        self.next_section
        
        text= [
            f"<span color='Turquoise'>To find the product of two numbers </span><span color='yellow'>n1</span> and <span color='yellow'>n2</span>.",
            "1. Find the nearest base <span color='red'>b</span>, and note its number of zeros <span color='green'>k</span>.",
            "2. Note if <span color='yellow'>n1</span> and <span color='yellow'>n2</span> are above or below <span color='red'>b</span>.",
            "3. Note the differences <span color='orange'>d1</span> and <span color='orange'>d2</span>.",
            "4. We then divide the answer into two parts - left and right.",
            "5. The right part of the answer is <span color='orange'>d1×d2</span>, padded to " + Span("k", color='green') + " digits.",
            "6. The left part of the answer is, ",
            "..  if n1 less than b    ⇒ <span color='yellow'>n1-</span><span color='orange'>d2</span>.",
            "..  if n1 greater than b ⇒ <span color='yellow'>n1+</span><span color='orange'>d2</span>.",
            "7. Combine the left and right parts."
        ]
    
        Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)

        YavadunamMult(self, 92, 97)
        self.next_section()

        YavadunamMult(self, 104, 110)
        self.next_section()

        YavadunamMult(self, 997, 988)
        self.next_section()

        YavadunamMult(self, 88, 89) 
        self.next_section()
        
        self.wait(5)

class Anurupyena(Scene):
    ''' Multiplication with Anurupyena '''
    def construct(self):
        # Title
        Title(self, "आनुरूप्येण", "Squares and Products with Anurupyena",
              move=(3, 5), wait=2)
        self.next_section()

        # Introduction
        text = [Span("The Yavadunam method works for", color='Turquoise'),
                "1. Squares  of numbers near a power of 10. ",
                "2. Products of numbers near a power of 10. ",
                "Wouldn't it be nice if we could extend it to other bases?",
                Span("The Anurupyena method extends Yavadunam to do just that!", color='Turquoise')
                ]
        e = Explanation(self, text, font='Cambria Math', wait=0, fade=False, aligned_edge=LEFT)
        self.wait(5)
        self.play(FadeOut(e))
        self.next_section()

        # Sutra Scene
        t0 = Span("आनुरूप्येण")
        t1 = [Span("आनुरूप्येण")]
        t2 = [Span("Proportionally")]
        Sutra(self, t0, t1, t2, wait=3, scale=1, move=None, fade=True, font='Cambria Math', dir1=DOWN, dir2=DOWN)
        self.next_section()

        text= [
            f"<span color='Turquoise'>To find the square of a number </span><span color='yellow'>n</span>,",
            "1. Find the nearest convenient pretend base <span color='red'>p</span>,",
            "2. Note the nearest power of 10, <span color='red'>b</span> that <span color='red'>p</span> is a convenient factor or multiple of,",
            "3. Note their ratio as <span color='turquoise'>f</span>,",
            "4. Execute the Yavadunam method using the pretend base <span color='red'>p</span>,",
            "5. Scale the left half (only) by <span color='turquoise'>f</span> before merging.",
        ]
    
        Explanation(self, text, font='Cambria Math', scale=0.5, aligned_edge=LEFT)

        YavadunamSquare(self, 44, pretend_base=50, base=100)
        self.next_section()

        YavadunamSquare(self, 503, pretend_base=500, base=1000)
        self.next_section()
        
        YavadunamSquare(self, 208, pretend_base=200, base=100) 
        self.next_section
        
        text= [
            f"<span color='Turquoise'>A similar strategy works for products as well</span>",
        ]
    
        Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)

        YavadunamMult(self, 42, 46, pretend_base=50, base=100)
        self.next_section()

        YavadunamMult(self, 504, 503, pretend_base=500, base=1000)
        self.next_section()

        YavadunamMult(self, 34, 35, pretend_base=30, base=10)
        self.next_section()
        
        self.wait(5)


class Antyayoreva(Scene):
    ''' Antyayo eva '''

    def construct(self):
        # Title

        Title(self, "अन्त्ययोरेव", "Multiplication by 11 ", move=(3, 5), wait=2)
        self.next_section()

        # Introduction
        text = ["<span color='TURQUOISE'>Multiply any number by 11</span>",
                "by just adding the digits."]

        Explanation(self, text, aligned_edge=LEFT,wait=1)
        self.next_section()

        # Sutra Scene
        t0 = "अन्त्ययोरेव"
        t1 = ["अन्त्ययोः", "एव"]
        t2 = ["<span size='smaller'>(Sum of) last digits</span>", "<span size='smaller'>only</span>"]
        Sutra(self, t0, t1, t2, wait=0, scale=1, move=None, fade=True)
        self.next_section()

        text = [
            f"<span color='TURQUOISE'>To multiply any number by 11</span>",
            f"Add zeros at both ends of the number.",
            f"At each step,",
            f"1) Add the last two digits to get one digit of the answer.",
            f"2) Drop the right digit of the number",
            "repeat until no digits remain."]

        Explanation(self, text, font='Cambria Math', aligned_edge=LEFT, wait=2)
        self.next_section()

        by11(self, 123)
        self.next_section()

        by11(self, 489)
        self.next_section()

        by11(self, 7485)
        self.next_section()

        
class Sopantyadvayamantyam(Scene):
    ''' Antyayo eva '''

    def construct(self):
        # Title

        Title(self, "सोपान्त्यद्वयमन्त्यम्", "Multiplication by 12 ", move=(3, 5), wait=3)
        self.next_section()

        # Introduction
        text = ["<span color='TURQUOISE'>To multiply any number by 12,</span>",
                "by doubling and adding the digits"]

        Explanation(self, text,font='Cambria Math', aligned_edge=LEFT, wait=2)
        self.next_section()

        # Sutra Scene
        t0 = "सोपान्त्यद्वयमन्त्यम्"
        t1 = ["उपान्त्यद्वयेन सह"," अन्त्यम्"]
        t2 = ["<span size='smaller'>Twice the Penultimate </span>", "<span size='smaller'>with Final</span>"]
        Sutra(self, t0, t1, t2, wait=3, scale=1, move=None, fade=True, font='Cambria Math')
        self.next_section()

        text = [
            f"<span color='TURQUOISE'>To multiply any number by 12</span>",
            f"Add zeros at both ends of the number.",
            f"At each step,",
            f"1) Multiply the penultimate digit by 2 ",
            f"... and add it with the final digit. ",
            f"2) Drop the right digit of the number and ",
            f"... repeat until no digits remain."]

        Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)
        self.next_section()

        by12to19(self, 182, 12)
        self.next_section()

        by12to19(self,534,12)
        self.next_section()

        by12to19(self, 1363,12)
        self.next_section()

        text = [
            f"<span color='TURQUOISE'>Do more practice and we can do this mentally. </span>",
            f"<span color='ORANGE'>We can extend this sutra where multiplier is any number from</span> <span color='RED'> 13-19 </span>",
            f"Note the last digit of the multiplier as <span color='RED'> n </span> and at each step,",
            f"1 Multiply the penultimate digit by <span color='RED'> n </span> ",
            f"... and add it with the final digit. ",
            f"2) Drop the right digit of the number and ",
            f"... repeat until no digits remain."]

        Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)
        self.next_section()

        by12to19(self, 231, 14)
        self.next_section()

        by12to19(self, 725, 17)
        self.next_section()

class Urdhvatiryagbhyam(Scene):
    ''' Urdhvatiryagbhyam Multiplication '''
    def construct(self):
        # Title
        Title(self, "ऊर्ध्वतिर्यग्भ्याम्", "Single-line Multiplication",
              move=(3, 5), wait=2)
        self.next_section()

        text = ["What if the numbers to be multiplied do not match",
                "any of the special sutras seen so far?",
                "We would like a general method",
                "that works for any numbers!"]

        Explanation(self, text, aligned_edge=LEFT)
        self.next_section()

        # Introduction
        text = ["<span color='Turquoise'>A General Method for Multiplication,</span>",
                "which works for all cases,",
                "requires only a single line",
                "and can be performed mentally!"]

        Explanation(self, text, aligned_edge=LEFT)
        self.next_section()

        ut(self, 12, 34, show_carry=True, explain=False)
        self.next_section

        text = ["<span color='Turquoise'>How did we do this?</span> ",
                ""]
        Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)
        self.next_section()

        # Sutra Scene
        t0 = "ऊर्ध्वतिर्यग्भ्याम्"
        t1 = ["ऊर्ध्व-", "तिर्यग्भ्याम्"]
        t2 = ["<span size='smaller'>By straight</span>",  "<span size='smaller'>and across</span>"]
        Sutra(self, t0, t1, t2, wait=0, scale=1, move=None, fade=True, font='Cambria Math')
        self.next_section()

        text = ["This method is based on a group of <span color='Turquoise'>patterns</span>.",
                "Each pattern of <span color='Yellow'>straight</span> and  <span color='Yellow'>across</span> lines",
                "gives us a collection of pairs of numbers.",
                "Each of those  <span color='Turquoise'>pairs</span> is  <span color='Yellow'>multiplied</span>,",
                "And then the  <span color='Turquoise'>products</span> are  <span color='Yellow'>added</span>.",
                "One digit of this  <span color='Turquoise'>partial product</span> becomes a  <span color='Yellow'>digit of the answer</span>.",
                "<span color='Turquoise'>Extra digits</span> become  <span color='Yellow'>carries</span> into the next digit,",
                "and are <span color='Turquoise'>added</span> to the  <span color='Yellow'>next partial product</span>.",
                "All of this can be done mentally."]

        Explanation(self, text, aligned_edge=LEFT)
        self.next_section()
        
        
        text = ["<span color='Turquoise'>Two digit multiplication patterns</span>."]
        Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)
        self.next_section()

        utpatterns(self, 2)
        self.next_section()
        
        
        text = ["<span color='Turquoise'>A few two-digit examples should make things clearer. </span>"]
        Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)
        
        
        ut(self, 12, 24, move=(0, -2))
        self.next_section

        ut(self, 34, 57, move=(0, -2))
        self.next_section

        text = ["<span color='Turquoise'>Three digit multiplication patterns</span>."]
        Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)
        self.next_section()

        utpatterns(self, 3)
        self.next_section()

        text = ["<span color='Turquoise'>Three-digit examples</span>."]

        Explanation(self, text, aligned_edge=LEFT)
        self.next_section()

        
        ut(self, 123, 456, move=(0, -2))
        self.next_section

        ut(self, 534, 645, move=(0, -2))
        self.next_section

        
        text = ["As you begin practicing this method,",
                "you can write out each partial product.",
                "With practice, you should be able to calculate them mentally.",
                "Once you are comfortable calculating partial products mentally,",
                "you should aim to write down just the answer digits,",
                "and note the carries below and to the left.",
                "This means multiplication happens in a single line!"]
        
        text = [Span(t, color='Turquoise') for t in text]
        Explanation(self, text, scale=0.65, aligned_edge=LEFT)
        self.next_section()

        text = ["Remember to check your answers",
                "using the digitsum method as well.",
                "This will give you confidence to multiply mentally."]
        text = [Span(t, color='Turquoise') for t in text]
        Explanation(self, text, scale=0.65, aligned_edge=LEFT)
        self.next_section()
        self.wait(5)

class Urdhvatiryagbhyam_45(Scene):
    ''' Urdhvatiryagbhyam Multiplication for 4 and 5 digit numbers'''
    def construct(self):
        # Title
        Title(self, "ऊर्ध्वतिर्यग्भ्याम् 4/5", "4/5 digit Multiplication",
              move=(3, 5), wait=2)
        self.next_section()

        text = [
            "Taking another look at ऊर्ध्वतिर्यग्भ्याम्,",
            "Also known as तत्स्थ multiplication.",
            "Can we use ऊर्ध्वतिर्यग्भ्याम् for numbers",
            "with more than 3 digits?",
            "Yes we can!"]

        Explanation(self, text, aligned_edge=LEFT)
        self.next_section()
        
        text = ["<span color='Turquoise'>Four digit multiplication patterns</span>."]
        Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)
        self.next_section()

        utpatterns(self, 4)
        self.next_section()
        
        
        text = ["<span color='Turquoise'>Four digit examples</span>"]
        Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)
        
        
        ut(self, 4312, 2435, move=(0, -3))
        self.next_section()

        ut(self, 3457, 6312, move=(0, -3))
        self.next_section()

        text = ["<span color='Turquoise'>Five digit multiplication patterns</span>."]
        Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)
        self.next_section()

        utpatterns(self, 5)
        self.next_section()

        text = ["<span color='Turquoise'>Five-digit examples</span>."]

        Explanation(self, text, aligned_edge=LEFT)
        self.next_section()

        
        ut(self, 12345, 87456, move=(0, -3))
        self.next_section
        
        text = ["With practice, four and five digit multiplication",
                "can be done mostly mentally too.",
                "Aim to write down just the answer digits,",
                "and note the carries below and to the left.",
                "This means multiplication happens in a single line!"]
        
        text = [Span(t, color='Turquoise') for t in text]
        Explanation(self, text, scale=0.65, aligned_edge=LEFT)
        self.next_section()

        
        text = ["These patterns can be extended to",
                "any number of digits, which means that",
                "numbers of any size can be multiplied this way."]
        
        text = [Span(t, color='Turquoise') for t in text]
        Explanation(self, text, scale=0.65, aligned_edge=LEFT)
        self.next_section()
        self.wait(5)

def utpatterns(scene, n, wait=3, d_wait=1):
    n1 = "1" * n
    n2 = "2" * n
    ut(scene, n1, n2, explain=False, show_res=False)

def ut(scene, sn1, sn2,  move=(0, 0), wait=3, d_wait=1, explain=True, show_res=True,
       show_carry=True, play=True, fade=True, oplen=0):
    ''' Urdhvatiryagbhyam helper function '''
    def _explain():
        ''' Step explanation '''
        # Get the ordinal right - ix comes in starting with 0
        _ord = {0: "1st", 1: "2nd", 2: "3rd"}
        ord = _ord[ix] if ix in _ord else f"{ix+1}th"
        etext = [f"The <span color='Turquoise'>{ord}</span> partial product is: <span color='Turquoise'>{_pp}</span>.",
                 ]
        if c_p:
            etext.append(f"<span color='Turquoise'>{_pp}</span> + <span color='Turquoise'>{c_p.text}</span> (prev. carry) =  <span color='Turquoise'>{pp}</span>.")
        if ix==(nit-1):
            etext.append(f"We retain <span color='yellow'>{pp}</span> as the rest of the answer.")
        else:
            etext.append(f"We retain <span color='yellow'>{d}</span> as a  digit of the answer.")
            if c:
                etext.append(f"<span color='yellow'>{c}</span> becomes the next carry.")

        el = [MarkupText(x, font="Cambria Math") for x in etext]
        eg = VGroup(*el).scale(0.5).arrange(DOWN, aligned_edge=LEFT).move_to(RIGHT*4)

        for _el in eg:
            scene.play(AddTextLetterByLetter(_el, time_per_letter=1))
        scene.wait(2)
        return eg
    
    sr = int(sn1)*int(sn2) # Result
    n = max(len(str(sn1)), len(str(sn2)))
    nit = 2*n-1
    sop = "×"
    # Zero fill multiplier/multiplicand as necessary
    n1 = MarkupText(str(sn1).zfill(n), font='Cambria Math').arrange(buff=0.5)
    n2 = MarkupText(str(sn2).zfill(n), font='Cambria Math').arrange(buff=0.5)
    op = MarkupText(str(sop), font='Cambria Math')
    res = MarkupText(str(sr), font='Cambria Math').arrange(buff=0.5)
    if oplen==0:
        oplen=res.width
    ln = Line(start=array([-1 * oplen, 0, 0]), end=array([0, 0, 0])).set_color(YELLOW)
    # First arrange as usual
    g1 = VGroup(n1, n2, ln, res).arrange(DOWN, aligned_edge=RIGHT)
    n1.next_to(n2, UP, buff=0.5, aligned_edge=RIGHT)  # Add some gap for ut lines
    g = VGroup(g1, op).arrange(RIGHT, aligned_edge=UP) # Final assembly
    g.move_to(UP * move[0] + RIGHT * move[1]) # move
    lr = len(str(sr)) # Length of result
    if play:
        scene.play(FadeIn(n1, n2, ln, op))
        lines = None
        show = [] # Lines to display
        cl = []
        c = 0
        c_p = None
        for ix in range(nit):
            x = res[-1-ix]  # Reversed
            # Display ixth urdhvatiryagbhyam pattern
            lines, show, pp = utlines(scene, ix, n1, n2, lines, show)
            n1.set_color(WHITE)
            n2.set_color(WHITE)
            # Only the digits relevant for this pattern are
            # shown in yellow
            for s in show:
                n1[s].set_color(YELLOW)
                n2[s].set_color(YELLOW)
            # Previous result digit turned back to White
            if show_res and (ix > 0):  
                res[lr-ix].set_color(WHITE)
            scene.wait(3)
            if c_p is not None:
                c_p.set_color(GREY)
            _pp = pp # For display
            pp += c  # Previous carry
            d = int(str(sr)[-1-ix])  # ixth digit of the answer
            c = (pp - d) // 10
            if explain:
               eg =  _explain()
            if show_res:
                # Add current result digit in Yellow
                scene.add(x.set_color(YELLOW))

            # Display carry down and to the left
            # Not done for the last step, because if there's a carry
            # it just becomes an extra digit directly
            if show_res and show_carry and c and (ix!=(nit-1)):
                ct = Text(str(c)).scale(0.7).next_to(x, DOWN*0.5+LEFT*0.5)
                scene.add(ct)
                c_p = ct
                cl.append(ct)
            # At the last step, display remaining digits of answer too
            if show_res and (ix==(nit-1)) and (lr>nit):
                scene.add(res[:(lr-nit)].set_color(YELLOW))
            scene.wait(d_wait)
            if explain:
                scene.play(FadeOut(eg))
        scene.remove(*lines)  # Remove last u line
        # Remove color emphasis
        n1.set_color(WHITE)
        n2.set_color(WHITE)
        if show_res:
            res.set_color(WHITE)
        if show_carry:
            scene.remove(*cl)
        if wait:
            scene.wait(wait)
        if fade:
            if show_res:
                scene.play(FadeOut(g))
            else:
                scene.play(FadeOut(n1, n2, ln, op))
    return g


def utlines(scene, ix, n1, n2, lines=None, show=[]):
    ''' Update and display connections for ixth urdhvatiryagbhyam pattern '''
    n = len(n1) # Length of inputs
    nit = 2*n-1  # Number of ut iterations
    # Initialize lines if required
    if lines is None:
        lines =  [Line(n2[i].get_top(), [n2[-1].get_top()[0], n1[-1].get_bottom()[1], n1[-1].get_bottom()[2]]).set_color(YELLOW) for i in range(n)]
    
    def _display(show):
        # list show is in the order of top vertices (eg: [5, 4, 3])
        # bottom vertices will be the same reversed (eg: [3, 4, 5])
        # We zip the two to get the connection iterator (eg [(3, 5), (4, 4), (5, 3)])
        cnxns = zip(reversed(show), show)
        for c in cnxns:
            # Update line connections to get each urdhvatiryagbhyam pattern
            lines[c[0]].put_start_and_end_on([n2[c[0]].get_top()[0], n2[c[0]].get_top()[1] + 0.05, n2[c[0]].get_top()[2]],
                                             [n2[c[1]].get_top()[0], n1[c[1]].get_bottom()[1] - 0.05, n1[c[1]].get_bottom()[2]])
            # This could have been (n2[c[0]].get_top(), [n2[c[1]].get_bottom())
            # However, we see some lines not looking "straight"

    def _pp(show):
        ''' Partial Product '''
        pp = 0
        cnxns = zip(reversed(show), show)
        for c in cnxns:
            pp += int(n2.text[c[0]]) * int(n1.text[c[1]])
        return pp
    
    if ix < n:
        # For the first n iterations, add one line, starting from the right
        scene.add(lines[n-1-ix])
        show.append(n-1-ix)  # Append added line to the show list
        # Update line display.
        # Connections will be modified based on the show list
        _display(show)
    elif ix < nit:
        # After the first n iterations
        rx = ix-n
        # Remove one line, starting from the first added
        # (Last line added never gets removed)
        scene.remove(lines[n-1-rx])  
        show.pop(0)  # Remove line from show list
        # Update line display
        # Connections will be modified based on the show list
        _display(show)
    pp = _pp(show)
    return lines, show, pp
  

class Samuccaya(Scene):
    def construct(self):
        # Title

        Title(self, "उत्तरपरिशोधनम्", "Checking Answers", move=(3, 5), wait=2)
        self.next_section()
        self.wait(2)

        # Introduction
        text = [Span("Verifying the results of", color='Turquoise'),
                "Addition, Subtraction, Multiplication, and Division.",
                ]
        e = Explanation(self, text, font='Cambria Math', wait=2, fade=True, aligned_edge=LEFT)
        #self.wait(2)
        #self.play(FadeOut(e))
        self.next_section()
        
       # Introduction
        text = ["Vedic Maths sutras help us calculate fast,",
                "but how do we know we have not made a calculation mistake?",
                "Calculation speed comes from confidence, and confidence is helped", 
                "by being able to check the answer we calculate!"
                ]
        e = Explanation(self, text, font='Cambria Math', wait=2, fade=True, aligned_edge=LEFT)
        #self.wait(2)
        #self.play(FadeOut(e))
        self.next_section()

        text = [
            f"<span color='TURQUOISE'>The <span color='PINK'>digitsum </span> technique helps us check our answers.</span>",
            f"<span color='TURQUOISE'>The <span color='PINK'>digitsum </span> or <span color='PINK'>समुच्चयः</span> of a number is the sum of its digits.</span>",
            f"<span color='TURQUOISE'>The digitsum of a number, also happens to be the <span color='ORANGE'>remainder</span>,</span>",
            f"<span color='TURQUOISE'>when <span color='ORANGE'>divided by 9,</span></span>",
            f"<span color='TURQUOISE'>and hence it is also called <span color='ORANGE'>नवशेषः/navashesha</span></span>.",
              ]

        e = Explanation(self, text, wait=2, aligned_edge=LEFT)
        #self.wait(2)
        self.next_section()

        calcDigitsum(self, "257")
        self.next_section()

        calcDigitsum(self, "5364")
        self.next_section()

        # Sutra Scene
        t0 = Span("गुणितसमुच्चयः समुच्चयगुणितः")
        t1 = [Span("गुणितसमुच्चयः"), Span("समुच्चयगुणितः")]
        t2 = [Span("The digitsum of the product is "),
              Span("The product of the  digitsums")]
        Sutra(self, t0, t1, t2, wait=0, scale=0.65, move=None, fade=True, font='Cambria Math', dir1=DOWN, dir2=DOWN)
        self.wait(2)
        self.next_section()

        digitsumcheck(self, "998", "996", "×", "994008")
        self.next_section()
        
        digitsumcheck(self, "232", "426", "×", "98832")
        self.next_section()

        digitsumcheck(self, "98", "96", "×", "9608")
        self.next_section()


def dsum(s):
    n = int(s)
    while n>9:
        n = sum([int(s) for s in str(n)])
    return n

def digitsumcheck(scene, num1, num2, opr, ans, wait=5, fade=True, scale=0.3, move=(3, 6)):
    ''' Digitsum Check '''
    def _op(d1, d2):
        if opr == "×":
            return d1*d2
        else:
            return eval(f"{d1}{opr}{d2}")

    title = DisplayText(scene, Span("Check", color="Turquoise"), scale=0.8, wait=0, move=(-3, -4), fade=False)
    g = ShowOp(scene, num1, num2, opr, ans, move=(0, -2), wait=2, fade=False)
    d1 = dsum(num1)
    d2 = dsum(num2)
    d3 = dsum(ans)
    td3 = Text(str(d3), font="Cambria Math").next_to(g, DOWN)
    cans = _op(d1, d2)
    tdans = dsum(cans)
    g1 = ShowOp(scene, str(d1), str(d2), opr, cans, move=(0, 2), wait=0, fade=False)
    t1 = Text("Digitsum").scale(0.5).next_to(g1, UP, aligned_edge=LEFT)
    scene.add(t1)
    t3 = Text(str(tdans), font="Cambria Math").next_to(g1[0], DOWN)
    scene.add(t3)
    scene.wait(3)
    scene.add(td3)
    scene.wait(1)
    if tdans == d3:
        t2 = MarkupText(Span("The answer is likely correct", color="green"))
    else:
        t2 = MarkupText(Span("The answer is wrong", color="red"))
    t2.scale(0.8).move_to(2.5*DOWN)
    scene.add(t2)
    scene.wait(3)
    scene.play(FadeOut(g, g1, t1, t2, t3, td3))  # td1, td2, td3, 
    
def calcDigitsum(scene, num, wait=5, fade=True, scale=0.75, move=(-2, -2)):
    title = DisplayText(scene, Span("Let's calculate the digitsum of ", color="Turquoise", font='Cambria Math')+
                        Span(num, color="Yellow", font='Cambria Math'),
                        scale=scale, wait=0, move=move, fade=False)
    n = int(num)
    digsum_l = []
    
    # Loop until current sum is <=9
    while n>9:
        dsum = sum([int(s) for s in str(n)])  # Current sum of digits
        digsum_l.append(f"{'+'.join([s for s in str(n)])} = {dsum}")  # Display current sum of digits
        n = dsum  # Next step
        
    el = [MarkupText(x, font='Cambria Math') for x in digsum_l]
    eg = VGroup(*el).scale(scale).arrange(DOWN, aligned_edge=LEFT)

    t = MarkupText(Span(f"The digitsum of {num} is {n}", color="Turquoise", font='Cambria Math'))
    t.scale(scale).next_to(eg, DOWN, buff=0.5)
    
    for _el in el:
        scene.play(AddTextLetterByLetter(_el, time_per_letter=1))
        scene.wait(3)
    scene.add(t)
    scene.wait(2)
    if fade:
        scene.play(FadeOut(eg, title, t))
    return eg

class Samkalanavyavakalanaabhyaam(Scene):
    def construct(self):
        # Title


        Title(self, "उत्तरपरिशोधनम् - २", "Answer Verification - 2", move=(3, 5), wait=2)
        self.next_section()
        self.wait(1)


        # Introduction

        text = [
            f"In the last lesson on <span color='orangered'>answer verification</span>, we saw <span color='LIGHTCORAL'>digitsum. </span>",
            f"It is also known as <span color='CYAN'>नवशेष:</span> as it is the <span color='goldenrod'>remainder, </span>",
            f" when any number is <span color='goldenrod'> divided by <span font='Cambria Math'> 9.</span> </span>",
            f"Only difference is that,",
            f"if <span color='LIGHTCORAL'>digitsum </span> is <span font='Cambria Math'>9</span>,<span color='CYAN'> नवशेष: </span> will be <span font='Cambria Math'> 0 </span>.",
            f"The reason is obvious - remainder is always less than the divisor. "]


        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        # font='Cambria Math',

        #self.wait(1)
        self.next_section

        calcDigitsum(self, "48", 1)
        self.next_section()

        calcDigitsum(self, "27", 1)
        self.next_section()

        self.wait(1)


        text = [
            f"While verifying the answer, ",
            f"we say that the <span color='LIME'>answer is likely correct, </span>if <span color='CYAN'> नवशेष: </span>is same.",
            f"Else we decide that the <span color='RED'> answer is wrong. </span>",
            f"But there are some cases in which we can't make a correct decision. ",
            f"<span color='YELLOW'>Let's see an example.</span>"]

        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)
        self.wait(2)
        self.next_section()


        digitsumcheck2(self, "9", "45", "45", "×", "2025", "47", "45", "×", "2025")
        self.next_section()

        self.wait(2)
        text = [
          f"<span color='ORANGE' > एकादशशेष: </span><span color='WHITE'> can be used in such cases.</span> ",
          f"<span color='WHITE'>It is the </span><span color='ORANGE'> remainder, </span><span color='WHITE'> when we </span><span color='ORANGE'>divide any number by 11.</span> ",
          f"To compute the <span color='ORANGE'> एकादशशेष: </span> of any number, ",
          f"alternately add and subtract its digits, from right to left. ",
          ]

        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)
        self.wait(2)
        self.next_section()


        # Sutra Scene
        t0 = Span("संकलनव्यवकलनाभ्याम्")
        t1 = [Span("संकलनव्यवकलनाभ्याम्")]
        t2 = [Span("By Addition and by Subtraction ")]
        Sutra(self, t0, t1, t2, wait=0, scale=0.65, move=None, fade=True, font='Cambria Math', dir1=DOWN, dir2=DOWN)

        self.next_section()

        shesha11(self, "345")
        shesha11(self, "4567")
        shesha11(self, "691")

        digitsumcheck2(self, "11","45", "45", "×", "2025", "47", "45", "×", "2025")
        self.next_section()



def dsum_911(s,shesha):

    if shesha == "9":
        n = int(s)
        while n > 9:
            n = sum([int(s) for s in str(n)])

        if n==9:
            n=0
    else:
        rev_num = s[::-1]
        n = sum((int(rev_num[i]) * -1 if i % 2 else int(rev_num[i]) for i in range(len(rev_num))))

    return n

def digitsumcheck2(scene,shesha, num1, num2, opr, ans, num3, num4, opr2, ans2, wait=5, fade=True, scale=0.3, move=(3, 6)):
    ''' Digitsum and 11 shesha check '''
    def _op(d1, d2):
        if opr == "×":
            return d1*d2
        else:
            return eval(f"{d1}{opr}{d2}")

    title = DisplayText(scene, Span("Check", color="Turquoise"), scale=0.8, wait=0, move=(-3, -4), fade=False)

    g_9 = ShowOp(scene, num1, num2, opr, ans, move=(0, -5), wait=2, fade=False)
    scene.wait(4)

    d1_9 = dsum_911(num1,shesha)
    d2_9 = dsum_911(num2,shesha)
    d3_9 = dsum_911(ans,shesha)
    cans_9 = _op(d1_9, d2_9)
    tdans_9 = dsum_911(str(cans_9),shesha)

    td3_9 = Text(str(d3_9), font="Cambria Math", color="ORANGE").next_to(g_9, DOWN)

    gd_9 = ShowOp(scene, str(d1_9), str(d2_9), opr, cans_9, move=(0, -2), wait=0, fade=False)
    scene.wait(5)

    if shesha == "11":
        t1_9 = Text("एकादशशेष:").scale(0.5).next_to(gd_9, UP, aligned_edge=LEFT)
    else:
        t1_9 = Text("नवशेष:").scale(0.5).next_to(gd_9, UP, aligned_edge=LEFT)

    scene.add(t1_9)



    t3_9 = Text(str(tdans_9), font="Cambria Math", color="ORANGE").next_to(gd_9[0], DOWN)
    scene.add(t3_9)
    scene.wait(5)
    scene.add(td3_9)
    scene.wait(2)

    if tdans_9 == d3_9:
        t2_9 = MarkupText(Span("The answer is likely correct", color="green"))
    else:
        t2_9 = MarkupText(Span("The answer is wrong", color="red"))



    t2_9.scale(0.6).move_to(2.5*DOWN + LEFT*3)
    scene.add(t2_9)

    scene.wait(2)

    ln = Line(start=array([0, 6, 1]), end=array([0, 0, 1])).set_color(PURE_GREEN)
    l1 = VGroup(ln).arrange(DOWN, aligned_edge=RIGHT)
    scene.add(l1)

    g_11 = ShowOp(scene, num3, num4, opr, ans2, move=(0, 2), wait=2, fade=False)
    scene.wait(4)
    d1_11 = dsum_911(num3,shesha)
    d2_11 = dsum_911(num4,shesha)
    dans_11 = dsum_911(ans2,shesha)
    td3_11 = Text(str(dans_11), font="Cambria Math", color="ORANGE").next_to(g_11, DOWN)
    cans_11 = _op(d1_11, d2_11)

    tdans_11 = dsum_911(str(cans_11),shesha)

    gd_11 = ShowOp(scene, str(d1_11), str(d2_11), opr, cans_11, move=(0,5), wait=0, fade=False)
    scene.wait(5)

    t1_11 = Text("11 Shesha").scale(0.5).next_to(gd_11, UP, aligned_edge=LEFT)

    if shesha == "11":
        t1_11 = Text("एकादशशेष:").scale(0.5).next_to(gd_11, UP, aligned_edge=LEFT)
    else:
        t1_11 = Text("नवशेष:").scale(0.5).next_to(gd_11, UP, aligned_edge=LEFT)

    scene.add(t1_11)

    t3_11 = Text(str(tdans_11), font="Cambria Math", color="ORANGE").next_to(gd_11[0], DOWN)
    scene.add(t3_11)
    scene.wait(5)
    scene.add(td3_11)
    scene.wait(2)

    if tdans_11 == dans_11:
        t2_11 = MarkupText(Span("The answer is likely correct", color="green"))
    else:
        t2_11 = MarkupText(Span("The answer is wrong", color="red"))

    t2_11.scale(0.6).move_to(2.5 * DOWN + RIGHT * 3)
    scene.add(t2_11)
    scene.wait(3)
    scene.play(FadeOut(g_9,g_11 ,l1, title, gd_9,gd_11,t1_11,t1_9,t2_9,t2_11,t3_11,t3_9,td3_11,td3_9))



    return t2_11

def shesha11(scene, num, wait=5, fade=True, scale=0.75, move=(-2, -2)):
    title = DisplayText(scene, Span("Let's calculate the एकादशशेष: of ", color="Turquoise") +
                        Span(num, color="Yellow", font='Cambria Math'),
                        scale=scale, wait=0, move=move, fade=False)

    scene.wait(2)
    # sum according to the sutra

    rev_num = num[::-1]
    sum1 = dsum_911(num,"11")
    #numOPR.extend((str(rev_num[i]) + "+") if i % 2 else (str(rev_num[i]) + "-") for i in range(len(rev_num)))

    numOPR = []
    for i in range(len(rev_num)):
        if i % 2:
            numOPR.extend(str(rev_num[i]) + "+")
        else:
            numOPR.extend(str(rev_num[i]) + "-")

    numOPR.pop()
    numOPR.extend("=" + str(sum1))
    add11 = False

    if sum1<0:
        numOPR.append("+")
        numOPR.append("11")
        sum1 = sum1 + 11
        add11 = True
        numOPR.extend("=" + str(sum1))
        t11 = MarkupText(Span("Here the answer is negative. So 11 is added.", font='Cambria Math', color="yellow"))



    el = [MarkupText(x, font='Cambria Math') for x in numOPR]
    eg = VGroup(*el).scale(scale).arrange(RIGHT, aligned_edge=RIGHT)
    eg.move_to(UP + RIGHT*2)

    for _el in el:
        scene.play(AddTextLetterByLetter(_el, time_per_letter=1))
        scene.wait(1.5)
    if add11:
        t11.scale(0.6).move_to(RIGHT * 2)
        scene.add(t11)

    scene.wait(1)

    scene.play(FadeOut(eg, title))
    if add11:
        scene.play(FadeOut(t11))
    return

def find_Norm_form(scene, num):
    # converting to Normal form
    vinc = False
    frag = ""
    vincD = []
    dig_lef_dec = False
    for s in num:
        frag = frag + s
        if int(s) < 0:
            if vinc == False:
                vinc = True
                vincD.append(str(10 + int(s)))
            else:
                vincD.append(str(9 + int(s)))
        else:
            if (vinc == True):
                vincD.append(str(int(s) - 1))
                dig_lef_dec = True
                frag = ""
                vinc = False
            else:
                vincD.append(str(int(s)))
    if dig_lef_dec == False:
        vincD.append("1")

    return vincD

def find_vinc_form(scene, num):
    # converting to vinculum form  as fragments
    vinc = False
    frag = ""
    vincD = []
    dig_lef_inc = False

    for s in num[::-1]:
        frag = frag + s
        if int(s) > 5:
            if vinc == False:
                vinc = True
                vincD.append(str(-1 * (10 - int(s))))
            else:
                vincD.append(str(-1 * (9 - int(s))))
        if (int(s)< 6):
            if (vinc == True):
                vincD.append(str(int(s) + 1))
                dig_lef_inc = True
                frag = ""
                vinc = False
            else:
                vincD.append(str(int(s)))
    if dig_lef_inc == False:
        vincD.append("1")
    return vincD

def ToNormal(scene, num):
    # Displaying num in Normal form
    # find_Norm_form - converts the number to normal form

    vincD = find_vinc_form(scene,num)
    el1 = [MathTex("\overline{" + str(abs(int(x))) + "}") if (int(x) < 0) else MathTex(x) for x in vincD]
    eg1 = VGroup(*el1).scale(1).arrange(LEFT * 2, aligned_edge=ORIGIN)
    eg1.next_to(eg1, UP*2)

    for _el1 in el1:
        scene.play(AddTextLetterByLetter(_el1, time_per_letter=1))
    scene.wait(1)

    normD = find_Norm_form(scene, vincD)
    el = [MathTex(x) for x in normD]
    eg = VGroup(*el).scale(1).arrange(LEFT * 2, aligned_edge=ORIGIN)
    eg.next_to(eg1, DOWN)

    for _el in el:
        scene.play(AddTextLetterByLetter(_el, time_per_letter=1))
    scene.wait(1)
    scene.play(FadeOut(eg,eg1))
    return eg

def Tovinculum(scene, num):
    # Displaying the vinculum form
    # find_vinc_form - converts the num to vinculum form  as fragments
    vincD = find_vinc_form(scene, num)

    el1 = [MathTex(x) for x in num[::-1]]
    eg1 = VGroup(*el1).scale(1).arrange(LEFT * 2, aligned_edge=ORIGIN)
    eg1.move_to(UP*2)

    for _el1 in el1:
        scene.play(AddTextLetterByLetter(_el1, time_per_letter=1))
    scene.wait(1)

    el = [MathTex("\overline{" + str(abs(int(x))) + "}") if (int(x) < 0) else MathTex(x) for x in vincD]
    eg = VGroup(*el).scale(1).arrange(LEFT * 2, aligned_edge=ORIGIN)
    eg.next_to(eg1, DOWN)

    for _el in el:
        scene.play(AddTextLetterByLetter(_el, time_per_letter=1))
    scene.wait(1)
    scene.play(FadeOut(eg,eg1))
    return eg


def ut_vinc3dig(scene,sn1,sn2):
    ''' UT 3 Digit multiplication of Vinculum Numbers '''

    res= str(int(sn1)*int(sn2))
    t = DisplayText(scene, "Multiplication Example", scale=0.7, wait=0, move=(-2, 0),
                    fade=False, font='Cambria Math')

    el1 = [MathTex(x) for x in sn1[::-1]]
    eg1 = VGroup(*el1).scale(1).arrange(LEFT * 2, aligned_edge=ORIGIN)
    eg1.next_to(t, LEFT*2 + DOWN*2)

    for _el1 in el1:
        scene.play(AddTextLetterByLetter(_el1, time_per_letter=1))
    scene.wait(1)


    el2 = [MathTex(x) for x in sn2[::-1]]
    eg2 = VGroup(*el2).scale(1).arrange(LEFT * 2, aligned_edge=ORIGIN)
    eg2.next_to(eg1, DOWN)

    for _el2 in el2:
        scene.play(AddTextLetterByLetter(_el2, time_per_letter=1))
    scene.wait(1)

    ln1 = Line(start=array([0, 4,0]), end=array([2, 4, 0])).set_color(YELLOW)
    l1 = VGroup(ln1).arrange(RIGHT, aligned_edge=RIGHT)
    l1.next_to(eg1, DOWN*4)
    scene.add(l1)
    scene.wait(1)

    ans1 = [MathTex(x) for x in res[::-1]]
    ans1g = VGroup(*ans1).scale(1).arrange(LEFT * 2, aligned_edge=ORIGIN)
    ans1g.next_to(l1, DOWN*2)

    for _ans1 in ans1:
        scene.play(AddTextLetterByLetter(_ans1, time_per_letter=1))
    scene.wait(1)

    vincD1 = find_vinc_form(scene,sn1)

    el3 = [MathTex("\overline{" + str(abs(int(x))) + "}") if (int(x) < 0) else MathTex(x) for x in vincD1]
    eg3 = VGroup(*el3).scale(1).arrange(LEFT * 2, aligned_edge=ORIGIN)
    eg3.next_to(eg1, RIGHT*14)

    for _el3 in el3:
        scene.play(AddTextLetterByLetter(_el3, time_per_letter=1))
    scene.wait(1)

    vincD2 = find_vinc_form(scene,sn2)
    el4 = [MathTex("\overline{" + str(abs(int(x))) + "}") if (int(x) < 0) else MathTex(x) for x in vincD2]
    eg4 = VGroup(*el4).scale(1).arrange(LEFT * 2, aligned_edge=ORIGIN)
    eg4.next_to(eg3, DOWN)

    for _el4 in el4:
        scene.play(AddTextLetterByLetter(_el4, time_per_letter=1))
    scene.wait(1)

    ln2 = Line(start=array([0,4,0]), end=array([2,4, 0])).set_color(RED)
    l2 = VGroup(ln2).arrange(RIGHT, aligned_edge=RIGHT)
    l2.next_to(eg3, DOWN*4)
    scene.add(l2)
    scene.wait(1)

    ans =[]
    ans.append(str(int(vincD1[0]) * int(vincD2[0])))
    ans.append(str((int(vincD1[0]) * int(vincD2[1])) + ((int(vincD1[1]) * int(vincD2[0])))))
    ans.append(str((int(vincD1[0]) * int(vincD2[2])) + (int(vincD1[1]) * int(vincD2[1])) + (int(vincD1[2]) * int(vincD2[0]))))
    ans.append(str((int(int(vincD1[1]) * int(vincD2[2])) + (int(vincD1[2]) * int(vincD2[1])))))
    ans.append(str(int(vincD1[2]) * int(vincD2[2])))

    el5 = [MathTex("\overline{" + str(abs(int(x))) + "}") if (int(x) < 0) else MathTex(x) for x in ans]
    eg5 = VGroup(*el5).scale(1).arrange(LEFT * 2, aligned_edge=ORIGIN)
    eg5.next_to(l2, DOWN*2)

    for _el5 in el5:
        scene.play(AddTextLetterByLetter(_el5, time_per_letter=1))
    scene.wait(1)

    vincD = find_Norm_form(scene,ans)

    el6 = [MathTex("\overline{" + str(abs(int(x))) + "}") if (int(x) < 0) else MathTex(x) for x in vincD]
    eg6 = VGroup(*el6).scale(1).arrange(LEFT * 2, aligned_edge=ORIGIN)
    eg6.next_to(eg5, DOWN*2)

    for _el6 in el6:
        scene.play(AddTextLetterByLetter(_el6, time_per_letter=1))
    scene.wait(1)

    scene.play(FadeOut(t,eg1, eg2, eg3, eg4,eg5,eg6,ans1g, l1, l2))
    return eg1

class Rekhitasamkhyaa(Scene):
    def construct(self):
        # Vinculum numbers  24 06 2022
        # Title

        Title(self, "रेखितसङ्ख्याः", "Vinculum Numbers", move=(3, 5), wait=2)
        self.next_section()
        self.wait(1)
        # Introduction

        text = [
            f"We all are familiar with +ve and -ve numbers.",
            f"Have you seen a number in which ",
            f"<span color = 'CYAN'>some digits are +ve and some are -ve?</span>",
            f"After all, what is the use of such a representation?",
            f"Quite interesting right?",
            f"Yes! Today's lesson is all about such special numbers."
        ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        text = [
            f"A number that is represented ",
            f"<span color ='YELLOW'>partly as positive and partly negative </span> is called a ",
            f"<span color = 'CYAN'>Vinculum number or रेखितसङ्ख्या. </span>",
            f"A <span color = 'LIGHTCORAL'>vinculum </span> (overbar) is used to indicate <span color='ORANGE'>negative digits.</span>",
            f"This gives the number an easier form to deal with ",
            f"the techniques that we learned before."
        ]
        e = Explanation(self, text,wait=2, fade=True, aligned_edge=LEFT)

        text = [
            f"How do we understand the value of the number <span color='CYAN'>18</span>? ",
            f"<span color='ORANGE'> 8</span> added with <span color='ORANGE' >10</span> is <span color='CYAN'> 18</span>",
            f"Is there any other way to get the value <span color='CYAN'> 18</span>?",
            f"Yes, <span color='CYAN'> 18 </span>is <span color='ORANGE'>2</span> subtracted from <span color='ORANGE' > 20</span> ",
            f"So, how can write that? " ]

        e1 = Explanation(self, text,font = "Cambria Math", wait=2, fade=False , aligned_edge=LEFT)

        t = MathTex("2", "\overline{2}")

        t.move_to(DOWN*1.2 )
        self.wait(1)
        self.add(t)
        self.wait(5)

        self.play(FadeOut(e1))
        self.remove(e1)
        self.remove(t)
        self.wait(2)

        # Sutra Scene
        t0 = Span("निखिलं नवतश्चरमं दशत:")
        t1 = [Span("निखिलं नव त:, चरमं दश त:")]
        t2 = [Span("All from 9, last from 10 ")]
        Sutra(self, t0, t1, t2, wait=0, scale=0.65, move=None, fade=True, font='Cambria Math', dir1=DOWN, dir2=DOWN)
        self.wait(2)

        text = [
            f"How to convert a number to <span color = 'CYAN'> vinculum? </span> ",
            f"For every sequence of digits > 5,  ",
            f"use <span color ='YELLOW'>Nikhilam</span> method.",
            f"Increase the previous digit by 1.",
        ]
        e = Explanation(self, text, font='Cambria Math',wait=2, fade=True, aligned_edge=LEFT)

        t = DisplayText(self, "Let's see some Examples - Normal to Vinculum", scale=0.7, wait=0, move=(-3, -1),
                        fade=False, font='Cambria Math')

        Tovinculum(self, "38")
        Tovinculum(self, "68")
        Tovinculum(self, "3768")
        Tovinculum(self, "278186")

        self.play(FadeOut(t))

        text = [
            f"How to convert a Vinculum number to <span color = 'CYAN'>Normal</span> Notation? ",
            f"For every vinculum digit,  ",
            f"use <span color ='YELLOW'>Nikhilam</span> method.",
            f"Reduce the previous digit by 1.",
        ]
        e = Explanation(self, text, font='Cambria Math', wait=2, fade=True, aligned_edge=LEFT)

        t = DisplayText(self, "Let's see some Examples -  Vinculum to Normal", scale=0.7, wait=0, move=(-3, -1),
                        fade=False, font='Cambria Math')

        ToNormal(self, "38")
        ToNormal(self, "68")
        ToNormal(self, "3768")
        ToNormal(self, "278186")

        self.play(FadeOut(t))

        text = [
            f"What is the actual benefit of the  <span color = 'CYAN'>Vinculum</span> notation? ",
            f"Sometimes we feel that mathematical operations ",
            f"with digits like 6,7,8,9 are bit hard.",
            f"Digits upto 5 are really easy to handle.",
            f"So,in the  <span color = 'CYAN'>Vinculum</span> form of numbers, these <span color='YELLOW'>digits >5</span> ",
            f"<span color='YELLOW'>are converted with face value 4,3,2,1. </span>"
        ]
        e = Explanation(self, text, font='Cambria Math',wait=2, fade=True, aligned_edge=LEFT)

        text = [
            f"If we have a clear idea about  <span color = 'YELLOW'>negative number handling</span>,",
            f" <span color = 'CYAN'>Vinculum</span> Numbers can really help us."
              ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        text = [
            f"And please note that,",
            f"this is  <span color = 'ORANGE'>strictly not necessary</span> for any of the ",
            f"Vedic Mathematics methods. ",
            f"But it does <span color = 'LIGHTCORAL'> make things easier</span> in some cases."
              ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        text = [
            f" <span color = 'CYAN'>Vinculum</span> notation is useful when there are  <span color = 'YELLOW'>large digits.</span> ",
            f"If we convert them into vinculum digits,",
            f"mathematical operations becomes really easy ",
            f"as the <span color = 'YELLOW'>face value of the digits are decreased.</span>",
              ]
        e = Explanation(self, text, wait=2, fade=True, aligned_edge=LEFT)

        ut_vinc3dig(self, "189","197")
        self.next_section
