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
        f"<span color='#0C8694'>Find the Square of </span><span color='yellow'>{snum}</span>",
        f"Digit(s) before 5 are <span color='yellow'>{sprev}</span>",
        f"One more than that is  <span color='yellow'>{prev+1}</span>",
        f"Our answer is simply <span color='yellow'>{prev} times {prev+1}, suffixed with 25</span>",
        f"Which is <span color='yellow'>{prev*(prev+1)}{25}</span>"]
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
    g11   = ShowOp(scene, prev, "<span color='red'>"+str(prev+1)+"</span>", "×", lans, play=False)
    g12   = ShowOp(scene, f1, f2, "×", rans, play=False)

    ar = Text("_" * ndig, color='yellow').scale(1.2)
    arf = Text(str(rans).zfill(ndig), color='yellow').scale(1.2)
    al = Text("_" * len(str(lans)), color='yellow').scale(1.2)
    alf = Text(str(lans), color='yellow').scale(1.2)
    br = SurroundingRectangle(ar, buff=0.5)
    bl = SurroundingRectangle(al, buff=0.5)
    ga = VGroup(VGroup(al, bl), VGroup(ar, br)).arrange(RIGHT)
    
    ga.move_to(DOWN*2)
    arf.next_to(ar, ORIGIN)
    alf.next_to(al, ORIGIN)
    scene.add(ga)
    scene.wait(2)
    g12.move_to(RIGHT*2)
    scene.play(Transform(g, g11))
    scene.add(g12)
    scene.play(Transform(ar, arf))
    scene.play(Transform(al, alf))
    scene.wait(2)
    #scene.play(FadeOut(g[1]))
    #scene.play(g12.animate.next_to(g[0], RIGHT, aligned_edge=UP))
    scene.play(FadeOut(g, g12))
    scene.wait(2)
    g2  = ShowOp(scene, snum, snum2, "×", ans, play=False)
    #scene.remove(g12)
    scene.play(Transform(ga, g2))
    scene.wait(wait)
    if fade:
        scene.play(FadeOut(ga))
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
        f"<span color='#0C8694'>Find the product of </span><span color='yellow'>{snum} and {snum2}</span>",
        f"Final digits are <span color='yellow'>{snum[-1]} and {snum2[-1]}</span>",
        f"Their product is <span color='yellow'>{int(snum[-1])*int(snum2[-1])}</span>",
        f"Pre-final Digit(s) are <span color='yellow'>{sprev}</span>",
        f"One more than that is  <span color='yellow'>{prev+1}</span>",
        f"As before, our answer begins with <span color='yellow'>{prev} times {prev+1}</span>",
        f"It is now suffixed with <span color='yellow'>{int(snum[-1])*int(snum2[-1])}</span>",
        f"Which leads us to <span color='yellow'>{inum*inum2}</span>"]
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
        f"<span color='#0C8694'>Find the product of </span><span color='yellow'>{snum1}</span> and <span color='yellow'>{snum2}</span>",
        "1.  The nearest power of 10 is: " + Span(str(base),color='red') + " with " + Span(str(ndig), color='green') + " digits",
        f"1a. <span color='yellow'>{snum1}</span> and <span color='yellow'>{snum2}</span> are " + Span(str(abs(diff1)), color='orange') + f" {bdiff1} and " + Span(str(abs(diff2)), color='orange') +  f" {bdiff2} the base " + Span(str(base),color='red'),
        "2.  The right part of the answer is " + Span(f"{abs(diff1)} * {abs(diff2)}", color='orange') + " = " + Span(str(rans).zfill(ndig), color='yellow'),
        "3.  The left part of the answer is " + Span(snum1, color='yellow') + dirs1 + Span(str(abs(diff2)), color='orange') + " = " + Span(lans, color='yellow'),
        "3a. The left part of the answer can also be written as " + Span(snum2, color='yellow') + dirs2 + Span(str(abs(diff1)), color='orange') + " = " + Span(lans, color='yellow'),
        f"4. Putting them together, <span color='yellow'>{snum1}×{snum2}</span> = " + Span(ans, color='yellow')
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
        f"<span color='#0C8694'>Find the square of </span><span color='yellow'>{snum}</span>",
        "1.  The nearest power of 10 is: " + Span(str(base),color='red') + " with " + Span(str(ndig), color='green') + " digits",
        f"1a. <span color='yellow'>{snum}</span> is " + Span(str(abs(diff)), color='orange') + f" {bdiff} the base " + Span(str(base),color='red'),
        "2.  The right part of the answer is " + Span(str(abs(diff)), color='orange') + "² = " + Span(str(rans).zfill(ndig), color='yellow'),
        "3.  The left part of the answer is " + Span(snum, color='yellow') + dirs + Span(str(abs(diff)), color='orange') + " = " + Span(lans, color='yellow'),
        f"4. Putting them together: <span color='yellow'>{snum}</span>² = "  + Span(ans, color='yellow')
    ]
    
    Explanation(scene, text, font='Cambria Math', aligned_edge=LEFT)
    scene.next_section()
    return YCom(scene, snum, snum, base, negp, negp, abs(diff), abs(diff), rans, lans, ans, ndig, wait, fade)

