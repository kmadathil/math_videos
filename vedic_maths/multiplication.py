from manim import *
from numpy import array
from common import *


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


def YavadunamMult(scene, num1, num2, wait=5, fade=True):
    snum1 = str(num1)
    inum1 = int(num1)
    snum2 = str(num2)
    inum2 = int(num2)
    base = findbase(num1)  # Nearest power of 10
    diff1 = (base - inum1)  # Difference from that
    diff2 = (base - inum2)  # Difference from that
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
    assert ans == lans * 10**ndig + rans, f" {ans} != {lans * 10**ndig + rans}, {base, diff1, diff2, lans, ndig, rans}"
    
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
    return YCom(scene, snum1, snum2, base, negp1, negp2, abs(diff1), abs(diff2), rans, lans, ans, ndig, wait, fade)


def YavadunamSquare(scene, num, wait=5, fade=True):
    snum = str(num)
    inum = int(num)
    base = findbase(num)  # Nearest power of 10
    diff = (base - inum)  # Difference from that
    negp = (diff > 0)     # Are we below base?
    ndig = len(str(base))-1   # Number of zeros in base

    rans = diff **2  # Right part of answer, has ndig digits
    lans = inum - diff  # Left part of answer - number + diff from base 
    
    dirs = " - " if negp else " + "
    bdiff = "less than" if negp else "greater than"

    ans = inum**2
    assert ans == lans * 10**ndig + rans, f" {ans} != {lans * 10**ndig + rans}, {base, diff, lans, ndig, rans}"
    
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
    return YCom(scene, snum, snum, base, negp, negp, abs(diff), abs(diff), rans, lans, ans, ndig, wait, fade)

def YCom(scene, snum, snum2, base, negp1, negp2, diff, diff2,  rans, lans, ans, ndig, wait, fade):
    g   = ShowOp(scene, snum, snum2, "×", "?", wait=1, fade=False)

    tb = MarkupText(f"Nearest base is <span color='red'>{base}</span>", color="Turquoise", font='Cambria Math')

    if negp1:
        g1 = ShowOp(scene, base, snum, "-", diff, play=False)
    else:
        g1 = ShowOp(scene, snum, base, "-", diff, play=False)
    if negp2:
        g12 = ShowOp(scene, base, snum2, "-", diff2, play=False)
    else:
        g12 = ShowOp(scene, snum2, base, "-", diff2, play=False)

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
    br = SurroundingRectangle(ar, buff=0.5)
    bl = SurroundingRectangle(al, buff=0.5)
    ga = VGroup(VGroup(al, bl), VGroup(ar, br)).arrange(RIGHT)    

    ga.move_to(DOWN*2)
    g.next_to(ga[0], UP)
    alf.next_to(al, ORIGIN)
    arf.next_to(ar, ORIGIN)
    g2.next_to(ga[0], UP)
    g22.move_to(LEFT)
    g1.next_to(ga[1], UP)
    g12.next_to(g1, ORIGIN)
    g3.next_to(g1, ORIGIN)



    scene.add(g.move_to(LEFT*4))
    scene.add(tb.next_to(g, UP*3))
    scene.wait(2)
    scene.add(ga)
    scene.wait(1)
    scene.add(g1)
    scene.wait(2)
    if diff != diff2:
        scene.play(Transform(g1, g12))
        scene.wait(2)
    scene.play(Transform(g1, g3))
    scene.wait(1)
    scene.play(Transform(ar, arf))
    scene.wait(1)
    #scene.play(Transform(g, g2))
    scene.add(g2)
    scene.wait(1)
    if diff != diff2:
        scene.play(Transform(g2, g22))
        scene.wait(1)
    scene.play(Transform(al, alf))
    scene.wait(2)
    scene.play(FadeOut(g2, g1))
    scene.wait(2)
    scene.remove(g1, g3)
    scene.play(Transform(ga, g4))
    scene.wait(wait)
    if fade:
        scene.play(FadeOut(ga, g, tb))
    return ga

