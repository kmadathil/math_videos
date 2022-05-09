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

        text = ["This method is all about <span color='Turquoise'>patterns</span>.",
                "Each pattern of <span color='Yellow'>straight</span> and  <span color='Yellow'>across lines</span>",
                "gives us a collection of pairs of numbers.",
                "Each of those  <span color='Turquoise'>pairs</span> is  <span color='Yellow'>multiplied</span>,",
                "And then the  <span color='Turquoise'>products</span> are  <span color='Yellow'>added</span>.",
                "One digit of this  <span color='Turquoise'>partial product</span> becomes a  <span color='Yellow'>digit of the answer</span>.",
                "<span color='Turquoise'>Extra digits</span> become  <span color='Yellow'>carries</span> into the next digit,",
                "and are <span color='Turquoise'>added</span> to the  <span color='Yellow'>next partial product</span>.",
                "All of this can be done mentally."]

        Explanation(self, text, aligned_edge=LEFT)
        self.next_section()

        text = ["A few <span color='Turquoise'>examples</span> should make things clearer,",
                "two-digit examples to start with."]
        Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)

        ut(self, 12, 24, move=(0, -2))
        self.next_section

        ut(self, 34, 57, move=(0, -2))
        self.next_section

        text = ["Three-digit examples"]

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

        

def ut(scene, sn1, sn2,  move=(0, 0), wait=3, d_wait=1, explain=True, show_carry=True, play=True, fade=True, oplen=0):
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
            etext.append(f"We retain <span color='yellow'>{d}</span> as  digit of the answer.")
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
            if ix > 0:  
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
            # Add current result digit in Yellow
            scene.add(x.set_color(YELLOW))

            # Display carry down and to the left
            # Not done for the last step, because if there's a carry
            # it just becomes an extra digit directly
            if show_carry and c and (ix!=(nit-1)):
                ct = Text(str(c)).scale(0.7).next_to(x, DOWN*0.5+LEFT*0.5)
                scene.add(ct)
                c_p = ct
                cl.append(ct)
            # At the last step, display remaining digits of answer too
            if ix==(nit-1) and (lr>nit):
                scene.add(res[:(lr-nit)].set_color(YELLOW))
            scene.wait(d_wait)
            if explain:
                scene.play(FadeOut(eg))
        scene.remove(*lines)  # Remove last u line
        # Remove color emphasis
        n1.set_color(WHITE)
        n2.set_color(WHITE)
        res.set_color(WHITE)
        if show_carry:
            scene.remove(*cl)
        if wait:
            scene.wait(wait)
        if fade:
            scene.play(FadeOut(g))
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
  

class Check_Answer(Scene):
    def construct(self):
        # Title

        Title(self, "उत्तरपरिशोधनम्", "Result Verification", move=(3, 5), wait=2)
        self.next_section()
        self.wait(2)

        # Introduction
        text = [Span("Verifying the results of", color='Turquoise'),
                "Addition, Subtraction, ",
                "Multiplication, Division... ",
                ]
        e = Explanation(self, text, font='Cambria Math', wait=0, fade=False, aligned_edge=LEFT)
        self.wait(2)
        self.play(FadeOut(e))
        self.next_section()

        text = [
            f"<span color='TURQUOISE'>Using </span> <span color='PINK'>digitsum </span><span color='TURQUOISE'> technique, we can verify the results.</span>",
            f"<span color='ORANGE'>Remainder</span><span color='TURQUOISE'> of any number, when </span><span color='ORANGE'>divided by 9, </span> ",
               f"<span color='TURQUOISE'>is equal to it's</span> <span color='PINK'> digitsum. </span>",
              ]

        e = Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)
        self.wait(2)
        self.next_section()

        calcDigitsum(self, "257")
        self.next_section()

        calcDigitsum(self, "5364")
        self.next_section()

        # Sutra Scene
        t0 = Span("गुणितसमुच्चयः समुच्चयगुणितः")
        t1 = [Span("गुणितसमुच्चयः"), Span("समुच्चयगुणितः")]
        t2 = [Span("The digitsum of the product is "),
              Span("The product of the  digitsum(s) ")]
        Sutra(self, t0, t1, t2, wait=3, scale=0.65, move=None, fade=True, font='Cambria Math', dir1=DOWN, dir2=DOWN)
        self.wait(2)
        self.next_section()

        digitsumcheck(self, "98", "96", "x", "9608")
        self.next_section()

        digitsumcheck(self, "232", "426", "x", "98832")
        self.next_section()