def YCom(scene, snum, snum2, base, negp1, negp2, diff, diff2,  rans, lans, ans, ndig, wait, fade):
    g   = ShowOp(scene, snum, snum2, "×", "?", wait=1, fade=False)
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
    g3 = ShowOp(scene, diff, diff2, "*", str(rans).zfill(ndig), play=False)
    g4  = ShowOp(scene, snum, snum2, "×", ans, play=False)

    ar = Text("_" * ndig, color='yellow').scale(1.2)
    arf = Text(str(rans).zfill(ndig), color='yellow').scale(1.2)
    al = Text("_" * len(snum), color='yellow').scale(1.2)
    alf = Text(str(lans), color='yellow').scale(1.2)
    br = SurroundingRectangle(ar, buff=0.5)
    bl = SurroundingRectangle(al, buff=0.5)
    ga = VGroup(VGroup(al, bl), VGroup(ar, br)).arrange(RIGHT)
    
    scene.add(g)
    g1.move_to(RIGHT*2)
    g12.move_to(RIGHT*2)
    g3.move_to(RIGHT*2)
    ga.move_to(DOWN*2)
    arf.next_to(ar, ORIGIN)
    alf.next_to(al, ORIGIN)
    scene.add(ga)
    scene.wait(2)
    scene.add(g1)
    scene.wait(2)
    if diff != diff2:
        scene.play(Transform(g1, g12))
        scene.wait(2)
    scene.play(Transform(g1, g3))
    scene.wait(1)
    scene.play(Transform(ar, arf))
    scene.wait(1)
    scene.play(Transform(g, g2))
    scene.wait(1)
    if diff != diff2:
        scene.play(Transform(g, g22))
        scene.wait(1)
    scene.play(Transform(al, alf))
    scene.wait(2)
    scene.play(FadeOut(g, g1))
    scene.wait(2)
    scene.remove(g1, g3)
    scene.play(Transform(ga, g4))
    scene.wait(wait)
    if fade:
        scene.play(FadeOut(ga))
    return ga

class Ekadhikena(Scene):
    ''' Ekadhikena Purvena '''
    def construct(self):
        # Title
        Title(self, "एकाधिकेन पूर्वेण", "Squares and Products with Ekadhikena",
              move=(3, 5), wait=2)
        self.next_section()

        # Introduction

        text = ["<span color='#0C8694'>Simple multiplication and squaring</span>",
                "Before we introduce a general method for multiplication",
                "We will look at special cases which are easier"]

        Explanation(self, text, aligned_edge=LEFT)
        self.next_section()

        # Introduction
        text = ["<span color='#0C8694'>Our first method works for</span> ",
                "1. Squares of numbers ending in 5",
                "2. Products of numbers with last digits adding to 10",
                "    and other digits identical"]
        Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)
        self.next_section()


        # Sutra Scene
        t0 = "एकाधिकेन पूर्वेण"
        t1 = ["एकाधिकेन", "पूर्वेणः"]
        t2 = ["<span size='smaller'>By one more than</span>", "<span size='smaller'>the previous</span>"]
        Sutra(self, t0, t1, t2, wait=3, scale=0.5, move=None, fade=True, font='Cambria Math')
        self.next_section()

        EkadhikenaSquare(self, 35)
        self.next_section()

        EkadhikenaSquare(self, 85)
        self.next_section()

        # Sutra Scene
        t0 = "अन्त्ययोर्दशकेऽपि"
        t1 = ["अन्त्ययोः", "दशके अपि"]
        t2 = ["<span size='smaller'>When the last</span>", "<span size='smaller'>sum to 10</span>"]
        Sutra(self, t0, t1, t2, wait=3, scale=0.5, move=None, fade=True, font='Cambria Math')
        self.next_section()

        # Introduction
        text = ["<span color='#0C8694'>We can use this to multiply numbers that</span>",
                "1. have identical digits barring the final one",
                "2. have their final digits adding up to 10"]
        Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)
        self.next_section()

        EkadhikenaMult(self, 33, 37)
        self.next_section()
        
        EkadhikenaMult(self, 72, 78)
        self.next_section()