def by11(scene, num, wait=5, fade=True, scale=0.3, move=(3, 6)):
    snum = "0" + str(num) + "0"
    numdig = len(snum)
    n = numdig - 1

    title = DisplayText(scene, Span("Examples", color="Turquoise"), scale=0.8, wait=0, move=(-3, -4), fade=False)

    qs = ShowOp(scene, num, 11, "×", "?", move=(0, 0), play=False)
    qs.move_to(LEFT * 3)
    scene.add(qs)
    scene.wait(1)
    scene.next_section()

    numdig = len(snum)
    n = numdig - 1
    i = 0

    #numg = []
    #while i <= n:
    #    dig1 = str(snum[i])
    #    numg.append(dig1)
    #    i = i + 1
    numg = [s for s in snum]
    
    t = DisplayText(scene, Span("1.Add zeroes at both ends of the number.", color="Turquoise"), scale=0.5, wait=0, move=(-2, 3),
                    fade=False, font='Cambria Math')

    el = [MarkupText(x, font_size=130) for x in numg]
    eg = VGroup(*el).scale(scale).arrange(RIGHT * 2, aligned_edge=ORIGIN)
    eg.move_to(UP + RIGHT * 4)

    for _el in el:
        scene.play(AddTextLetterByLetter(_el, time_per_letter=1))
    scene.wait(1)

    #sp = []
    #j = n
    #while j > 0:
    #    sum = int(snum[j])
    #    j = j-1
    #    sum = sum + int(snum[j])
    #    sp.append(str(sum))
    sp = [str(int(snum[i])+int(snum[i+1])) for i in reversed(range(len(snum)-1))]
    
    scene.play(FadeOut(t))
    t = DisplayText(scene, Span("2. Add the last two digits to get one digit of the Answer.", color="Turquoise"), scale=0.5, wait=0, move=(-2, 3),
                    fade=False, font='Cambria Math')

    spl = [MarkupText(x, font_size=130) for x in sp]
    spg = VGroup(*spl).scale(scale).arrange(LEFT * 2, aligned_edge=ORIGIN)
    spg.next_to(eg, DOWN)

    j = n
    for _spl in spl:
        scene.play(eg[j].animate.set_color(YELLOW))
        j = j-1
        scene.play(eg[j].animate.set_color(YELLOW))
        scene.play(AddTextLetterByLetter(_spl, time_per_letter=1))
        scene.play(eg[j+1].animate.set_color(RED))
    scene.wait(1)

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
                        scale=0.5, wait=0, move=(-2.4, 3),
                        fade=False, font='Cambria Math')
        t2 = DisplayText(scene, Span("...  other digits are added to the digits to its left.",
                                    color="Turquoise"),
                        scale=0.5, wait=0, move=(-2, 3),
                        fade=False, font='Cambria Math')

        t3 = DisplayText(scene, Span("With more practice, we can do this directly in 2nd step",
                                    color="Turquoise"),
                        scale=0.5, wait=0, move=(2, 3),
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
            j = j+1
            scene.wait(1)

    scene.wait(1)

    if cy_found == True:
        scene.play(FadeOut(t1, t2,t3))

    g2 = ShowOp(scene, num, 11, "×", int(num)*11, move=(0, 0), play=False)
    g2.move_to(LEFT * 2)
    scene.play(Transform(qs, g2))
    scene.wait(1)

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

        YavadunamSquare(self, 1002)
        self.next_section()

        
    
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
        self.wait(5)


class Antyayoreva(Scene):
    ''' Antyayo eva '''

    def construct(self):
        # Title

        Title(self, "अन्त्ययोरेव", "Multiply any number by 11 ", move=(3, 5), wait=2)
        self.next_section()

        # Introduction
        text = ["<span color='TURQUOISE'>Multiplication by 11</span>",
                "by applying the sutra Antyayoreva"]

        Explanation(self, text, aligned_edge=LEFT)
        self.next_section()

        # Sutra Scene
        t0 = "अन्त्ययोरेव"
        t1 = ["अन्त्ययोः", "एव"]
        t2 = ["<span size='smaller'>(Sum of) last digits</span>", "<span size='smaller'>only</span>"]
        Sutra(self, t0, t1, t2, wait=3, scale=1, move=None, fade=True, font='Cambria Math')
        self.next_section()

        text = [
            f"<span color='TURQUOISE'>To multiply any number by 11</span>",
            f"Add zeros at both ends of the number.",
            f"At each step,",
            f"1) Add the last two digits to get one digit of the answer.",
            f"2) Drop the right digit of the number",
            "repeat until no digits remain."]

        Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)
        self.next_section()

        by11(self, 123)
        self.next_section()

        by11(self, 489)
        self.next_section()

        by11(self, 7485)
        self.next_section()
