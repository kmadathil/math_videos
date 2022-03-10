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
    g   = ShowOp(scene, snum, snum2, "×", "?", wait=1, fade=False)
    g11   = ShowOp(scene, prev, "<span color='red'>"+str(prev+1)+"</span>", "×", prev*(prev+1), play=False)
    g12   = ShowOp(scene, f1, f2, "×", f1*f2, play=False)
    g12.move_to(RIGHT*2)
    scene.play(Transform(g, g11))
    scene.add(g12)
    scene.wait(2)
    scene.play(FadeOut(g[1]))
    scene.play(g12.animate.next_to(g[0], RIGHT, aligned_edge=UP))
    scene.wait(2)
    g2  = ShowOp(scene, snum, snum2, "×", ans, play=False)
    scene.remove(g12)
    scene.play(Transform(g, g2))
    scene.wait(wait)
    if fade:
        scene.play(FadeOut(g))
    return g

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
        f"<span color='#0C8694'>Find the Square of </span><span color='yellow'>{snum}</span>",
        "1.  Nearest Base is: " + Span(str(base),color='red') + " with " + Span(str(ndig), color='green') + " digits",
        "1a. Our number is " + Span(str(abs(diff)), color='orange') + f" {bdiff} the base " + Span(str(base),color='red'),
        "2.  The right part of the answer is " + Span(str(abs(diff)), color='orange') + "² = " + Span(str(rans).zfill(ndig), color='yellow'),
        "3.  The left side of the answer is " + Span(snum, color='yellow') + dirs + Span(str(abs(diff)), color='orange') + " = " + Span(lans, color='yellow'),
        "4. Putting them together, our final answer is: " + Span(ans, color='yellow')
    ]
    
    Explanation(scene, text, font='Cambria Math', aligned_edge=LEFT)
    scene.next_section()
    return YCom(scene, snum, snum, base, negp, abs(diff), abs(diff), rans, lans, ans, ndig, wait, fade)

def YCom(scene, snum, snum2, base, negp, diff, diff2,  rans, lans, ans, ndig, wait, fade):
    g   = ShowOp(scene, snum, snum2, "×", "?", wait=1, fade=False)
    if negp:
        g1 = ShowOp(scene, base, snum, "-", diff, play=False)
    else:
        g1 = ShowOp(scene, snum, base, "-", diff, play=False)

    op = "-" if negp else "+"
    g2 = ShowOp(scene, snum, diff2, op, lans, play=False)
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
    g3.move_to(RIGHT*2)
    ga.move_to(DOWN*2)
    arf.next_to(ar, ORIGIN)
    alf.next_to(al, ORIGIN)
    scene.add(ga)
    scene.wait(2)
    scene.add(g1)
    scene.wait(2)
    scene.play(Transform(g1, g3))
    scene.wait(1)
    scene.play(Transform(ar, arf))
    scene.wait(1)
    scene.play(Transform(g, g2))
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
        text = [Span("Our second  method works for", color='#0C8694'),
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
            f"<span color='#0C8694'>To find the Square of a number </span><span color='yellow'>n</span>",
            "1. Find the nearest base b, and note its number of digits <span color='green'>k</span>",
            "1a. Note if n is above or below b, and note the difference <span color='orange'>d</span>",
            "2. We then divide the answer into two parts - right and left",
            "3. The right part of the answer is <span color='orange'>d²</span>, padded to " + Span("k", color='green') + " digits",
            "4. The left part of the answer, is ",
            "4a. if n less than b    ⇒ <span color='yellow'>n-</span><span color='orange'>d</span>",
            "4b. if n greater than b ⇒ <span color='yellow'>n+</span><span color='orange'>d</span>",
            "5. Append the left and right parts to get the answer"
        ]
    
        Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)

        YavadunamSquare(self, 94)
        self.next_section()

        YavadunamSquare(self, 1002)
        self.next_section()

        # # Sutra Scene
        # t0 = "अन्त्ययोर्दशकेऽपि"
        # t1 = ["अन्त्ययोः", "दशके अपि"]
        # t2 = ["<span size='smaller'>When the last</span>", "<span size='smaller'>sum to 10</span>"]
        # Sutra(self, t0, t1, t2, wait=3, scale=0.5, move=None, fade=True, font='Cambria Math')
        # self.next_section()

        # # Introduction
        # text = ["<span color='#0C8694'>We can use this to multiply numbers that</span>",
        #         "1. have identical digits barring the final one",
        #         "2. have their final digits adding up to 10"]
        # Explanation(self, text, font='Cambria Math', aligned_edge=LEFT)
        # self.next_section()

        # EkadhikenaMult(self, 33, 37)
        # self.next_section()
        
        # EkadhikenaMult(self, 72, 78)
        # self.next_section()
    