class Yavadunam(Scene):
    ''' Multiplication with Yavadunam '''
    def construct(self):
        # Title
        Title(self, "यावदूनम्", "Squares and Products with Yavadunam",
              move=(3, 5), wait=2)
        self.next_section()

        # Introduction
        text = [Span("This method works for", color='#0C8694'),
                "1. Squares of numbers near a power of 10",
                "2. Products of numbers near a power of 10"
                ]
        Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)
        self.next_section()


        # Sutra Scene
        t0 = Span("यावदूनम् तावदूनीकृत्य वर्गं च योजयेत्", size='smaller')
        t1 = [Span("यावद् ऊनम्", size='smaller'), Span("तावद् ऊनीकृत्य", size='smaller'), Span("वर्गं च योजयेत्", size='smaller')]
        t2 = [Span("By the difference from the base", size='smaller'),
              Span("Reduce the number", size='smaller'),
              Span("and append the square", size='smaller')]
        Sutra(self, t0, t1, t2, wait=3, scale=0.5, move=None, fade=True, font='Cambria Math', dir1=DOWN, dir2=DOWN)
        self.next_section()

        text= [
            f"<span color='#0C8694'>To find the square of a number </span><span color='yellow'>n</span>",
            "1. Find the nearest base <span color='red'>b</span>, and note its number of digits <span color='green'>k</span>",
            "1a. Note if <span color='yellow'>n</span> is above or below <span color='red'>b</span>, and note the difference <span color='orange'>d</span>",
            "2. We then divide the answer into two parts - left and right",
            "3. The right part of the answer is <span color='orange'>d²</span>, padded to " + Span("k", color='green') + " digits",
            "4. The left part of the answer is,",
            "4a. if n less than b    ⇒ <span color='yellow'>n-</span><span color='orange'>d</span>",
            "4b. if n greater than b ⇒ <span color='yellow'>n+</span><span color='orange'>d</span>",
            "5. Append the left and right parts"
        ]
    
        Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)

        YavadunamSquare(self, 94)
        self.next_section()

        YavadunamSquare(self, 1002)
        self.next_section()

        
    
        text= [
            f"<span color='#0C8694'>To find the product of two numbers </span><span color='yellow'>n1</span> and <span color='yellow'>n2</span>",
            "1. Find the nearest base <span color='red'>b</span>, and note its number of digits <span color='green'>k</span>",
            "1a. Note if <span color='yellow'>n1</span> and <span color='yellow'>n2</span> are above or below <span color='red'>b</span>",
            "1b. note the differences <span color='orange'>d1</span> and <span color='orange'>d2</span>",
            "2. We then divide the answer into two parts - left and right",
            "3. The right part of the answer is <span color='orange'>d1*d2</span>, padded to " + Span("k", color='green') + " digits",
            "4. The left part of the answer is, ",
            "4a. if n1 less than b    ⇒ <span color='yellow'>n1-</span><span color='orange'>d2</span>",
            "4b. if n1 greater than b ⇒ <span color='yellow'>n1+</span><span color='orange'>d2</span>",
            "5. Append the left and right parts"
        ]
    
        Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)

        YavadunamMult(self, 92, 97)
        self.next_section()

        YavadunamMult(self, 104, 110)
        self.next_section()

        YavadunamMult(self, 997, 988)
        self.next_section()

        
    