def ShowOp9(scene, sn1, sn2, sop, eqs, sr, move=(0, 0), wait=3, play=True, fade=True):
    ''' Helper function to display digitsum  '''
    n1 = MarkupText(str(sn1), font='Cambria Math')
    n2 = MarkupText(str(sn2), font='Cambria Math')

    op = MarkupText(str(sop), font='Cambria Math')
    res = MarkupText(str(sr), font='Cambria Math')
    eqs1 = MarkupText(str(eqs), font='Cambria Math')

    if sn2 == "0":
        g = VGroup(n1, eqs1, res).arrange(RIGHT * 2, aligned_edge=UP)
    else:
        g = VGroup(n1, op, n2, eqs1, res).arrange(RIGHT * 2, aligned_edge=UP)
    if play:
        scene.play(Write(g.move_to(UP * move[0] + RIGHT * move[1])))
        scene.wait(wait)
        if fade:
            scene.play(FadeOut(g))
    return g


def digitsumcheck(scene, num1, num2, opr, ans, wait=5, fade=True, scale=0.3, move=(3, 6)):
    title = DisplayText(scene, Span("Let's verify these", color="Turquoise"), scale=0.6, wait=0, move=(-3, -4),
                        fade=False)

    g2 = ShowOp9(scene, num1, num2, opr, "=", int(ans), move=(1, 0), play=True, fade=False)
    scene.wait(1)

    t1 = DisplayText(scene, Span("product of digitsums = digitsum of the product", color="yellow"), scale=0.5, wait=0,
                     move=(-2, 0), fade=False, font='Cambria Math')
    scene.wait(1)

    num1REM = int(math.fmod(int(num1), 9))
    num2REM = int(math.fmod(int(num2), 9))

    if (opr == "x"):
        resREM = int(math.fmod(int(ans), 9))
        lhsREM = int(math.fmod(int(num1REM) * int(num2REM), 9))
    else:
        resREM = int(math.fmod(int(ans), 9))
        lhsREM = int(math.fmod(int(num1REM) / int(num2REM), 9))

    g3 = ShowOp9(scene, num1REM, num2REM, opr, "=", resREM, move=(0, 0), play=True, fade=False)

    if (lhsREM == resREM):
        g4 = ShowOp9(scene, lhsREM, "0", opr, "=", resREM, move=(-1, 0), play=True, fade=False)
        t = DisplayText(scene, Span("correct answer", color="yellow"), scale=0.5, wait=0, move=(2, 0), fade=False,
                        font='Cambria Math')
        scene.wait(1)
    else:
        g4 = ShowOp9(scene, lhsREM, "0", opr, "!=", resREM, move=(-1, 0), play=True, fade=False)
        t = DisplayText(scene, Span("wrong answer", color="yellow"), scale=0.5, wait=0, move=(2, 0), fade=False,
                        font='Cambria Math')

    scene.wait(2)
    scene.play(FadeOut(t1, t, g2, g3, g4, title))
    scene.next_section()
    return g4


def calcDigitsum(scene, num, wait=5, fade=True, scale=0.3, move=(3, 6)):
    title = DisplayText(scene, Span("Let's calculate Digitsum of " + num, color="Turquoise", font='Cambria Math'),
                        scale=0.6, wait=0, move=(-2, -2), fade=False)
    digsum = []
    digsum.append(int(num))

    if int(num) < 9:
        digsum.append(int(num))
    else:
        if int(num) == 9:
            digsum.append(int(num) - 9)
        else:
            while len(str(num)) > 1:
                num_s = [s for s in num]
                num_int = [int(x) for x in num_s]
                digsum.append(sum(num_int))
                num = str(sum(num_int))

    digsum = [str(x) for x in digsum]
    digsum1 = []
    for x in digsum:
        if (len(x) > 1):
            tmps1 = ""
            for s in x:
                tmps1 = tmps1 + s + ' + '
            digsum1.append(tmps1[:-2])
        else:
            if x == "9":
                digsum1.append(x)
                digsum1.append("0")
            else:
                digsum1.append(x)

    el = [MarkupText(x, font_size=130, font='Cambria Math') for x in digsum1]
    eg = VGroup(*el).scale(scale).arrange(DOWN, aligned_edge=ORIGIN)

    for _el in el:
        scene.play(AddTextLetterByLetter(_el, time_per_letter=1))
        scene.wait(3)

    scene.play(FadeOut(eg, title))
    return eg
